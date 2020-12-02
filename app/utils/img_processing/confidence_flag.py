from google.cloud import vision
import io
from google.oauth2 import service_account


def image_confidence(image_path):
    """
    Detects text in images and calculates the confidence level for each
    character. Returns a True boolean if the overall confidence for the
    page is less than 0.85. Otherwise, returns False

        Input: Path to file where image is stored
            One image per call: run function on each image in a submission
        Output: Boolean; True if confidence level for page is less than 0.85
                False if confidence is 0.85 or greater
    """

    # If image_path is local
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    # # If image_path is a uri
    # image = vision.types.Image()
    # image.source.image_uri = uri

    # Set language to english only
    language = vision.types.ImageContext(language_hints=["en-t-i0-handwrit"])

    # Connect to Google API client
    creds = service_account.Credentials.from_service_account_file(
        "/Users/stevenchase/Desktop/Steven/Computer_Science/Lambda/labs/story_sqaud/Story Squad-6122da7459cf.json"
    )
    client = vision.ImageAnnotatorClient(credentials=creds)
    response = client.document_text_detection(
        image=image, image_context=language
    )

    # List of confidence levels of each character
    symbol_confidences = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        symbol_confidences.append(symbol.confidence)

    # If there is no text on the page
    if len(symbol_confidences) == 0:
        return "No Text Detected"
    else:
        # Calculate the overall confidence for the page
        page_confidence = sum(symbol_confidences) / len(symbol_confidences)

        # Return flag: True under 85% confident, False 85% confident or over
        if page_confidence < 0.85:
            return True
        else:
            return False
