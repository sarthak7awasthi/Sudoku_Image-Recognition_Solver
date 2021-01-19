# Sudoku_Solver

This is a web application which allows users to input a sudoku board. The web app uses Python OpenCV to adjust the images; TensorFlow to predict the digits in sudoku board; and backtracking algorithm to solve the obtained sudoku board.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Python3.7, pip, Flask, OpenCV, TensorFlow
You can download and find the instructions to install them through these links:

* [Python3](https://www.python.org/downloads/)
* [Pip](https://pip.pypa.io/en/stable/installing/)
* [Flask](https://pypi.org/project/Flask/)
* [OpenCV](https://pypi.org/project/opencv-python/)
* [TensorFlow](https://pypi.org/project/tensorflow/)

### Installing
To install the other necessary packages: 
* Navigate to the repository on your terminal
* Install all other dependencies:
```bash
pip install -r requirements.txt
```
** In case of failure of above command due to version mismatch of any dependency, comment out the particular dependency in 'requirements.txt' and install manually using the command below and re run the above command:
```bash
pip install <failed-dependency-name>
```

## Running the project and using the app

* Navigate to the project directory
* Then run the flask server:
```bash
python __init__.py
```
* Open any browser and go to localhost:5000/
* Upload any .jpg image of any unsolved sudoku board
