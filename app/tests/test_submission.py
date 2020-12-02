from fastapi.testclient import TestClient
from os import getenv
from app.main import app
from app.api.submission import Submission
from unittest import TestCase

client = TestClient(app)


class TestSubmission(TestCase):
    def test_submission_text(self):
        pass

    def test_submission_illustration(self):
        pass
