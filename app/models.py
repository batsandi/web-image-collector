from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base

# TODO: decided to omit the run status for simplicity. Add later.


class ScreenshotRun(Base):
    __tablename__ = "screenshot_runs"

    id = Column(String, primary_key=True)
    start_url = Column(Text, nullable=False)

    screenshots = relationship("Screenshots",
                               back_populates="run",
                               cascade="all, delete-orphan")


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True)
    run_id = Column(String, ForeignKey("screenshot_runs.id"))
    filepath = Column(String, nullable=False)

    run = relationship("ScreenshotRun", back_populates="screenshots")
