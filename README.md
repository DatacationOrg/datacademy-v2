# Datacademy V2

> This version is currently **under construction**.

The Datacademy Bootcamp is brought to you by Datacation B.V. This repository contains all exercises to test your Data Science skills. As can be seen, the modules above or on the left side correspond to the theoretical part in Easy-LMS. After completing a theoretical part on Easy-LMS you will be asked to open the corresponding files in this repository. Most modules use Notebooks for the exercises. The structure of a Notebook lends itself to add tekst between code cells, which will guide you through the exercises.

However, later modules will mostly be written in actual plain Python files. The reason for this being that some of the functionalities needed are not supported in Notebooks. However after already written some code we suspect that you will not face too much difficulties doing this. Besides, in practice most code you will find and work with will be in plain Python files, making it a good practice.

We wish you good luck, but above all a lot of fun, making your first steps of your data journey!

Best regards, Team Datacation.

## Installation instructions

### Step 0. Install Python (optional)
The Datacademy supports **Python version 3.10 and higher**. If you do not have Python installed, you can simply do so from the [Python website](https://www.python.org/downloads/).

### Step 1. Install and set up the package manager
1. Open this folder in [VS Code](https://code.visualstudio.com/) or your favorite code editor.
2. Open a terminal and execute the following commands:

```bash
# Install/update package manager
python -m pip install --upgrade pip
python -m pip install --upgrade poetry

# Let poetry create a virtual environment
python -m poetry config virtualenvs.create true
python -m poetry config virtualenvs.in-project true
```

### Step 2. Install dependencies
Execute the following commands to install all necessary packages. We call this the dependencies. 

```bash
# This install all dependencies.
python -m poetry install --no-root
```

You should now have a folder called `.venv`. It might not show in your editor, but you can see it in file explorer. These dependencies are specified in `pyproject.toml`, but you don't need to worry about that!

### Step 3. Select the environment as interpreter
In VS Code, use `ctrl+shift+p` and then use `Python: Select Interpreter` to select the virtual environment in `.venv` as the python interpreter. The correct interpreter should look something like:

> Python 3.11.5 ('.venv': Poetry) `.\venv\Scripts\python.exe`

In Notebooks, also select this interpreter at the top right.

**Now, you are good to go!**
