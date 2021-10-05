## Phases / Modules to manage and import new training data for tesseract
- Each module should by default take as input the output of the previous phase/module
- Each module should also be able to be launched seperatly and work on whatever input the user gives it
- Each module should be one phase
- The first module also includes code that sequentially runs the next phases
- Each module will retain information about what [paramaters](https://datascience.stackexchange.com/questions/14187/what-is-the-difference-between-model-hyperparameters-and-model-parameters) and [hyper-parameters](https://en.wikipedia.org/wiki/Hyperparameter_(machine_learning)) the user used to create the output


These modules represent phases in the pipeline

### Phase 0 - Transform the geometry of the photo: story_photo_transformer.py
- Perform progressive perspective warps on the image given user input
### Phase 1 - extract small images: story_image_clip.py
- Allow the user to highlight and extract small drawings often captured with the story
### Phase 2 - Modify the color information of the photo
- Color manipulation to help remove lines on lined writing paper
### Phase 3 - Convert to grayscale
- Allow the user to verify and possibly modify the parameters
### Phase 4 - Convert to black and white
- Allow the user to verify and possibly modify the parameters
### Phase 5 - Line removal
- Apply automatic line removal, and allow user to manually remove writing lines
### Phase 6 - Convert to individual lines of writing
- Apply automatic writing line segmentation and allow user to verify / manually enter
### Phase 7 - Acquire ground truth
- Allow user to translate the line of text
### Phase 8 - Test and review entire story
- Run tests on the data that all other phases have created
