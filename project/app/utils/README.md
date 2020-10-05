### Overview of `utils` content:

`img_processing` subfolder:
- `transcription.py`: Utilizes the Google Cloud Vision API and their `document_text_detection` method to transcribe text from a given image
- `safe_search.py`: Utilizes the Google Cloud Vision API and their `safe_search` method to perform moderation of user uploaded illustrations
- `google_api.py`: Utilizes methods from `transcription.py` and `safe_search.py` to provide the DS API with an Object Oriented Programming interface to the Google API and to prepare the google credentials for parsing by the Google API
