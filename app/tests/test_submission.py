import unittest
from os import getenv
# from ..api.submission import Submission
from unittest import TestCase
import requests
from ..api.submission import submission_illustration
from ..api.models import ImageSubmission
from os import getenv
from dotenv import load_dotenv


load_dotenv()

class TestSubmission(unittest.TestCase):
    host_url = 'http://127.0.0.1:8000'
    @classmethod
    def setUpSubmission(cls):
        pass

    def test_submission_text(self):
        pass

    def test_submission_illustration(self):

        token = getenv('DS_SECRET_TOKEN')
        headers = {
                    'accept': 'application/json',
                    'Authorization': f'{token}',
                    'Content-Type': 'application/json',
                    }
        data = '{"SubmissionID":265458,"URL":"https://artprojectsforkids.org/wp-content/uploads/2020/04/Minion-791x1024.jpg","Checksum":"bb5d2ce7b35d3c9a300b11fce49450eb321fb23dd5307da45649e4fa588891ed79aaef1de94d9f341cafba90b2887930d06a94b97a7bffad1b6ed325e4b2d54f"}'

        response = requests.post('http://127.0.0.1:8000/submission/illustration', headers=headers, data=data)
        assert response.status_code





