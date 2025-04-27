from .models import Screenshot, ScreenshotRun

import logging

logger = logging.getLogger(__name__)


# Start a new run
def create_screenshot_run(
    db,
    run_id,
    start_url,
):
    db_run = ScreenshotRun(
      id=run_id,
      start_url=start_url,
    )
    db.add(db_run)
    db.commit()

    logger.info(f"Created new screenshot run with ID: {run_id} and start URL: {start_url}")

    return db_run


# Def a func to create screenshot records in the db
def create_screenshot(
      db,
      run_id,
      filepath
):
    db_screenshot = Screenshot(
        run_id=run_id,
        filepath=filepath
    )
    db.add(db_screenshot)
    db.commit()

    logger.info(f"Created new screenshot with filepath: {filepath}")

    return db_screenshot


# A function to return the screenshot filepaths per requested screenshot run
def get_screenshots_for_run(
    db,
    run_id
):
    logger.info(f"Returning screenshots for run ID: {run_id}")

    return db.query(Screenshot).filter(Screenshot.run_id == run_id).all()
