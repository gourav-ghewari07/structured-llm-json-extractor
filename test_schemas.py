"""Unit tests for schema validation; no API key is required."""
import unittest
from pydantic import ValidationError
from app.schemas import InvoiceData, ResumeData, LineItem


class SchemaTests(unittest.TestCase):
    def test_valid_invoice(self):
        invoice = InvoiceData(
            invoice_number="INV-01",
            currency="INR",
            total=100.0,
            line_items=[
                LineItem(description="Notebook", quantity=2, unit_price=50, amount=100)
            ],
        )
        self.assertEqual(invoice.total, 100.0)
        self.assertEqual(len(invoice.line_items), 1)

    def test_negative_line_item_amount_is_rejected(self):
        with self.assertRaises(ValidationError):
            LineItem(description="Notebook", quantity=1, unit_price=10, amount=-10)

    def test_valid_resume(self):
        resume = ResumeData(full_name="Aarav Shah", skills=["Python", "SQL"])
        self.assertEqual(resume.full_name, "Aarav Shah")
        self.assertIn("Python", resume.skills)

    def test_unknown_fields_are_rejected(self):
        with self.assertRaises(ValidationError):
            ResumeData(full_name="Aarav", invented_field="not allowed")


if __name__ == "__main__":
    unittest.main()
