from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class Registration(BaseModel):
    email: EmailStr = Field(..., description="Valid email address for login")
    contact: str = Field(..., description="Indian mobile number in format +91XXXXXXXXXX")
    password: str = Field(..., min_length=8, description="Hashed password (min 8 chars)")
    role_id: int = Field(..., description="Role ID (admin/user)")

    @field_validator("contact")
    @classmethod
    def validate_contact(cls, v: str) -> str: return v if re.match(r"^\+91\d{10}$", v) else (_ for _ in ()).throw(ValueError("Contact must be in format +91XXXXXXXXXX"))
