# Xcoin

This is a full implementation of an object orientated blockchain in python.

## Development highlights
- Unspent transaction model
- Proof of work consensus
- Asynchronous peer to peer using twisted
- Testing using Docker Compose

## How to install
1. Make sure you have python 3 installed on your machine
1. Clone desired version to local directory
1. Navigate through terminal to the package directory
1. Create virtual environment 
```python -m virtualenv env```
1. Install dependencies
```pip install -r requirements.txt```
1. Activate virtual enviroment
```source env/bin/activate```
1. Switch to the src directory
```cd src```

### Start your own chain
1. Activate virtual enviroment
```source env/bin/activate```
1. Switch to the src directory
```cd src```
1. Generate your own public/private key pair
```python generate_seed.py```
1. Enter your own 32 character seed at the prompt
1. Create a genesis block
```python genesis.py```
1. Start your node 
```python xcoin.py```

### Join an existing chain
1. Generate your own public/private key pair
```python generate_seed.py```
1. Enter your own 32 character seed at the prompt
1. Add the genesis block from the desired chain to your directory, a ledger.p file
1. Start your node in peer modes with the ip of a known peer
```python xcoin.py -p ip```


## Commands while running xcoin
- **Help**: List available commands
- **Balance**: Display your current balance
- **pow**: Start hashing to create clocks
- **send**: (send value address) Generate a transaction to spend money
- **quit**: Save ledger and shutdown node


