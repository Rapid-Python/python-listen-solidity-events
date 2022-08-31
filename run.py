from flask import Flask
from web3 import Web3
import asyncio
from brownie import network, Contract
import os
from dotenv import load_dotenv

app = Flask(__name__)


# Load environment variables
load_dotenv()

# Create Infura Connection
# define "INFURA_PROVIDER" in your .env file
web3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/90e863301f6a4d09b679359653e18378'))

# contract Address
contractAddress = '0xd9145CCE52D386f254917e481eB44e9943F39138'

# Connect to rinkeby network
# doing this step just to read the Contract abi
# file but you can read the abi file manually with web3. py as well

try:
    network.connect('rinkeby')
except Exception as e:
    print(e)

token = Contract(contractAddress)

contract = web3.eth.contract(address=contractAddress, abi=token.abi)

# define function to handle events and print to the console
# You can also setup any action after listening to the event
def handle_event(event):
    print(Web3.toJSON(event))


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.showData.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    app.run(debug= True)