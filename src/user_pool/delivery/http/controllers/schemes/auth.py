from pydantic import BaseModel

from user_pool.application.common.data.dtos.auth import ClientCreateRequest


class RegisterSchema(BaseModel):
    email: str
    password: str

    def to_dto(self) -> ClientCreateRequest:
        return ClientCreateRequest(email=self.email, password=self.password)