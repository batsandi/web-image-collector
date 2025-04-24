from unittest.mock import Mock

from app.crud import create_screenshot_run
from app.models import ScreenshotRun


class TestScreenshotRun:
    def test_screenshot_run_creation(cls    ):
        test_db = Mock()
        test_run_id = "4200"
        test_start_url = "https://eedited.com"

        result = create_screenshot_run(
            db=test_db,
            run_id=test_run_id,
            start_url=test_start_url,
        )

        assert isinstance(result, ScreenshotRun)
        assert test_db.add.call_count == 1
        assert test_db.commit.call_count == 1
