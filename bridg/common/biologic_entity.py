from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .administrative_gender import AdministrativeGender
from .entity_name import EntityName


class BiologicEntity(Base):
    """
    Any individual living (or previously living) being.

    Attributes:
        id:
        administrative_gender_code:
        birth_date:
        death_date:
        death_date_estimated_indicator:
        death_indicator:
        name:
    """

    __tablename__ = "biologic_entity"
    __mapper_args__ = {
        "polymorphic_identity": "biologic_entity",
        "polymorphic_on": "type",
    }

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]

    administrative_gender_code: Mapped[Optional[AdministrativeGender]]
    birth_date: Mapped[Optional[date]]
    death_date: Mapped[Optional[date]]
    death_date_estimated_indicator: Mapped[Optional[bool]]
    death_indicator: Mapped[Optional[bool]]

    name: Mapped[List[EntityName]] = relationship(
        back_populates="biologic_entity", cascade="all, delete-orphan")

    # FIXME: return something more meaningfull than first entry
    @property
    def primary_name(self) -> Optional[EntityName]:
        return next((n for n in self.name), None)

    def __str__(self):
        if not self.primary_name:
            return "Anonymous"
        return str(self.primary_name)
