import logging 
import os
import shutil
import subprocess
import sys
from pathlib import Path
from seeq.addons.udf_ui import __version__

build_logger = logging.getLogger('build')
build_logger.addHandler(logging.StreamHandler())

PARENT_DIR = Path(__file__).resolve().parent
ADDON = "seeq_udf_ui"
custom_env = {"PATH": os.environ.get("PATH")}

subprocess_kwargs = {
    'capture_output': True,
    'shell': True
}


def log_build_error(logger, results):
    logger.error(
        results.stderr.decode('utf-8')
        if results.stderr
        else f'Error running build script for {ADDON}'
    )

def cleanup():
    temp_folder_path = PARENT_DIR/"temp_folder"
    try:
        shutil.rmtree(temp_folder_path)
        if(not os.path.exists("temp_folder/")):
            print("Successfully removed temp_folder")
    except FileNotFoundError:
        print("Attempting clean up unsuccessful. No temp_folder/ found at: ", temp_folder_path)

def setup_environment():
    requirements_results = subprocess.run(
        ['pip','install','-r', 'requirements.txt'],
        **subprocess_kwargs
    )

    if requirements_results.returncode:
        log_build_error(build_logger,requirements_results)
        sys.exit(requirements_results.returncode)
        
    print('Environment setup complete')
        

def build_backend(): 
    build_results = subprocess.run(
        ['python','setup.py','bdist_wheel'],
        **subprocess_kwargs
    )

    if build_results.returncode:
        log_build_error(build_logger,build_results)
        sys.exit(build_results.returncode)
        
    print('Building backend complete')

#TODO: add version numbers 
paths = [
    [PARENT_DIR/'requirements.txt',PARENT_DIR/'temp_folder/data-lab-functions/requirements.txt'],
    [PARENT_DIR/('dist/seeq_udf_ui-'+__version__+'-py3-none-any.whl'), PARENT_DIR/(('temp_folder/data-lab-functions/seeq_udf_ui-'+__version__+'-py3-none-any.whl'))],
    [PARENT_DIR/'seeq/addons/udf_ui/deployment_notebook/UDF_UI_deployment.ipynb',PARENT_DIR/'temp_folder/data-lab-functions/UDF_UI_deployment.ipynb'],
    [PARENT_DIR/ 'addon.json',PARENT_DIR/'temp_folder/addon.json']
]

def move_artifacts():
    build_logger.info("Moving artifacts into .addon directory:")
    for artifact in paths:
        print("Copying ,", artifact[0],"to ", artifact[1])
        current_path = artifact[0]
        new_path = artifact[1]
        if current_path.is_dir():
            shutil.copytree(str(current_path), str(new_path))
        else:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(str(current_path), str(new_path))

        if new_path.exists():
            build_logger.info(f"\t{current_path} moved successfully to {new_path}")
        else:
            build_logger.error(f'\t{current_path} failed to move to {new_path}')

def zip_artifacts(): 
    print("HI there")

def test_packaging(): 
    print("HI there")

if __name__ == "__main__" : 
    cleanup()
    setup_environment()
    build_backend() 
    move_artifacts()
    zip_artifacts()
    test_packaging() 
