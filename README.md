<div align="center">
    <img src="https://raw.githubusercontent.com/Jobsity/ReactChallenge/main/src/assets/jobsity_logo_small.png"/>
    <h1>Stock Quote API</h1>
</div>


## Description
This project is a Flask-based API that allows registered users to query stock quotes. It consists of two separate services: a user-facing API and an internal stock aggregator service.

## Requirements
* [Python 3.10.12+](https://www.python.org/downloads/release/python-31012/)
* [Git](https://git-scm.com/downloads)
* Recommended tools for making API requests: Curl, Postman, or [Insomnia](https://github.com/Kong/insomnia/releases/latest).

## Architecture
![Architecture Diagram](diagram.svg)
1. A user makes a request asking for Apple's current Stock quote: `GET /stock?q=aapl.us`
2. The API service calls the stock service to retrieve the requested stock information
3. The stock service delegates the call to the external API, parses the response, and returns the information back to the API service.
4. The API service saves the response from the stock service in the database.
5. The data is formatted and returned to the user.


## Getting started

1. Clone the repository:

```sh
git clone https://git.jobsity.com/roman_mor/flask-challenge.git
```
2. Navigate to the cloned directory:
```sh
cd flask-challenge
```
2. Create a virtual environment and activate it:
```sh
python -m venv virtualenv
. virtualenv/bin/activate
```
3. Install project dependencies: 
```sh
pip install -r requirements.txt
```
4. Start the stock aggregator service: 
```sh
cd stock_service ; flask run
```
5. On a separate terminal session, start the API service: 
```sh
cd api_service ; flask init; flask db migrate; flask db upgrade ; flask run
```

## Available users

* Normal user:`(username : password)`
    ```
    johndoe : john 
    ```
* Admin user:`(username : password)`
    ```
    admin : admin 
    ```
## API Endpoints

### GET /stock

Fetches data for a specific stock.

**Authorization:**
This endpoint requires Basic Authentication.

**Query Parameters:**
- `q`: The stock symbol to fetch data for.

**Response:**
The stock data for the requested stock. This includes properties such as:
- `symbol`: The symbol of the stock.
- `company_name`: The name of the company requested.
- `quote`: The closing price of the stock

**Example:**
```bash
curl -u username:password "http://localhost:5000/stock?q=aapl.us"
```

### GET /stats

Fetches the top 5 most queried stocks. 

**Authorization:**
This endpoint requires Basic Authentication and is only accessible to users with admin privileges.

**Response:**
A list of the top 5 most queried stocks, each with the following properties:
- `stock`: The symbol of the stock.
- `time_requested`: The number of times the company has been requested.


**Example:**
```bash
curl -u username:password http://localhost:5000/stats
```

### GET /users/history

Fetches the history of stock queries made by the current user.

**Authorization:**
This endpoint requires Basic Authentication.

**Response:**
A list of stock query entries made by the current user, each with the following properties:
- `date`: The date and time when the stock data was requested.
- `name`: The name of the company.
- `symbol`: The symbol of the stock.
- `open`: The opening price of the stock for the day.
- `high`: The highest price of the stock for the day.
- `low`: The lowest price of the stock for the day.
- `close`: The closing price of the stock for the day.

**Example:**
```bash
curl -u username:password "http://localhost:5000/users/history"
```