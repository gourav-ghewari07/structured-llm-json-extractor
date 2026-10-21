"""Pydantic schemas used to validate extracted document data."""
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class LineItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    description: str = Field(description="Description of the product or service")
    quantity: float = Field(ge=0)
    unit_price: float = Field(ge=0)
    amount: float = Field(ge=0)


class InvoiceData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = Field(default=None, description="Date in YYYY-MM-DD format if available")
    vendor_name: Optional[str] = None
    customer_name: Optional[str] = None
    currency: Optional[str] = Field(default=None, description="Currency code, such as INR or USD")
    subtotal: Optional[float] = Field(default=None, ge=0)
    tax: Optional[float] = Field(default=None, ge=0)
    total: Optional[float] = Field(default=None, ge=0)
    line_items: List[LineItem] = Field(default_factory=list)


class ResumeData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)
    experience: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)


SCHEMA_BY_TYPE = {
    "invoice": InvoiceData,
    "resume": ResumeData,
}
