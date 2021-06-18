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
        # Code to load .env file for secret credentials
        load_dotenv()
        # Get secret credentials from .env file
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
            before anything else runs.  Some of the items
            will not be 'HistogramRequest' models.  This
            is because that model will automatically convert
            data types to the correct type.  For purposes
            of testing input types, we will build failing
            objects ourself.
        """

        # Properly structured dummy data for testing desired responses.
        cls.d1 = HistogramRequest(
            GradeList=[1005, 1500, 9000, 789, 800, 1000, 1300],
            GradeLevel=8,
            StudentName="Sally",
            StudentScore=600
        )
        cls.data1 = return_histogram(cls.d1)

        # This data has a score as a string, and is not a HistogramRequest
        cls.d2 = [['789', 800, 1000, 1300], [8, "Jane", 350]]
        cls.data2 = histogram.histogram(cls.d2[0], cls.d2[1])
    
        # This data has an invalid GradeLevel (not between 8 and 12) 
        cls.d3 = [[500, 500, 500], [7, "Jane", 500]]
        cls.data3 = histogram.histogram(cls.d3[0], cls.d3[1])

        # This data contains a non-list type GradeList.
        cls.d4 = [500, [8, "Jane", 500]]
        cls.data4 = histogram.histogram(cls.d4[0], cls.d4[1])

        # This data contains a string for StudentGrade
        cls.d5 = [[500, 500, 500], ['8', "Jane", 500]]
        cls.data5 = histogram.histogram(cls.d5[0], cls.d5[1])

        # This data is missing a StudentName
        cls.d6 = [[500, 500, 500], [8, None, 500]]
        cls.data6 = histogram.histogram(cls.d6[0], cls.d6[1])

        # This data has the StudentScore listed as a 'string' type.
        cls.d7 = [[500, 500, 500], [8, 'Jane', '500']]
        cls.data7 = histogram.histogram(cls.d7[0], cls.d7[1])

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
        except TypeError:
            return False
        return True

#     def test_empty(self):
#         """
#         This method will test if the input contains any empty fields.
#         """
#         def check_empty(data):
#             self.assertRaises(ValidationError, return_histogram(data))
# ​
#             if len(data.GradeList) == 0:
#                 self.assertEqual(histogram.histogram(
#                     data.GradeList,
#                     [data.GradeLevel, data.StudentName, data.StudentScore]),
#                     "No Score History for this User"
#                 )
# ​
#             elif data.GradeLevel is None or \
#                     data.StudentName == "" or \
#                     data.StudentScore is None:
#                 self.assertEqual(histogram.histogram(
#                     data.GradeList,
#                     [data.GradeLevel, data.StudentName, data.StudentScore]),
#                     "Not Enough Values for this User"
#                 )
# ​
#             # Tests the properly formatted dummy data
#             else:
#                 self.assertTrue(
#                     self.get_json_bool(histogram.histogram(
#                         data.GradeList,
#                         [data.GradeLevel, data.StudentName, data.StudentScore])
#                     )
#                 )
# ​
#         # This data has an empty list for the score history
#         check_empty(HistogramRequest(
#             GradeList=[],
#             GradeLevel=6,
#             StudentName="John",
#             StudentScore=700
#         ))
#         # This data has a None value for the Grade level
#         check_empty(HistogramRequest(
#             GradeList=[1005, 1500, 9000, 789],
#             GradeLevel=None,
#             StudentName="John",
#             StudentScore=700
#         ))
#         # This data has an empty string for the name
#         check_empty(HistogramRequest(
#             GradeList=[1005, 1500, 9000, 789],
#             GradeLevel=6,
#             StudentName="",
#             StudentScore=700
#         ))
#         # This data has a None value for the current score
#         check_empty(HistogramRequest(
#             GradeList=[1005, 1500, 9000, 789],
#             GradeLevel=6,
#             StudentName="John",
#             StudentScore=None
#         ))
#         pass

    def test_json(self):
        '''
        This method tests that proper input yields proper JSON output,
        then tests that input items end up in the correct location
        in the JSON object.
        '''
        # Assert True, self.data1 is formatted for proper output
        self.assertTrue(self.get_json_bool(self.data1))
        # Assert False, self.data2 should not return a JSON output
        self.assertFalse(self.get_json_bool(self.data2))

    def test_histogram(self):
        """
        This method will test the output JSON to be sure the elements of the 
        input end up in the correct JSON dictionary locations.
        """

        # Tests that the GradeList ends up in the proper section of the JSON
        case1 = json.loads(histogram.histogram([1005, 1500, 9000, 798], 
                                               [8, 'FirstName', 1058]))
        gradeList = case1['data'][0]['x']
        self.assertEqual(gradeList, [1005, 1500, 9000, 798])

        '''
        Tests that the GradeLevel appears in correct location with proper range.
        Since the GradeLevel only appears in the 'Title' section of the 
        histogram function, we run through all valid grade numbers and check
        that the 'Title' location in the JSON output reflects the proper number.
        '''
        item = 0
        for num in range(8,13):
          case2 = json.loads(histogram.histogram([1200, 0, 785, 1566],
                                                [num, 'FirstName', 1058]))
          digit1 = case2['layout']['title']['text'][34] 
          digit2 = case2['layout']['title']['text'][35]
          if num >= 1 and num <= 9:
            if digit1 == str(num):
              item += 1
          if num >= 10 and num <= 12:
            if digit1 == str(num)[0] and digit2 == str(num)[1]:
              item += 1
        self.assertEqual(item, 5)

    def test_inputs(self):
        """
        This method will test various input values for correct types and ranges
        """
        # Assert GradeLevel type error message from histogram function
        self.assertEqual(
            self.data2, ['Index entries [0] of GradeList is not of type \'integer\'. ']
            )
        
        # Assert GradeLevel range error message from histogram function
        self.assertEqual(self.data3, ['Student\'s grade level is not between 8 and 12. '])

        # Assert GradeLevel is type 'list' error message
        self.assertEqual(self.data4, ['GradeList not formatted as a list. '])

        # Assert StudentGrade is type 'integer' error message
        self.assertEqual(self.data5, ['Student\'s grade level is not of type \'integer\'. '])

        # Assert StudentName is not empty error message
        self.assertEqual(self.data6, ['Student\'s name is not a valid \'string\' type or is empty. '])

        # Assert StudentScore type error message.
        self.assertEqual(self.data7, ['Student\'s score is not of type \'integer\'. '])

    def test_response(self):
        """
        This method will test for the proper response status code.  
        'Mocking' is the testing technique you will want to apply
        here.
        """
        pass

