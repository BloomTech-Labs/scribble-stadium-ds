# CICD Pipeline #

On every push this action will run and check python files that have been changed or created for syntax errors.

- - - -

## Usage ##
To see the action in progress click on the actions tab from the branch homepage. Then click the tab titled linting, you will then be able to view the progress of the action.

If any files cause a flag the test will fail and the name of the files will show along with the recommended changes.

- - - -

## Tools ##
Utilizes the [Super Linter Repo](https://github.com/github/super-linter)
Currently it is configured to only check new or edited python files. The super linter has the capability to check almost every possible file type.

VALIDATE_ALL_CODEBASE is currently set to false, this is what sets it to only check new files. If set to true then it will check all python files no matter what.

A word of Caution:Setting VALIDATE_ALL_CODEBASE to true and removing python variables will check every single file in the whole repo, it will take upwards of 2 hours.


