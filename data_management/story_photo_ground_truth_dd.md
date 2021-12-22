#Design documentation for story_photo_ground_truth.py

###The purpose of this module is to allow the user to easily and accurately verify the ground truth or label of the segmented image.

To this end the module will be designed with these features
- the module will:
    - work in line just like the other phases, it will open and proceed from the previous phase
    - automatically load the written text segments from the segmentation phase
    - automatically load any provided ground truth file and attempt to pair segments with ground truth (gt)
    - allow the user to view the entire story at the same time to help with context and labeling the gt
    - provide instructions for the formatting and creation of ground truth text files
    - provide the user an option to mark a segment as **INVALID**
    - require that each segment be either marked as **DONE** or **INVALID** before proceeding
    - make available to the next phase .png and .gt pairs.

---
Plan:
The UI should be a horizontal and vertical flow:

```
|------------------------------------|
|   |  written text         | button |
| 1 |-----------------------|  area  |
|   |[ground truth text box]|        |
|------------------------------------|
|   |  written text         | Invalid|
| 2 |-----------------------|  Done  |
|   |[ground truth text box]|        |
|------------------------------------|
```

this can more quickly be facilitated with a custom tk widget.

structure:
- frame; horz layout
  - label
  - frame; vert layout
    - canvas
    - textbox
  - frame; vert layout
    - button1
    - button2

1. finding the clips to use can be done with glob.glob
2. approximating the correct line of text can be done by seperating on new lines and counting
3. as each segment is marked as done or invalid its status should be changed on the filesystem
4. invalid segments should not be deleted but instead renamed with -invalid- in the filename
5. done segments should be renamed with -validated- in the file name and the .gt file as well
---
Managing state
- States
  - state of validation for each segment
    - unprocessed
    - invalid
    - valid
    - stored in filename
    - communicated by color and pressed state of toggle buttons
    - as well communicated in filename on file system
  - state of validation for the entire story
    - once the entire story has been validated by the user pressing the done button the phase directory will be renamed with -validated appended
    - validated
    - unvalidated
    - stored in phase directory name