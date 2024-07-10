from utils.bcolors import bcolors

def printe(message, exit_status=0): #print error
    print(f"{bcolors.FAIL}error:{bcolors.ENDC} {message}")
    if exit_status == 0:
        exit()
def printw(message): #print warning
    print(f"{bcolors.WARNING}warning:{bcolors.ENDC} {message}")

def filecolored(path):
    return bcolors.OKBLUE + path + bcolors.ENDC
