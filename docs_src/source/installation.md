# Installation

The backend of **seeq-udf-ui** requires **Python 3.7** or later.

## Dependencies

See [`requirements.txt`](https://github.com/seeq12/seeq-udf-ui/tree/main/requirements.txt) file for a list of
dependencies and versions. Additionally, you will need to install the `seeq` module with the appropriate version that
matches your Seeq server. For more information on the `seeq` module see [seeq at pypi](https://pypi.org/project/seeq/)

## User Installation Requirements (Seeq Data Lab)

If you want to install **seeq-udf-ui** as a Seeq Add-on Tool, you will need:

- Seeq Data Lab (>= R50.5.0, >=R51.1.0, or >=R52.1.0)
- `seeq` module whose version matches the Seeq server version
- `spy` version >= 182.25
- Seeq administrator access
- Enable Add-on Tools in the Seeq server

## User Installation (Seeq Data Lab)

The latest build of the project can be found [here](https://pypi.org/project/seeq-udf-ui/) as a wheel file. The
file is published as a courtesy to the user, and it does not imply any obligation for support from the publisher.

1. Create a **new** Seeq Data Lab project and open the **Terminal** window
2. Run `pip install seeq-udf-ui`
3. Run `python -m seeq.addons.udf_ui [--users <users_list> --groups <groups_list>]`

## Developer Installation 

For development work, after checking out the code from the repository, 
it is highly recommended you create a python virtual environment, 
`pip install -r requirement.txt`, and install the package in that
working environment. If you are not familiar with python virtual environments,
it is recommended you take a look [here](https://docs.python.org/3.8/tutorial/venv.html).

Once your virtual environment is activated, you can install **seeq-udf-ui** from source with:

```shell
python setup.py install
```

Or build a `.whl` file using the following command 
```shell
python setup.py bdist_wheel
```
and then `pip install [FILE NAME].whl`
(the `wheel` file name can change depending on the version).

There is a template for the developer notebook in `/development`. 
Next, modify the parameters within the workbook for your local environment (username, password, workbook, worksheet, etc.).
Finally, start a jupyter server and navigate to the development notebook in the root directory.

```sh

$ jupyter notebook

```
Please note that running the tests requires administrative priviledge in the running Seeq instance.

Documentation can be updated by editing the source files in `docs_src/` then using the provided 
bat file (which runs sphinx) to generate the documentation in the docs folder, i.e.:

Using the bat file:
```sh

$ make.bat github

```
or using `Makefile`:

```sh

$ make github

```


