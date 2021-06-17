"""
This file contains code for testing the endpoints in the visualization.py file
"""

from os import getenv
from dotenv import load_dotenv
import unittest
import requests
import json
import pprint
from ..api.visualization import router, return_line_graph, return_histogram
from ..utils.visualizations import line_graph
from ..utils.visualizations import histogram
from ..api.models import LineGraphRequest, HistogramRequest


class TestLinegraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        A class method that will run its code at the beginning,
            before anything else runs.
        """
        # This data is in the proper input format we need,
        #   inputted in the pydantic model format
        cls.d1 = LineGraphRequest(
            ScoreHistory=[1005, 1500, 9000, 789, 800, 1000, 1300],
            StudentName="Sally"
        )
        # Using the route function to test the inputted data
        cls.data1 = return_line_graph(cls.d1)

        # This data has an empty list for the score history,
        #   inputted in the pydantic model format
        cls.d2 = LineGraphRequest(
            ScoreHistory=[],
            StudentName="John"
        )
        # Using the route function to test the inputted data
        cls.data2 = return_line_graph(cls.d2)

        # This data has an empty string for the student name,
        #   inputted in the pydantic model format
        cls.d3 = LineGraphRequest(
            ScoreHistory=[9000, 789, 800, 1000, 1300],
            StudentName=""
        )
        # Using the route function to test the inputted data
        cls.data3 = return_line_graph(cls.d3)

        # This data has a score as a string,
        #   inputted in the pydantic model format
        cls.d4 = LineGraphRequest(
            ScoreHistory=[1005, 1500, '9000', 789, 800, 1000, 1300],
            StudentName="Jane"
        )
        # Using the route function to test the inputted data
        cls.data4 = return_line_graph(cls.d4)

        # This is the default example data,
        #   inputted in the pydantic model format
        cls.d5 = LineGraphRequest(
            ScoreHistory=[1005, 1500, 9000, 789],
            StudentName="Firstname"
        )
        # Using the route function to test the inputted data
        cls.data5 = return_line_graph(cls.d5)

    def setUp(self):
        """
        This method will run its code before each
            individual test is ran within this class.
        """
        # Create test variables for the scores and names based on dummy data
        # Properly formatted dummy data
        self.scores1, self.name1 = self.d1.ScoreHistory, self.d1.StudentName
        # Dummy data with empty scores list
        self.scores2, self.name2 = self.d2.ScoreHistory, self.d2.StudentName
        # Dummy data with empty name string
        self.scores3, self.name3 = self.d3.ScoreHistory, self.d3.StudentName
        # Dummy data with one score as a string in the scores list
        self.scores4, self.name4 = self.d4.ScoreHistory, self.d4.StudentName
        # Dummy data using default data
        self.scores5, self.name5 = self.d5.ScoreHistory, self.d5.StudentName

    def get_json_bool(self, json_data):
        """
        This function will check that the file is in the json format

            :param json_data: the file/data you want to verify
            :return: bool: True or False if in json format
        """
        try:
            # If json_data is a json object, converts to a string
            json.loads(json_data)

        # Otherwise, will raise a ValueError
        except ValueError as err:
            # Not a json object, returns False
            return False

        # Is a json object, returns True
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
        load_dotenv()
        token = getenv('DS_SECRET_TOKEN')

        # Header information needed to call on the API directly
        #   Information obtained from the "Curl" command on the Swagger UI
        headers = {
            'accept': 'application/json',
            'Authorization': f'{token}',
            'Content-Type': 'application/json',
        }

        # The proper data format for inputting through the API
        data1 = '{"ScoreHistory":[1000,1500,9000,789],"StudentName":"Joanne"}'
        # Incorrect data format for inputting through the API
        data2 = '{"ScoreHistory":[1000,1500,9000,789],"StudentName":}'

        # Should return a 200 status code for properly formatted input
        response1 = requests.post(
            'http://127.0.0.1:8000/viz/linegraph', headers=headers, data=data1
        )
        # Should return a 422 status code for incorrect formatted input
        response2 = requests.post(
            'http://127.0.0.1:8000/viz/linegraph', headers=headers, data=data2
        )

        # Get the status code for properly formatted input
        stat_code1 = response1.status_code
        # Assert we are getting 200 - Successful Response
        self.assertEqual(stat_code1, 200)

        # Get the status code for incorrect formatted input
        stat_code2 = response2.status_code
        # Assert we are getting 422 - Error: Unprocessable Entity
        self.assertEqual(stat_code2, 422)


    def test_json(self):
        """
        This method will test the output to ensure we are returning the
            data in json format in the response body.
        """
        # Tests the properly formatted dummy data
        self.assertTrue(
            self.get_json_bool(line_graph.line_graph(self.scores1, self.name1))
        )

        # Tests the properly formatted dummy data
        self.assertFalse(
            self.get_json_bool(line_graph.line_graph(self.scores5, self.name5))
        )

    def test_line_graph(self):
        """
        This method will test the output to ensure we are getting the proper
            data outputted in the response body in the json file format.

        Locations of input data in the output json file:

        ['data'][0]['x'] = list: range length of score_history +1, start at 1
        ['data'][0]['y'] = list: score_history values
        ['layout']['title']['text'] = str: contains name string
        """
        # Load proper json dummy data through line_graph function for testing
        load1 = json.loads(line_graph.line_graph(self.scores1, self.name1))
        x_list = [int(i) + 1 for i in range(len(self.scores1))]
        # Load string json dummy data through line_graph function for testing
        load2 = json.loads(line_graph.line_graph(self.scores4, self.name4))

        # # This code is for finding location of the input data in the json file
        # print('\n')
        # pprint.pprint(load1)

        # Verify all of the input data is in the proper location in the
        #   json file that is outputted for properly formatted dummy data
        self.assertEqual(load1['data'][0]['x'], x_list)
        self.assertEqual(load1['data'][0]['y'], self.scores1)
        self.assertTrue(
            load1['layout']['title']['text'].__contains__(self.name1)
        )

        # Verify the string dummy data returns error message
        self.assertRaises(TypeError, load2)


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
        # This data has a score as a string
        cls.d2 = HistogramRequest(
            GradeList=[1005, 1500, 9000, '789', 800, 1000, 1300],
            GradeLevel=4,
            StudentName="Jane",
            StudentScore=350
        )
        cls.data2 = return_histogram(cls.d2)
        # This is the default example data
        cls.d3 = HistogramRequest(
            GradeList=[1005, 1500, 9000, 789],
            GradeLevel=8,
            StudentName="Firstname",
            StudentScore=1058
        )
        cls.data3 = return_histogram(cls.d3)

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

    def get_json_bool(self, json_data):
        """
        This function will check that the file is in the json format
            :param json_data: the file/data you want to verify
            :return: bool: True or False if in json format
        """
        try:
            json.loads(json_data)
        except ValueError:
            return False
        return True

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
            data in json format in the response body through the API.
        """
        pass

    def test_histogram(self):
        """
        This method will test the output to ensure we are getting the proper
            data outputted in the response body in the json file format.
        """
        pass
