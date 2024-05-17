import os
import errno
import json


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
    current_data = openJsonFile(file_path)
    if current_data:  # If the file is not empty
        current_data.update(data)
        return writeJsonFile(file_path, current_data)
    return False


def deleteJsonFile(file_path):
    if checkFileExists(file_path):
        os.remove(file_path)
        return True
    return False
