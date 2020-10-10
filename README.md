# Getting started
### Clone the repo
Clone the repository https://github.com/amd1250x/GroceryListApp to your local Github directory.
### Setup a Python virtual environment (venv) and modify .gitignore
Ensure that you have Python installed (v3 is best). Then, open either Windows Command Line or Windows Powershell.

Navigate to the cloned Github repo using cd and run
```py -m venv my_virtual_environment```

Then open the .gitignore file and add
```
my_virtual_environment/*
```

### Activate the virtual environment and install requirements

Navigate to my_virtual_environment\Scripts

* If using Command Line, run
```activate```

* If using Powershell, run
```.\activate.ps1```
If you received a system error, re-open Powershell as administrator, and run
``` Set-ExecutionPolicy Unrestricted```
Then try running ```.\activate.ps1``` again

Navigate back to your GitHub project using cd ..\\..

Install the requirements file with ```pip install -r requirements.txt```. This may take a few minutes.

### Run Django methods to create local test server

Run ```py manage.py makemigrations```. If an option list for (1) or (2) shows, select (1) by typing and entering 1. Then type and enter 1 again. If the same prompt shows up again, repeat the steps once more.

Run ```py manage.py migrate```

Run ```py manage.py runserver```

Open your web browser of choice and enter the local server URI. It will likely be http://127.0.0.1:8000/

Enjoy!
