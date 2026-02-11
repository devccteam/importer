from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field


def formatar_texto(v: str) -> str:
    return v.strip().upper()


BetterStr = Annotated[str, AfterValidator(formatar_texto)]


class NewLayout(BaseModel):
    name: BetterStr
    ext: BetterStr = Field(alias='format')

    class Config:
        populate_by_name = True
