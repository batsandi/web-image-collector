import time

from .database import engine, Base
from .models import ScreenshotRun, Screenshot

# # TODO: Handle wait for db better
# Another dummy wait to improve chances
# of db being ready
time.sleep(5)

Base.metadata.create_all(bind=engine)
