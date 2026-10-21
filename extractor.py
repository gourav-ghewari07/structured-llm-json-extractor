"""Provider adapters and validation for the extraction pipeline."""
import json
import os
import re
from typing import Type
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from app.prompts import build_extraction_prompt

load_dotenv()


class ExtractionError(RuntimeError):
    """Raised when an LLM response cannot be extracted or validated."""


def _strip_markdown_fence(text: str) -> str:
    """Remove optional JSON Markdown fences from a model response."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def call_llm(prompt: str) -> str:
    """Call the configured provider and return its text response."""
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower()

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ExtractionError("GEMINI_API_KEY is missing. Add it to your .env file.")
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            response = client.models.generate_content(model=model, contents=prompt)
            if not response.text:
                raise ExtractionError("Gemini returned an empty response.")
            return response.text
        except ExtractionError:
            raise
        except Exception as exc:
            raise ExtractionError(f"Gemini API request failed: {exc}") from exc

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ExtractionError("OPENAI_API_KEY is missing. Add it to your .env file.")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Return only valid JSON matching the supplied schema."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )
            content = response.choices[0].message.content
            if not content:
                raise ExtractionError("OpenAI returned an empty response.")
            return content
        except ExtractionError:
            raise
        except Exception as exc:
            raise ExtractionError(f"OpenAI API request failed: {exc}") from exc

    raise ExtractionError("Unsupported LLM_PROVIDER. Set it to 'gemini' or 'openai'.")


def extract_structured_data(
    source_text: str,
    document_type: str,
    schema: Type[BaseModel],
) -> BaseModel:
    """Generate a prompt, call the LLM, parse JSON, and validate with Pydantic."""
    if not source_text.strip():
        raise ExtractionError("Input text is empty.")

    prompt = build_extraction_prompt(document_type, source_text, schema)
    raw_response = _strip_markdown_fence(call_llm(prompt))

    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise ExtractionError(
            f"The model did not return valid JSON: {exc.msg}. "
            "Try again or inspect the provider response."
        ) from exc

    try:
        return schema.model_validate(payload)
    except ValidationError as exc:
        raise ExtractionError(f"JSON failed schema validation:\n{exc}") from exc
