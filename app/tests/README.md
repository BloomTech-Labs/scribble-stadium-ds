## Python Unittest

This documentation will help in the running of the included test suite.

Firstly, for the test to provide any desirable response for the testing of the endpoints,
it will be necessary to launch the application locally, as this is set up for local testing.
Once into the pipenv shell, the next step is to launch the app.
The command from the command line is:

`uvicorn app.main:app --reload`

Once it can be confirmed that the local instance is running, testing the application
can be done by running the following command:

`python -m unittest discover`

The "discover" part of the command line will discover all the available tests, and run
all of them.  These tests can be run individually if you would like.  Documentation on
the different modifications to this command can be found in the documentation for
unittest, which lies just below.

[Documentation for Unittest](https://docs.python.org/3/library/unittest.html)
 
[Documentation for Uvicorn](https://www.uvicorn.org/)

---

At the time of writing the readme, the illustration endpoint, the histograph endpoint,
and the linegraph endpoint have tests completed.  Further exploration of the code will
reveal additional testing opportunities.

Note: all commands listed above are using a Windows Powershell prompt.  Check the docs
pertaining to your specific environment for potential necessary changes.
