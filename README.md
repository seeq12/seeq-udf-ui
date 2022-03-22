# User Interface for User-Defined Formula Functions


User-Defined Formula Function User Interface (UDF UI) is a Seeq Add-On that allows users to manage UDFs. This includes creating new UDFs, 
modifying existing ones, modifying access control, or deleting existing user defined functions and packages. 

![drawing](https://github.com/seeq12/seeq-udf-ui/blob/main/docs/_static/overview.png?raw=true)

----
# Installation

### User Installation Requirements (Seeq Data Lab)
If you want to install **seeq-udf-ui** as a Seeq Add-on Tool, you will need a version of Seeq Data Lab:

- Seeq Data Lab (> R50.5.0, >R51.1.0, or >R52.1.0)
- Seeq module whose version matches the Seeq server version, and the version of SPy >= 182.25
- Seeq server admin access


### User Installation (Seeq Data Lab)
1. Create a **new** Seeq Data Lab project, and open the terminal window.

2. Run `pip install seeq-udf-ui` 
3. (if you would like to install a version not on PyPi, `pip install` a local `.whl`
file)

4. Run `python -m seeq.addons.udf_ui [--users <users_list> --groups <groups_list>]`.  During the installation you will
   be prompted for your username/password (an access key can also be used).  It will also prompt for the url of the
   app notebook which will be available from the deployment folder in Seeq Data Lab.

5. Verify that the UDF UI add-on is present in the AddOn menu in workbench.

### Source Installation

For development work, after checking out the code from repository, 
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

----

# Development

We welcome new contributors of all experience levels.

- Official Source code repository : https://github.com/seeq12/seeq-udf-ui

- Issue tracker : https://github.com/seeq12/seeq-udf-ui/issues

You can get started by cloning the repository with the command : 

```sh

$ git clone git@gitub.com:seeq12/seeq-udf-ui.git

```
For development work, after checking out the code from repository, 
it is highly recommended you create a python virtual environment, 
`pip install -r requirement.txt`, and install the package in that
working environment. 

There is a template for the developer notebook in /development. 

Next, modify the parameters within the workbook for your local environment (username, password, workbook, worksheet, etc.).

Finally, start a jupyter server and navigate to the development notebook in the root directory.

```sh

$ jupyter notebook

```

Documentation can be updated by editing the source files in docs/src/source, and then using the provided bat file to
generate the documentation in the docs folder, i.e., from the docs/src folder:

```sh

$ make github

```


# Important links

* Official source code repo: https://github.com/seeq12/seeq-udf-ui

* Official documentation : https://seeq12.github.io/seeq-udf-ui/

* Change Log : https://seeq12.github.io/seeq-udf-ui/changelog.html

* Issue tracker (bugs, feature requests, etc.) : https://github.com/seeq12/seeq-udf-ui/issues

----

# Citation

Please cite this work as:

```shell
seeq-udf-ui
Seeq Corporation, 2022
https://github.com/seeq12/seeq-udf-ui
```

----
# Version compatibility notes


As of Seeq R54, archived formula functions and packages cannot be found in the Workbench Formula 
editor, whereas prior to R54 they can still be found.
