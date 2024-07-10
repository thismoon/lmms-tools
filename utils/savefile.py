import os
from utils.specialprint import printe, printw, filecolored
import re

def savefile(data, path):
    if isinstance(data, str):
        write_mode = 'w'
    elif isinstance(data, bytes):
        write_mode = 'wb'
    if os.path.isfile(path):
        printw(f"'{filecolored(os.path.basename(path))}' already exists")
        response1 = yes_no_question("overwrite?", "n")
        if response1 == "y":
            unsafe_save(path, write_mode, data)
            return path
        else:
            new_path = auto_rename(path)
            response2 = yes_no_question(f"save to '{filecolored(os.path.basename(new_path))}'?", "y")
            if response2 == "y":
                unsafe_save(new_path, write_mode, data)
                return new_path
            else:
                printw("didn't save anything")
    else:
        unsafe_save(path, write_mode, data)
        return path

def auto_rename(path):
    path_parts = os.path.splitext(path)
    if re.match(r".+ \((\d+)\)$", path_parts[0]):
        re_groups = re.match(r"(.+)( \((\d+)\))$", path_parts[0])
        counter = int(re_groups.group(3))
        path_parts = (re_groups.group(1), path_parts[1])
    else:
        counter = 0
    new_path = path
    while os.path.isfile(new_path):
        counter+=1
        new_path = path_parts[0] + f" ({counter})" + path_parts[1]
    return new_path

def yes_no_question(question, default_response):
    choices = "[Y/n]" if default_response == "y" else "[y/N]"
    while True:
        response = input(f"{question} {choices}: ").strip().lower()
        if not response:
            return default_response
        if response in ["y", "n"]:
            return response
        else:
            printe("sorry, invalid response. please answer with y or n", 1)

def unsafe_save(a, b, c):
    with open(a, b) as f:
            f.write(c)

def script_save(data, path, existing_behavior): # existing_behavior = "rename" or "overwrite"
    if isinstance(data, str):
        write_mode = 'w'
    elif isinstance(data, bytes):
        write_mode = 'wb'
    if os.path.isfile(path):
        if existing_behavior == "rename":
            unsafe_save(auto_rename(path), write_mode, data)
        elif existing_behavior == "overwrite":
            unsafe_save(path, write_mode, data)
    else:
        unsafe_save(path, write_mode, data)
