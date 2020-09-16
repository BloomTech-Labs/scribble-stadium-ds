# Connect to Google Cloud Vision API and utilize their safe_search to
# moderate illustration submissions

from google.cloud import vision
import io


def detect_safe_search(path):
    '''
    Detects adult, violent or racy content in uploaded images
        Input: path to the image file
        Output: String, either stating 'No inappropriate material detected'
            or 'Image Flagged' with information about what is inappropriate
    '''

    client = vision.ImageAnnotatorClient()

    # If local illustration
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    # # If remote illustration
    # image = vision.types.Image()
    # image.source.image_uri = uri

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    # Check illustration against each safe_search category
    # Flag if inappropriate material is 'Possible' or above
    if safe.adult > 2 or safe.violence > 2 or safe.racy > 2:
        # Set flag - provide information about what is inappropriate
        flagged = [
            ('adult: {}'.format(likelihood_name[safe.adult])),
            ('violence: {}'.format(likelihood_name[safe.violence])),
            ('racy: {}'.format(likelihood_name[safe.racy])),
        ]
        return f'Image Flagged: {flagged}'

    else:
        return 'No inappropriate material detected'
