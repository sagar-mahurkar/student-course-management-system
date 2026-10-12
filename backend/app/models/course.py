from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from flask_sqlalchemy.model import Model
from sqlalchemy import CheckConstraint, DateTime, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


if TYPE_CHECKING:
    BaseModel = Model
    from app.models.enrollment import Enrollment
else:
    BaseModel = db.Model


class Course(BaseModel):
    __tablename__ = "courses"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=db.text("gen_random_uuid()"),
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    instructor_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    duration_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "duration_hours > 0",
            name="ck_courses_duration_hours_positive",
        ),
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="course",
        passive_deletes="all",
    )
