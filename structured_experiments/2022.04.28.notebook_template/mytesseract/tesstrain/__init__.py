import subprocess
import os


def run_system_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        print(output.decode("utf-8"))
        return True
    except subprocess.CalledProcessError as exc:
        print("message: {}".format(exc))
        return False

def train_tesseract(make_folder, tessdata_folder="/train/tessdata", **kwargs):
    # kwargs is a dictionary where each key is the keyword and each value is the corresponding argument value
    make_arguments = generate_make_arguments(kwargs, tessdata_folder=tessdata_folder)
    command = f"cd {make_folder} && make training {make_arguments}"
    print(f'Running C code (via make) to train a tesseract model: {command}')
    ran_succesfully =  run_system_command(command)
    if ran_succesfully:
        run_system_command(f"cp {os.path.join(make_folder, 'data')}/{kwargs['model_name']}.traineddata {tessdata_folder}/{kwargs['model_name']}.traineddata")


def generate_make_arguments(argument_dictionary, **kwargs):
    argument_strings = []
    seen = set() # set data structure https://pyshark.com/everything-about-python-set-data-structure/
    
    #Places every key/value pair in argument_dictionary into kwargs. 
    # Overwrites kwargs value with argument_dictionary value when there are conflicts
    kwargs.update(argument_dictionary)

    # loop through kwargs and format each argument as a make argument
    for argument_key, argument_value in kwargs.items():
        argument_key_upper = argument_key.upper()
        if argument_key_upper in seen:
            print(f'Not adding key "{argument_key_upper}" as it is redundant with another argument')
        else:
            argument_strings.append(f"{argument_key_upper}={argument_value}")
            seen.add(argument_key_upper)
    return " ".join(argument_strings)

# train_tesseract("data", "/train/tessdata", model_name="helloworld", start_model="eng", tessdata="/train/tessdata", max_iterations=100)