## Modules to manage and import new training data for tesseract
These modules represent phases in the pipeline

### Phase 1 - Transform the geometry of the photo: story_photo_transformer.py
- Perform progressive perspective warps on the image given user input
### Phase 2 - extract small images: story_image_clip.py
- Allow the user to highlight and extract small drawings often captured with the story
### Phase 3 - Modify the color information of the photo
- Color manipulation to help remove lines on lined writing paper
### Phase 4 - Convert to grayscale
- Allow the user to verify and possibly modify the parameters
### Phase 5 - Convert to black and white
- Allow the user to verify and possibly modify the parameters
### Phase 6 - Line removal
- Apply automatic line removal, and allow user to manually remove writing lines
### Phase 7 - Convert to individual lines of writing
- Apply automatic writing line segmentation and allow user to verify / manually enter
### Phase 8 - Acquire ground truth
- Allow user to translate the line of text
### Phase 9 - Test and review entire story
- Run tests on the data that all other phases have created
