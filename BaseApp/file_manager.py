import uuid
import os
import shutil

UPLOAD_DIR = "static/uploads"
TEMP_DIR = "static/temp"


def getRandomFilename(filename):
    # Extract the file extension
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    # Generate a random filename using UUID
    random_filename = f"{uuid.uuid4().hex}{ext}"

    return random_filename


def save_image(creator, file, filename):
    userDirPath = os.path.join(UPLOAD_DIR, creator)
    # Ensure the upload directory exists
    os.makedirs(userDirPath, exist_ok=True)

    imagePath = os.path.join(userDirPath, filename)
    # Save the file
    file.save(imagePath)


def get_image(creator, file, filename):
    userDirPath = os.path.join(UPLOAD_DIR, creator)
    # Ensure the upload directory exists
    os.makedirs(userDirPath, exist_ok=True)

    imagePath = os.path.join(userDirPath, filename)
    # Save the file
    file.save(imagePath)


def delete_image(creator, filename):
    userDirPath = os.path.join(UPLOAD_DIR, creator)
    # Ensure the upload directory exists
    os.makedirs(userDirPath, exist_ok=True)
    imagePath = os.path.join(userDirPath, filename)
    # Save the file
    os.remove(imagePath)


def delete_user_directory(username):
    userDirPath = os.path.join(UPLOAD_DIR, username)
    if os.path.exists(userDirPath) and os.path.isdir(userDirPath):
        try:
            shutil.rmtree(userDirPath)
            print(f"Successfully deleted directory: {userDirPath}")
        except Exception as e:
            print(f"Error deleting directory {userDirPath}: {e}")


def path_for_image(creator, filename):
    userDirPath = os.path.join(UPLOAD_DIR, creator)
    imagePath = os.path.join(userDirPath, filename)
    return imagePath


def save_temp_image(image_data):
    # Ensure the upload directory exists
    os.makedirs(TEMP_DIR, exist_ok=True)
    # Save the image to the temp folder
    tmp_filename = f"{uuid.uuid4().hex}.png"
    tmp_filepath = os.path.join(TEMP_DIR, tmp_filename)
    with open(tmp_filepath, "wb") as tmp_file:
        tmp_file.write(image_data)

    return tmp_filename
