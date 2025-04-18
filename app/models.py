from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

from database import Base


class RunStatus(Enum):
    RUNNING = "RUNNING"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"


class ScreenshotRun(Base):
    __tablename__ = "screenshot_runs"

    id = Column(String, primary_key=True)
    start_url = Column(Text, nullable=False)
    status = Column(SQLAlchemyEnum(RunStatus, name="run_status_enum"))

    screenshots = relationship("Screenshots",
                               back_populates="run",
                               cascade="all, delete-orphan")


class Screenshots(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True)
    run_id = Column(String, ForeignKey("screenshot_runs.id"))
    filepath = Column(String, nullable=False)

    run = relationship("ScreenshotRun", back_populates="screenshots")
