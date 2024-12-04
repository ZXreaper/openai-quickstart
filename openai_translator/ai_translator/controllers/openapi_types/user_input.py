from pydantic import BaseModel


class UserInput(BaseModel):
    model_name: str
    book_file_path: str
    file_format: str