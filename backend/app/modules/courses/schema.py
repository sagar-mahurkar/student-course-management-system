
from pydantic import BaseModel, ConfigDict, Field, model_validator


class CreateCourseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    instructor_name: str = Field(min_length=1, max_length=100)
    duration_hours: int = Field(gt=0)


class UpdateCourseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    instructor_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    duration_hours: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_update_fields(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")

        if any(
            getattr(self, field_name) is None
            for field_name in self.model_fields_set
        ):
            raise ValueError("Fields cannot be null")

        return self
