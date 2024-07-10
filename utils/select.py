from utils.specialprint import printe, filecolored

def select_xml(items, attr):
    reversed_items = list(reversed(items))

    for i, item in enumerate(reversed_items, start=1):
        print(f"{len(items) - i + 1}. {filecolored(item.attrib[attr])}")
    
    while True:
        try:
            selection = int(input("please enter the number of your selection: "))
            
            if 1 <= selection <= len(items):
                return reversed_items[len(items) - selection]
            else:
                printe("invalid selection. please enter a number within the range", 1)
        except ValueError:
            printe("invalid input. please enter a number", 1)