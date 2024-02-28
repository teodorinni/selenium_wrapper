import os
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv(dotenv_path="launch_params.env")
    test_folders = [folder_name.strip() for folder_name in os.getenv("TEST_FOLDERS").split(",")]
    test_files = [file_name.strip() for file_name in os.getenv("TEST_FILES").split(",")]
    num_threads = int(os.getenv("NUM_THREADS"))
    path_string = f"{' '.join(test_folders)} {' '.join(test_files)}"
    if num_threads <= 1:
        script = f"pytest {path_string}"
    else:
        script = f"pytest -n{num_threads} --dist=loadfile {path_string}"
    os.system(script)
