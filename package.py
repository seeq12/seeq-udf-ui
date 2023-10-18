import logging 
import os
import shutil
import subprocess
import sys
from artifactory import ArtifactoryPath
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
    # 'shell': True,
    # 'stdout':subprocess.PIPE
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
    print("here is parent dir: ", PARENT_DIR)
    build_results = subprocess.run(
        # ['setup.py','bdist_wheel'],
        # ['python3','setup.py','bdist_wheel'],
        ['pwd'],
        text=True,
        cwd=PARENT_DIR, #only works locally
        **subprocess_kwargs
    )
    print(build_results)

    build_results = subprocess.run(
        # ['setup.py','bdist_wheel'],
        ['python3','setup.py','bdist_wheel'],
        # ['poetry', 'build'],
        cwd=PARENT_DIR, #only works locally
        **subprocess_kwargs
    )

    print(build_results)
    if build_results.returncode:
        log_build_error(build_logger,build_results)
        sys.exit(build_results.returncode)

    print("Checking if dist/ exists")
    dist_path = PARENT_DIR/('dist')
    print("Checking if this works: ")
    if os.path.exists(dist_path):
        print("dist/ confirmed to exist at: ", dist_path)
    else:
        error_message = "failed to generate: " + str(dist_path)
        raise FileNotFoundError(error_message) 
    
    expected_whl_path = PARENT_DIR/('dist/seeq_udf_ui-'+__version__+'-py3-none-any.whl')
    if os.path.exists(expected_whl_path):
        print(".whl file confirmed to exist at: ", expected_whl_path)
    else:
        error_message = "failed to generate: " + str(expected_whl_path)
        raise FileNotFoundError(error_message) 
    print('Building backend complete')

def generate_requirements_txt():
    print("Generating backend requirements.txt file")
    path = PARENT_DIR / "temp_folder/data-lab-functions/requirements.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    requirements = 'seeq_udf_ui-'+__version__+'-py3-none-any.whl'

    with open(path, 'w') as f:
        f.write(requirements)

    if path.exists():
        print("Successfully generated backend requirements.txt")
    else:
        print("Failed to generate backend requirements.txt")

#TODO: add version numbers 
paths = [
    # [PARENT_DIR/'requirements.txt',PARENT_DIR/'temp_folder/data-lab-functions/requirements.txt'],
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
                relPath = Path(relPath) #to fix build agent shenanigans 
                zip.write(fileName, arcname = relPath)

def create_addonmetadata(): 
    addon_path = PARENT_DIR/ 'addon.json'
    zipName = "seeq-udf-ui-" + __version__ + ".addonmeta"
    with ZipFile(zipName, 'w') as zip: 
        zip.write(addon_path, 
                  arcname='addon.json')

def test_packaging(): 
    print("HI there")

addon_manager_artifacts = [PARENT_DIR/("seeq-udf-ui-" + __version__ + ".addonmeta"),
                           PARENT_DIR/("seeq-udf-ui-" + __version__ + ".addon")]

def deploy_artifacts(): 
    print(f'Distributing addon manager artifacts to seeq.jfrog.io')
    api_key = os.getenv('JFROG_API_KEY')
    if api_key is not None: 
        print("We got the key!")
    for artifact in addon_manager_artifacts:
        _, file = os.path.split(artifact)
        print("We're deploying this: ", file, "and this is the original file path: ", artifact)
        # jfrog_repo_url="https://seeq.jfrog.io/artifactory/seeq-add-ons-dev-local"
        # jfrog_file_path = f"UDFEditor/{file}"
        # jfrog_repo_url="https://seeq.jfrog.io/artifactory/seeq-add-ons-dev-local"
        jfrog_file_path = f"https://seeq.jfrog.io/artifactory/seeq-add-ons-dev-local/UDFEditor/{file}"
        print("Before path")
        path = ArtifactoryPath(jfrog_file_path, apikey=api_key)
        print("After path: ", path)
        try:
            if(not os.path.exists(artifact)):
                print("Ha yeah it doesn't exist")
            else:
                print("I mean we found it idk")
            path.deploy_file(artifact)
            print("We have deployed artifact")
            properties = path.properties
            # Add identifier property
            properties["identifier"] = "com.seeq.addons.udf_ui"
            print("Setting properties")
            path.properties = properties
            print("Done with properties")
        except Exception as e:
            print(e)


if __name__ == "__main__" : 
    cleanup()
    setup_environment()
    build_backend() 
    generate_requirements_txt()
    move_artifacts()
    zip_items()
    create_addonmetadata()
    test_packaging() 
    # deploy_artifacts()
