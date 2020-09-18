# Google Vision function to extract text from a local or uri hosted image

from google.cloud import vision
import io


def transcribe(image_path):
    """
    Detects document features in images and returns extracted text
    Input: Path to file where images are stored
        - Assuming 1 image per image_path
        - Code for both local image_path and remote image_path, comment out
            the apporopriate one
    Output: Transcribed text as a string
    """

    # If image_path is local
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    # # If image_path is a uri
    # image = vision.types.Image()
    # image.source.image_uri = uri

    # Connect to Google API client
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(image=image)

    # Save transcribed text
    if response.text_annotations:
        transcribed_text = response.text_annotations[0].description.replace(
            "\n", " "
        )
    else:
        print("No Text Detected")

    return transcribed_text
