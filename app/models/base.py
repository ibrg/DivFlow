from datetime import datetime

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """
    Represents a base model for all models.

    Attributes:
        id (int): The primary key identifier for the record.
        created_at (datetime): The timestamp when the record was created.
        updated_at (datetime): The timestamp when the record was last updated.
    """

    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
