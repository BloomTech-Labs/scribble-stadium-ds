Google Vision to Tesseract transition


Main files used:
app/api/models.py
    Purpose: 
        Defines “Submission” class: submission ID, story ID, pages (pg#: URL)
    Assessment: 
        Does not need to be modified to handle Tesseract output.

app/api/submission.py
    Purpose: 
        Obtains: [confidence flag, content flag, transcript] from google_api.py
        Returns: SubmissionID, IsFlagged (T/F), LowConfidence (T/F), Complexity (score), WordCount
	Assessment:
        Will need some modifications to handle Tesseract, but nothing major as long as the data items above can be obtained from Tesseract in the same format.

app/utils/img-processing/google_api.py
Purpose:
 	The “GoogleAPI” class does a lot:
        1 Connects to Google Vision client: vision.ImageAnnotatorClient()
        2 Obtains transcribed text for all pages
        3 Calculates overall confidence score (by symbol not word) and returns True (confidence < 0.85) or False (≥0.85)
        4 Puts each word through content moderator and returns True if any word is flagged
	Assessment:
        1 Items 1, 2, 3 use Google Vision and will need Tesseract versions.
        2 #4 uses an in-house function and word list that should work with Tesseract output (app/utils/moderation/text_moderation.py).


Questions: 
1 The GoogleAPI class also contains an image moderator (detect_safe_search) that uses Google Vision. Will this also need to be replaced? 
2 How functional is [app/utils/img_processing/tesseract_api.py]? It appears to do 1, 2, 4 in the list of GoogleAPI actions above. 
3 How to calculate confidence using Tesseract? 
    Possible tools: https://github.com/sirfz/tesserocr, https://github.com/tesseract-ocr/tessdoc/blob/main/APIExample.md
