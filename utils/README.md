**Explanation of essaycheck_script.py**

**How to Run This Script:**

Place the script in the repo's top-level directory. cd into the repo from the command line and enter the following:
```angular2html
python essaycheck_script.py
```

**What it Does:**

The essaycheck_script.py file scans the repo for image files that potentially might be full essays.

**What it Finds:**

The script finds files with the following extensions:
    * .png
    * .jpg
    * .tif

The script returns the total number of image files along with a breakdown of the totals for image files in the following two categories:
1. Files that are likely to be full essays 
2. Files that are likely to be individual snippets

**What the Script Does Not Do:**

The script does not remove the files that it finds. The user will need to make a determination about whether a file was inadvertently pushed and needs to be removed to comply with COPPA regulations.

The threshold for determining whether or not a file is likely to be a snippet or a full original essay currently is 
determined by its file size. Any files greater than 260000 bytes are possibly full essay images.

_Note: This script will be refactored shortly to have an additional check based on file dimensions to further increase the accuracy of the results._
