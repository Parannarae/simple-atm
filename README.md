# Simple ATM
A conceptual controller implementation for ATM machine which does very simple things such as get balance, deposit, and withdraw from an account associated with a card.

## Step to build an environment
### Basic Python
- Install Python3 (>=3.8)
- (if not installed with python) Install pip

### Project Environment
```bash
# install pipenv
python3 -m pip install pipenv
# setup environment
python3 -m pipenv install
```

## Run Test
- Start the virtualenv
```bash
# startup virtualenv
python3 -m pipenv shell
```
- Run Test
```bash
python -m tests.test_atm
```