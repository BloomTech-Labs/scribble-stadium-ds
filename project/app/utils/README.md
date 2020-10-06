### Overview of `utils` content:

#### `complexity` subfolder:
- `squad_score.py`: Contains two functions: `metrics`, which generates a single row DataFrame of complexity metrics from a transcription string, and `squad_score` which takes a single row of complexity metrics and outputs a complexity metric integer, or "Squad Score."

#### `img_processing` subfolder:
- `transcription.py`: Utilizes the Google Cloud Vision API and their `document_text_detection` method to transcribe text from a given image
- `safe_search.py`: Utilizes the Google Cloud Vision API and their `safe_search` method to perform moderation of user uploaded illustrations
- `google_api.py`: Utilizes methods from `transcription.py` and `safe_search.py` to provide the DS API with an Object Oriented Programming interface to the Google API and to prepare the google credentials for parsing by the Google API
- `confidence_flag.py`: Utilizes the Google Cloud Vision API to calculate a confidence level for each page transcription. Will return a flag if the confidence level is below 0.85.
