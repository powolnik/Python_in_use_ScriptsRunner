import os

def get_filepath():
    return os.getcwd()

def get_all_functionalities():
    exclude_folders = ["__pycache__", ".git", "Utils"] 
    filepath = get_filepath()
    folder_names = [name for name in os.listdir(filepath)
                if os.path.isdir(os.path.join(filepath, name))
                and name not in exclude_folders]    
    return list(folder_names)

