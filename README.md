# Stock Analysis Tool

## Setup

### Prerequisites

* Must have python3 installed with venv support (typically included within
  the python3 installation).
  * Use your system's package manager or download directory: https://www.python.org/downloads/
* Alpha Vantage API Key (Free)
  * Sign up here: https://www.alphavantage.co/support/#api-key
  * Key limitations are 5 requests per minute, 500 per day.

### Setup Commands

* Commands assume your are on a **unix environment** using bash.

```
# Setups virtual environment folder.
mkdir .venv             

# Installs barebones for virtualenvironment: a python and pip executable etc.
python3 -m venv .venv   

# Installs project dependencies.
pip install -r requirements

# Activates current terminal to be isolated within virtual environment.
# Must be done everytime a new terminal is used for the project unlike
# the previous three commands.
source .venv/bin/activate
```

## Running

To generate excel sheets with metrics run
`python3 main.py <space seperated tickers>`

Each ticker will take 1 minute to generate a report due to AlphaVantage API
request limitations.