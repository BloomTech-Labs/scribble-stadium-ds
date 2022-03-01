from pathlib import Path
from sys import argv


# To run this file locally, use a terminal with the command:
#   <path to file> <path to folder>
#       example: ./.github/workflows/update_structured_experiments_readme.py ./structured_experiments

# Checks for path argument in system variables
# First argument is this file
# Second argument is the user supplied path
if argv and len(argv) == 2:
    cwd = Path(argv[1])
elif argv and len(argv) > 2:
    raise Exception(f'Expected to arguments but received {len(argv)-1}')
else:
    raise TypeError('Could not find experiments parent directory.')


def update_readme(wd):
    """
    Updates Structured Experiments README. Takes path as string to structured experiments folder.
    Outputs 'README Updated Successfully'.
    ----------
    input   : string path to structured experiments folder
    output  : string 'README Updated Successfully' upon successful update
    """

    # Instantiate the list of experiments to be added to readme as a string
    exp_readme_list = ''

    # Iterate over the structured_experiments directory
    for exp_dir in wd.iterdir():
        # Create a path for each experiment folder encountered
        exp_dir = Path('/'.join([wd.name, exp_dir.name]))
        if not exp_dir.is_file():
            # Get name of markdown file
            file = [i for i in exp_dir.glob('*.md')]
            if file:
                with file[0].open('r') as f:
                    # Read the first line, which contains the description
                    tmp_desc = f.readline()
                    # Get the position of the last character in the description
                    desc_end_idx = tmp_desc.find('-->')
                    # Extract description by indexing the extracted line
                    tmp_desc = tmp_desc[8:desc_end_idx]
                    # Instantiate empty string to remove unnecessary portions of the path
                    delete_text = ''
                    # Removes the parent folders while building the experiment readme directory entry
                    exp_entry = f'###[{exp_dir.name}]({exp_dir.name.replace(wd.name, delete_text)})\n####{tmp_desc}\n'

                # Appends most recent entry to top of readme directory list
                exp_readme_list = exp_entry + exp_readme_list

    # Creates the path to structured experiments README
    main_readme_path = Path('/'.join([wd.name, 'README.md']))

    # Reads the contents currently in the README
    main_readme_contents = main_readme_path.read_text()
    # Gets the index of the beginning of the experiment directory
    main_idx = main_readme_contents.find('##Experiment Directory') + 23
    # Replaces the current experiments directory with an update version
    main_readme_contents = main_readme_contents.replace(main_readme_contents[main_idx:], exp_readme_list)
    # Rewrites the README in it's entirety
    main_readme_path.write_text(main_readme_contents)


update_readme(cwd)
