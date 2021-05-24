"""
This file contains code for testing the endpoints in the visualization.py file
"""

import unittest
import json
from ..api.visualization import return_line_graph
from ..utils.visualizations import line_graph
from ..api.models import LineGraphRequest


class TestLinegraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        This method will run its code at the beginning,
            before anything else runs.
        """

        # This data is in the proper input format we need
        cls.d1 = LineGraphRequest(
            ScoreHistory=[1005, 1500, 9000, 789, 800, 1000, 1300],
            StudentName="Sally"
        )
        cls.data1 = return_line_graph(cls.d1)
        # This data has an empty list for the score history
        cls.d2 = LineGraphRequest(
            ScoreHistory=[],
            StudentName="John"
        )
        cls.data2 = return_line_graph(cls.d2)
        # This data has a score as a string
        cls.d3 = LineGraphRequest(
            ScoreHistory=[1005, 1500, '9000', 789, 800, 1000, 1300],
            StudentName="Jane"
        )
        cls.data3 = return_line_graph(cls.d3)
        # This is the default example data
        cls.d4 = LineGraphRequest(
            ScoreHistory=[1005, 1500, 9000, 789],
            StudentName="Firstname"
        )
        cls.data4 = return_line_graph(cls.d4)

    def setUp(self):
        """
        This method will run its code before each
            individual test is ran within this class.
        """
        # Create test variables for the scores and names based on dummy data
        self.scores1, self.name1 = self.d1.ScoreHistory, self.d1.StudentName
        self.scores2, self.name2 = self.d2.ScoreHistory, self.d2.StudentName
        self.scores3, self.name3 = self.d3.ScoreHistory, self.d3.StudentName
        self.scores4, self.name4 = self.d4.ScoreHistory, self.d4.StudentName

    def test_empty(self):
        """
        This method will test if the input contains any empty fields.
        """
        pass

    def test_ints(self):
        """
        This method will test if all the values are integers in the input.
        """
        pass

    def test_response(self):
        """
        This method will test for the proper response status code.
        """
        pass

    def test_json(self):
        """
        This method will test the output to ensure we are returning the
            data in json format in the response body.
        """
        pass

    def test_line_graph(self):
        """
        This method will test the output to ensure we are getting the proper
            data outputted in the response body in the json file format.
        """
        pass
