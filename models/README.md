## Trained Models
Models are automatically saved to the name `storysquad.traineddata` in `tesstrain/data`, and new models will overwrite the old ones if not moved to another directory or renamed. So this is the directory you want to move them to, once you’ve trained your model!


As of 10/2021

-Our best performing model (`storysquadalldata4.traineddata`) gives an accuracy of 61% on a neat handwriting image (full_sample2.png). 
-I have documented how we arrived at this accuracy in the `tesseract-model training` dir README.md
- This model doesn't perform well on children's handwriting (check `tesseract-model training` dir for details)
