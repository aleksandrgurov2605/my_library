from datetime import date

from pydantic import BaseModel, ConfigDict, Field

cur_year = date.today().year

class SBookAdd(BaseModel):
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="The author of the book")
    year: int = Field(gt=0, le=cur_year, description="Year of publication of the book")
    pages: int = Field(gt=0, le=5000, description="Number of pages")
    is_read: bool = Field(default=False)


class SBookRead(SBookAdd):
    model_config = ConfigDict(from_attributes=True)

    id: int
