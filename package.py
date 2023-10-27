import logging 
import os
import shutil
import subprocess
import sys
from pathlib import Path
from seeq.addons.udf_ui import __version__
from zipfile import ZipFile

build_logger = logging.getLogger('build')
build_logger.addHandler(logging.StreamHandler())

PARENT_DIR = Path(__file__).resolve().parent
ADDON = "seeq_udf_ui"
custom_env = {"PATH": os.environ.get("PATH")}

subprocess_kwargs = {
    'capture_output': True,
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
        if(not os.path.exists(PARENT_DIR/"temp_folder/")):
            print("Successfully removed temp_folder")
    except FileNotFoundError:
        print("Attempting clean up unnecessary. No temp_folder/ found at: ", temp_folder_path)

    dist_folder=PARENT_DIR/"dist"
    try:
        shutil.rmtree(dist_folder)
        if(not os.path.exists(PARENT_DIR/"dist/")):
            print("Successfully removed dist_folder")
    except FileNotFoundError:
        print("Attempting clean up unnecessary. No temp_folder/ found at: ", dist_folder)

def setup_environment():
    requirements_results = subprocess.run(
        ['pip','install','-r', 'requirements.txt'],
        cwd=PARENT_DIR,
        **subprocess_kwargs
    )

    if requirements_results.returncode:
        log_build_error(build_logger,requirements_results)
        sys.exit(requirements_results.returncode)
        
    print('Environment setup complete')
        

def build_backend(): 
    print("Building the backend")
    build_results = subprocess.run(
        ['python3','setup.py','bdist_wheel'],
        cwd=PARENT_DIR, #only works locally
        **subprocess_kwargs
    )

    if build_results.returncode:
        log_build_error(build_logger,build_results)
        sys.exit(build_results.returncode)
    
    expected_whl_path = PARENT_DIR/('dist/seeq_udf_ui-'+__version__+'-py3-none-any.whl')
    if os.path.exists(expected_whl_path):
        print(".whl generated at: ", expected_whl_path)
    else:
        error_message = "failed to generate: " + str(expected_whl_path)
        raise FileNotFoundError(error_message) 
    
    print('Building backend complete')

def generate_requirements_txt():
    print("Generating backend requirements.txt file")
    path = PARENT_DIR / "temp_folder/add-on-tool/requirements.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    requirements = 'seeq_udf_ui-'+__version__+'-py3-none-any.whl'

    with open(path, 'w') as f:
        f.write(requirements)

    if path.exists():
        print("Successfully generated backend requirements.txt")
    else:
        print("Failed to generate backend requirements.txt")
 
paths = [
    [PARENT_DIR/('dist/seeq_udf_ui-'+__version__+'-py3-none-any.whl'), PARENT_DIR/(('temp_folder/add-on-tool/seeq_udf_ui-'+__version__+'-py3-none-any.whl'))],
    [PARENT_DIR/'seeq/addons/udf_ui/deployment_notebook/UDF_UI_deployment.ipynb',PARENT_DIR/'temp_folder/add-on-tool/UDF_UI_deployment.ipynb'],
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


def zip_items():
    zipName = "seeq-udf-ui-" + __version__ + ".addon"
    print ("Zipping files into", zipName)

    with ZipFile(zipName, 'w') as zip:
        for root, dirs, files in os.walk(PARENT_DIR/'temp_folder', topdown=True):

            for file in files:
                fileName = root + "/"+ file
                fileName = Path(fileName)
                print("filename isS: ", fileName)
                relPath = os.path.relpath(fileName, PARENT_DIR/'temp_folder').replace('\\','/')
                print("Writing: " , relPath)
                relPath = Path(relPath) 
                zip.write(fileName, arcname = relPath)

def create_addonmetadata(): 
    addon_path = PARENT_DIR/ 'addon.json'
    zipName = "seeq-udf-ui-" + __version__ + ".addonmeta"
    with ZipFile(zipName, 'w') as zip: 
        zip.write(addon_path, 
                  arcname='addon.json')

def test_packaging(): 
    print("Testing the seeq-udf-ui package")
    test_results = subprocess.run(
        ['python3','test_package.py'],
        cwd=PARENT_DIR
    )
    if test_results.returncode:
        log_build_error(build_logger,test_results)
        sys.exit(test_results.returncode)
    
if __name__ == "__main__" : 
    cleanup()
    setup_environment()
    build_backend() 
    generate_requirements_txt()
    move_artifacts()
    zip_items()
    create_addonmetadata()
    test_packaging() 