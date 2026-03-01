from pydantic import BaseModel, Field

from user_pool.application.common.data.dtos.auth import ClientCreateRequest


class RegisterSchema(BaseModel):
    email: str = Field(
        ...,
        description=(
            "Email address.\n"
            "Format: local-part + '@' + domain.\n"
            "Valid characters in local part: letters, digits, '._%'+-'\n"
            "End with TLD ≥ 2 letters."
        ),
        examples=["user@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=36,
        description=(
            "Raw password before hashing.\n"
            "- must NOT start with a digit\n"
            "- allowed characters: lowercase letters, digits, '_!$%'\n"
            f"- length: {8}–{36}"
        ),
        examples=["qwerty_123", "password!12"],
    )

    def to_dto(self) -> ClientCreateRequest:
        return ClientCreateRequest(email=self.email, password=self.password)