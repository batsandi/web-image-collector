
from models import Screenshot, ScreenshotRun


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
    return db_screenshot


# A function to return the screenshot filepaths per requested screenshot run
def get_screenshots_for_run(
    db,
    run_id
):
    return db.query(Screenshot).filter(Screenshot.run_id == run_id).all()
