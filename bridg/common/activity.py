from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from ..db import Base

if TYPE_CHECKING:
    from ..study import StudySite
    from .project import Project


class Activity(Base):
    __abstract__ = True

    reason_code: Mapped[Optional[str]]
    comment: Mapped[Optional[str]]

    using_project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("project.id"))

    @declared_attr
    def using_project(cls) -> Mapped[Optional[Project]]:
        """
        Each Activity might be used by one Project.
        Each Project might use one or more Activity.
        """
        return relationship()

    context_for_study_site_id: Mapped[Optional[int]] = mapped_column(ForeignKey("study_site.id"))

    @declared_attr
    def context_for_study_site(cls) -> Mapped[Optional[StudySite]]:
        """
        Each Activity might have as context one StudySite.
        Each StudySite might be the context for one or more Activity.
        """
        return relationship()
