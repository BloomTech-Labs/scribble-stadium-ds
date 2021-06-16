import unittest
from os import getenv
# from ..api.submission import Submission
from unittest import TestCase
import requests
from ..api.submission import submission_illustration
from ..api.models import ImageSubmission
from dataclasses import dataclass, field


class TestSubmission(unittest.TestCase):
    host_url = 'http://127.0.0.1:8000'
    @classmethod
    def setUpSubmission(cls):
        '''
        This sets up the variables for the submission tests.
        '''
        # This is where the API URL will go.
        cls.host_url ='http://127.0.0.1:8000'
        # Correct data and checksum:
        cls.a1 = submission_illustration({
        "SubmissionID":554566,
        "URL":'Image_scoring/Data/Training/1/5d0d6e8b5e.jpg',
        "Checksum":'3f96ee854e28f71234633cdf0ead8255c203b006688748383cb38e3b88d1d9975515297a15fc8db04ae0c7c738e8579c08a933c787ef31e90978680064983993'
        })

    def test_submission_text(self):
        pass

    def test_submission_illustration(self):
        # image_object = ImageSubmission(
        #     "SubmissionID"= 265458,
        #     "URL" = Field("https://artprojectsforkids.org/wp-content/uploads/2020/04/Minion-791x1024.jpg"),
        #     "Checksum" = "bb5d2ce7b35d3c9a300b11fce49450eb321fb23dd5307da45649e4fa588891ed79aaef1de94d9f341cafba90b2887930d06a94b97a7bffad1b6ed325e4b2d54f"
        #     )

        response_code = requests.post("http://127.0.0.1:8000/submission/illustration", data={
            "SubmissionID":265458,
            "URL":"https://artprojectsforkids.org/wp-content/uploads/2020/04/Minion-791x1024.jpg",
            "Checksum":"bb5d2ce7b35d3c9a300b11fce49450eb321fb23dd5307da45649e4fa588891ed79aaef1de94d9f341cafba90b2887930d06a94b97a7bffad1b6ed325e4b2d54f"
            })
        print(response_code.status_code)




