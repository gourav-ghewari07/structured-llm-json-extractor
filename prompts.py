"""Parameterized prompts for document extraction."""
import json
from typing import Type
from pydantic import BaseModel


def build_extraction_prompt(document_type: str, source_text: str, schema: Type[BaseModel]) -> str:
    schema_json = json.dumps(schema.model_json_schema(), indent=2)
    return f"""
You are a careful information-extraction assistant.
Extract information from the document below and return ONLY one valid JSON object.
Do not include Markdown fences, comments, or explanations.
Use null for missing optional scalar values and [] for missing lists.
Do not invent details. Preserve the source meaning. If a date is clear, use YYYY-MM-DD.
The output must match this JSON Schema:

{schema_json}

Document type: {document_type}

DOCUMENT TEXT START
{source_text}
DOCUMENT TEXT END
""".strip()
