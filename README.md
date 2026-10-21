# Structured LLM Prompt Pipeline & JSON Extractor

A beginner-friendly Python project that extracts structured information from unstructured text (such as invoices and resumes) using an LLM API, then validates the result with **Pydantic** before saving JSON.

## Features

- Supports **Google Gemini** or **OpenAI** through a simple provider setting.
- Reusable prompt templates for invoice and resume extraction.
- Pydantic schemas validate the extracted fields and data types.
- Reads text from a `.txt` file or directly from the command line.
- Saves validated results as JSON.
- Includes sample inputs and tests that run without an API key.

## Project structure

```text
structured_llm_json_extractor/
├── app/
│   ├── __init__.py
│   ├── cli.py
│   ├── extractor.py
│   ├── prompts.py
│   └── schemas.py
├── examples/
│   ├── invoice.txt
│   └── resume.txt
├── tests/
│   └── test_schemas.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 1. Requirements

- Python 3.10 or newer
- A Gemini API key **or** an OpenAI API key for live extraction

## 2. Install

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

## 3. Configure your API key

Copy `.env.example` to `.env`, then add your own key. Never commit `.env` or share your API key.

For Gemini:
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

For OpenAI:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Use one provider at a time. Model names and API availability can change, so check the provider's current documentation if a model is unavailable.

## 4. Run the extractor

Extract an invoice:
```bash
python -m app.cli --type invoice --file examples/invoice.txt --out output/invoice.json
```

Extract a resume:
```bash
python -m app.cli --type resume --file examples/resume.txt --out output/resume.json
```

Or pass text directly:
```bash
python -m app.cli --type resume --text "Aarav Shah is a Python developer with SQL and Power BI skills." --out output/resume.json
```

The program sends the text to the selected LLM, parses the response as JSON, validates it against the chosen Pydantic model, and only then writes the output file. If validation fails, the program exits with an error instead of silently saving invalid data.

## 5. Example output

For `examples/invoice.txt`, the output will look similar to:

```json
{
  "invoice_number": "INV-2026-104",
  "invoice_date": "2026-10-15",
  "vendor_name": "Bright Office Supplies",
  "customer_name": "Northstar Analytics",
  "currency": "INR",
  "subtotal": 12500.0,
  "tax": 2250.0,
  "total": 14750.0,
  "line_items": [
    {
      "description": "Office chairs",
      "quantity": 5,
      "unit_price": 2500.0,
      "amount": 12500.0
    }
  ]
}
```

LLMs can make mistakes. Always verify extracted values against the original document before using them for financial, hiring, or other important decisions.

## 6. Run tests

```bash
python -m unittest discover -s tests -v
```

Tests cover schema validation and do not call an LLM API.

## 7. Push to GitHub

1. Create a new empty repository on GitHub, for example `structured-llm-json-extractor`.
2. Extract this ZIP file and open a terminal inside the project folder.
3. Run:

```bash
git init
git add .
git commit -m "Build structured LLM JSON extractor"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/structured-llm-json-extractor.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Tech stack

- Python
- Google Gemini API / OpenAI API
- Pydantic
- python-dotenv
- unittest

## Future improvements

- Add PDF/DOCX file text extraction.
- Add a Streamlit web interface.
- Add retry handling for temporary API errors.
- Add confidence scores and a review screen.
- Add more document schemas, such as purchase orders and job descriptions.
