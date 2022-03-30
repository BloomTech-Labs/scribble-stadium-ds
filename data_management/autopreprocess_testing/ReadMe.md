This is a brief overview of the preprocessing_pipeline and preprocessing_directory files. As stated in the docstring we are attempting to pull all necessary files for testing the model in one function.  This current commit attempts to elucidate some of the inline documentation that appeared in the previous commit.   
Steps for using the preprocessing pipeline
    1. Run the preprocessing_directory.py file
    2. In the command line, specify the file path for the preprocessing_directory.py file (See above) as well as the source directory that you are pulling image or text files from(your dataset).  The line below gives an example.
    
python3 .\data_management\autopreprocess_testing\example.py .\data_management\autopreprocess_testing\test_images

**Note there is a space between the directory path and the file path.**
Currently, you must run the preprocessing_directory.py file to run this function.