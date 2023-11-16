# Levi9 5 Days in Cloud Challenge | Player Performance Tracker

## Environment Setup

To build and run this project, you need to have the following environment setup:

- Python 3.11
- Django 4.2.7
- Django REST Framework 3.14.0
- Django CORS Headers 4.3.0

## Build Instructions

1. Install poetry, a dependency management tool for python. You can install it using pip:

```bash
pip install poetry
```

2. Clone the repository and navigate to the project directory.
   
```bash
git clone https://github.com/ssspetrovic/l9-cloud-challenge-2023.git && cd 9-cloud-challenge-2023
```
3. Install the project dependencies:

```bash
poetry install
```

## Running the Application

To run the application:
1. Place the .csv file inside of the ./player_performance_tracker/stats_api/data folder and update the **FILE_NAME** accordingly inside of DataService class

```bash
cp file_name.csv CLONE_LOCATION/l9-cloud-challenge-2023/player_performance_tracker/stats_api/data
```
   
3. Activate the poetry shell
   
```bash
poetry shell
```

3. Run the server

```bash
python player_performance_tracker/manage.py runserver
```
## Technologies Used

- **Python**: A high-level, interpreted programming language with dynamic semantics.
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework**: A powerful and flexible toolkit for building Web APIs in Django.
- **Django CORS Headers**: A Django App that adds Cross-Origin Resource Sharing (CORS) headers to responses. This allows in-browser requests to your Django application from other origins.
- **Poetry**: A tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.
