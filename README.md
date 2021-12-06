# Advent of Code 2021
This repository consists of my solutions for the advent of code 2021 problems.

## Usage

- Each day's solution is in the corresponding folder, ingeniously named 'dayx' where 'x' is the day number, in a file called `main.py`
- To run the solution go to that folder and run the `main.py` file as follows:

```
$python main.py -f <location of your inputs>
```

- My specifc inputs are also provided for each day, to run on those, use the following:

```
$python main.py
```

## Requirements
Create a conda environment or use pipenv or whatever. For conda do the following:
```
conda create --name <virtual env name> python=3.8
conda activate <name of virtual environment>
conda install --file requirements.txt
```
or just do `make install` from the parent directory.