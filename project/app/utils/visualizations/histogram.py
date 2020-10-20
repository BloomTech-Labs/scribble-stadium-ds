# Function to produce a histogram that shows the distribution of the scores
# from the student's grade level for the current week
# Plots a vertical line of the students most recent score for comparison

# Imports
import plotly.express as px


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
