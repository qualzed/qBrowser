import argparse
from qb import debug

def CheckArguments():
    parser = argparse.ArgumentParser(description="Example")
    parser.add_argument('-d', '--debug', action='store_true', help='Turn on/off debug')

    args = parser.parse_args()

    if args.debug:
        debug.debug_bool = True
        print("Browser in debug mode has been started")
    else:
        debug.debug_bool = False