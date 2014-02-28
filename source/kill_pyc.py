import glob
import os

if __name__ == "__main__":
    for item in glob.glob(os.path.join(os.getcwd(), "*.pyc")):
        os.remove(item)
