import os
def list_directories(path):
    try:
        print(path)

        for item in os.listdir(path):
            full_path = os.path.join(path, item)

            if os.path.isdir(full_path):
                list_directories(full_path)
    except PermissionError:
        pass
    except FileNotFoundError:
        pass

list_directories('C:\\')