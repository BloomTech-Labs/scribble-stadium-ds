# Function to produce a histogram that shows the distribution of the scores
# from the student's grade level for the current week
# Plots a vertical line of the students most recent score for comparison

# Imports
import plotly.express as px

'''
The following functions serve as validtion on the HistogramRequest
class outlined in app/api/models.py. They test for input specifications
that are specific to Story Squad; such as the grade level being between
8-12.  The error messages produced by these functions are used in
app/api/tests/test_visualization.py to validate inputs.
'''
# Check that the GradeList is of 'list' type.
def grade_list_type_test(grade_list):
  if type(grade_list) != list:
    error = "GradeList not formatted as a list."
    return error

# Check that the GradeList entries are 'int' types.
def grade_list_entry_type_test(grade_list):
  indexes = []
  if type(grade_list) != list:
    return
  for i, score in enumerate(grade_list):
    if type(score) != int:
      indexes.append(i)
  if len(indexes) >= 1:
    error = f'Index entries {indexes} of GradeList is not of type \'integer\'.'
    return error

# Checks that the Student's grade is in the valid range.
def student_grade_range_test(student_info):
  if type(student_info[0]) != int:
    return
  if student_info[0] not in range(8,13):
    error = 'Student\'s grade level is not between 8 and 12.'
    return error

# Checks that the Student's grade is of type 'int'.
def student_info_grade_number_type_test(student_info):
  if type(student_info[0]) != int:
    error = 'Student\'s grade level is not of type \'integer\'.'
    return error

# Checks that the Student's name is of type 'str' and is not empty.
def student_info_name_type_test(student_info):
  if type(student_info[1]) != str or len(student_info[1]) == 0:
    error = 'Student\'s name is not a valid \'string\' type or is empty.'
    return error

# Checks that the Student's score is of type 'int'.
def student_score_type_test(student_info):
  if type(student_info[2]) != int:
    error = 'Student\'s score is not of type \'integer\'.'
    return error

def input_error_results(grade_list, student_info):
  '''
  This compiles all of the above functions and appends any
  error messages to the 'input_error' variable.  If 'input_error'
  has a length greater than zero (meaning an input error has occured),
  the histogram function will return the error messages and not run.
  '''
  input_errors = []
  check1 = grade_list_type_test(grade_list)
  if type(check1) == str:
    input_errors.append(check1 + ' ')
  check2 = grade_list_entry_type_test(grade_list)
  if type(check2) == str:
    input_errors.append(check2 + ' ')
  check3 = student_grade_range_test(student_info)
  if type(check3) == str:
    input_errors.append(check3 + ' ')
  check4 = student_info_grade_number_type_test(student_info)
  if type(check4) == str:
    input_errors.append(check4 + ' ')
  check5 = student_info_name_type_test(student_info)
  if type(check5) == str:
    input_errors.append(check5 + ' ')
  check6 = student_score_type_test(student_info)
  if type(check6) == str:
    input_errors.append(check6 + ' ')
  return input_errors


def histogram(grade_list, student_info):
    """
    Plotly histogram of all of the submission scores for the student's grade
    for the current week
    
    Plots a vertical line for the student's most recent score so they can see
    how it compares to the rest of the grade

        Input: List of the current week's scores for the specific grade level
        Student information in a list in this order: 
            [grade_number, student_name, student_score]

        Output: Plotly JSON that can be passed to the web to display on the
        parent dashboard
    """
    # This returns input errors if any exist and stops the function.
    input_errors = input_error_results(grade_list, student_info)
    if len(input_errors) > 0:
      return input_errors
      
    # Dynamic variables to use for labels on the plot
    grade_number, student_name, student_score = student_info

    # Plot
    fig = px.histogram(
        x=grade_list, nbins=20, color_discrete_sequence=["#EB7E5B"]
    )
    fig.update_layout(
        title={
            "text": f"Distribution of This Week's Grade {grade_number} Stories",
            "y": 0.95,
            "x": 0.5,
            "font": {"size": 25, "family": "PT Sans Narrow"},
        },
        shapes=[
            dict(
                type="line",
                yref="paper",
                y0=0,
                y1=1,
                xref="x",
                x0=student_score,
                x1=student_score,
            )
        ],
        annotations=[
            dict(
                x=student_score,
                y=0.5,
                xref="x",
                yref="paper",
                text=f"{student_name}'s submission",
                arrowhead=5,
                ax=200,
                ay=-100,
                showarrow=True,
                font=dict(family="PT Sans Narrow", size=16, color="black"),
                align="center",
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="#B5D33D",
                opacity=0.8,
            ),
        ],
        plot_bgcolor="#6CEAE6",
    )

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    fig.update_xaxes(
        title_text="Squad Score",
        showticklabels=False,
        title_font={"size": 20, "family": "PT Sans Narrow"},
    )

    fig.update_yaxes(title_text="", showticklabels=False, showgrid=False)

    # Return as json for web
    return fig.to_json()
