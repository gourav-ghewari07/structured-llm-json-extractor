"""Command-line interface for the structured extraction project."""
import argparse
import json
import sys
from pathlib import Path
from app.extractor import extract_structured_data, ExtractionError
from app.schemas import SCHEMA_BY_TYPE


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract validated JSON from invoice or resume text using an LLM."
    )
    parser.add_argument("--type", choices=sorted(SCHEMA_BY_TYPE), required=True,
                        help="Type of document to extract.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", help="Path to a UTF-8 text file.")
    source.add_argument("--text", help="Document text in quotes.")
    parser.add_argument("--out", default="output/result.json",
                        help="Output JSON path (default: output/result.json).")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        text = Path(args.file).read_text(encoding="utf-8") if args.file else args.text
        schema = SCHEMA_BY_TYPE[args.type]
        result = extract_structured_data(text, args.type, schema)
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result.model_dump(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Success: validated {args.type} data saved to {output_path}")
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
    except (OSError, ExtractionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
