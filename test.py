from brownie import Contract , accounts, network
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    account = accounts.add("de7ec9aebd67f83943a0c9e5c7e8db3067bc5aa47837729fe24e328679ced13f")
    #network.connect('rinkeby')
    token = Contract('0x2d6b682F7a726aF7130a0E391Ab1Bb611fC33759')
    print(token.display('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', 30, "New York1", {"from":account}))
    # network.disconnect()

main()