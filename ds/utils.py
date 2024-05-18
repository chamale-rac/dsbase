import os
import errno
import json
from .constants import PRINT_DICTS_WITH


def checkFileExists(file_path):
    return os.path.exists(file_path)


def createDirectory(directory_path):
    try:
        os.makedirs(directory_path)
        return True
    except OSError as e:
        if e.errno != errno.EEXIST:
            return False
        return True


def checkDirectoryExists(directory_path):
    return os.path.exists(directory_path)


def loadJsonFile(file_path):
    if checkFileExists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return None


def writeJsonFile(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        return True


def createJsonFile(file_path, data):
    if checkFileExists(file_path):
        return False
    return writeJsonFile(file_path, data)


def updateJsonFile(file_path, data):
    if not checkFileExists(file_path):
        return False
    return writeJsonFile(file_path, data)
    # return False


def deleteJsonFile(file_path):
    if checkFileExists(file_path):
        os.remove(file_path)
        return True
    return False


def printDict(data):
    if PRINT_DICTS_WITH == 'pprint':
        import pprint
        pprint.pprint(data)
    elif PRINT_DICTS_WITH == 'json':
        print(json.dumps(data, indent=4))
    elif PRINT_DICTS_WITH == 'yaml':
        import yaml
        print(yaml.dump(data, default_flow_style=False))
    else:
        print(data)
