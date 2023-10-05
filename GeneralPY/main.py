import importlib
from Utils.PathGetters import get_all_functionalities

def main():
    available_functionalities = get_all_functionalities()
    for each in available_functionalities:
        print(each)
    
main()

# def run_functionality(functionality):
#     if functionality == "T":


# if __name__ == "__main__":
#     functionality = input("T for TextExtractor, X to quit").upper()
#     run_functionality(functionality)662481486