# Onboarding script notebooks

Suggestions: Take the time to run both onboarding script files within colab to make sure you understand how the code runs and how it populates the images.

---

**You will need:**
- The included form.jpg - this is the onboarding form filled sample handwriting. The original, unfilled form is also included for your referaence.

- Tesseract.exe - Onboarding script 1 uses tesseracte.exe in order to run. I had some issues with downloading and tellng colab where to find the file so I just added it to the files when running the notebook.

---

These are the colab notebooks made to create functions for two purposes

1. (Onboarding script 1) Take the onboarding form and find the contours of the boxes that house the handwriting, extracting each separate box and saving it as its own .jpg. This will auto create all of the jpgs within the file that the code is run. 

2. (Onboarding script 2) Take the .jpg of the handwriting inside the box and extract each singular character as .jpgs, to then be turned into a list of images. This will also create all of the jpgs within the file that the code is run.

**OBJECTIVE**

Extract each character from each cropped box of handwriting, and turn the images into a dictionary. (i.e. all handwritten a's are the value for the key of a, all handwritten b's are the value for the key of b, etc.)

**WHAT NEEDS TO BE DONE**

1. The first function needs to be automated so that the output JPGs are automatically filtered through the second function to create the jpgs of the characters.

2. The function to create the jpgs of the characters needs to loop through all available "cropped" images of the handwritten sentences. 