## Contents of API folder

`clustering` : This endpoint takes a list of cohort and submission objects and then returns clusters based on cohort in groups of four.

`db` : database functions : This gets a SQLAlchemy database connection. Uses this environment variable if it exists: `DATABASE_URL=dialect://user:password@host/dbname`. Otherwise uses a SQLite database for initial local development.

`models` :  This contains endpoints for text and illustration submissions, along with line graph, histogram, and crop cloud requests.

`submission` : Contains a function that takes a submission object and calls the Google Vision API to text annotate the passed s3 link, then passes those concatenated transcriptions to the SquadScore method. Also contains a function that checks the illustration against the Google Vision SafeSearch API and flags if explicit content is detected.

`visualization` : This contains endpoints for Story Squad’s main visualizations: line graphs, histograms, and the crop cloud.
