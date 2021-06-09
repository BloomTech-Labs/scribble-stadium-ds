"""
This file contains code for testing the endpoints in the visualization.py file
"""

import unittest
import json
from ..api.visualization import return_line_graph, return_histogram
from ..utils.visualizations import line_graph
from ..utils.visualizations import histogram
from ..api.models import LineGraphRequest, HistogramRequest


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
        # This data has an empty string for the Student Name
        cls.d3 = LineGraphRequest(
            ScoreHistory=[9000, 789, 800, 1000, 1300],
            StudentName=""
        )
        cls.data3 = return_line_graph(cls.d3)
        # This data has a score as a string
        cls.d4 = LineGraphRequest(
            ScoreHistory=[1005, 1500, '9000', 789, 800, 1000, 1300],
            StudentName="Jane"
        )
        cls.data4 = return_line_graph(cls.d4)
        # This is the default example data
        cls.d5 = LineGraphRequest(
            ScoreHistory=[1005, 1500, 9000, 789],
            StudentName="Firstname"
        )
        cls.data5 = return_line_graph(cls.d5)

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
        self.scores5, self.name5 = self.d5.ScoreHistory, self.d5.StudentName

    def get_json_bool(self, json_data):
        """
        This function will check that the file is in the json format

            :param json_data: the file/data you want to verify
            :return: bool: True or False if in json format
        """
        try:
            json.loads(json_data)
        except ValueError as err:
            return False
        return True

    def test_empty(self):
        """
        This method will test if the input contains any empty fields.
        """
        # Tests the properly formatted dummy data
        self.assertTrue(
            self.get_json_bool(line_graph.line_graph(self.scores1, self.name1))
        )
        # Tests the dummy data with empty list for the score history
        self.assertEqual(line_graph.line_graph(self.scores2, self.name2),
                         "No Submissions for This User")
        # Tests the dummy data with empty string for the student name
        self.assertEqual(line_graph.line_graph(self.scores3, self.name3),
                         "No User Specified")

    def test_ints(self):
        """
        This method will test if all the values are integers in
            the ScoreHistory input.
        """
        # Tests the properly formatted dummy data
        self.assertTrue(
            self.get_json_bool(line_graph.line_graph(self.scores1, self.name1))
        )
        # Tests the dummy data that has a string value in ScoreHistory to
        #   verify that we are getting a TypeError raised for the wrong type
        self.assertRaises(
            TypeError, line_graph.line_graph(self.scores4, self.name4)
        )

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


    def test_line_graph(self):
        """
        This method will test the output to ensure we are getting the proper
            data outputted in the response body in the json file format.
        """
        pass


class TestHistogram(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        This method will run its code at the beginning,
            before anything else runs.
        """

        # This data is in the proper input format we need
        cls.d1 = HistogramRequest(
            GradeList=[1005, 1500, 9000, 789, 800, 1000, 1300],
            GradeLevel=5,
            StudentName="Sally",
            StudentScore=600
        )
        cls.data1 = return_histogram(cls.d1)
        # This data has an empty list for the score history
        cls.d2 = HistogramRequest(
            GradeList=[],
            GradeLevel=6,
            StudentName="John",
            StudentScore=700
        )
        cls.data2 = return_histogram(cls.d2)
        # This data has a score as a string
        cls.d3 = HistogramRequest(
            GradeList=[1005, 1500, 9000, '789', 800, 1000, 1300],
            GradeLevel=4,
            StudentName="Jane",
            StudentScore=350
        )
        cls.data3 = return_histogram(cls.d3)
        # This is the default example data
        cls.d4 = HistogramRequest(
            GradeList=[1005, 1500, 9000, 789],
            GradeLevel=8,
            StudentName="Firstname",
            StudentScore=1058
        )
        cls.data4 = return_histogram(cls.d4)

    def setUp(self):
        """
        This method will run its code before each
            individual test is ran within this class.
        """
        # Create test variables for the grade list and student info based on dummy data
        self.grades1 = self.d1.GradeList
        self.info1 = [self.d1.GradeLevel, self.d1.StudentName, self.d1.StudentScore]
        self.grades2 = self.d2.GradeList
        self.info2 = [self.d2.GradeLevel, self.d2.StudentName, self.d2.StudentScore]
        self.grades3 = self.d3.GradeList
        self.info3 = [self.d3.GradeLevel, self.d3.StudentName, self.d3.StudentScore]
        self.grades4 = self.d4.GradeList
        self.info4 = [self.d4.GradeLevel, self.d4.StudentName, self.d4.StudentScore]

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

    def test_histogram(self):
        """
        This method will test the output to ensure we are getting the proper
            data outputted in the response body in the json file format.
        """
        pass
