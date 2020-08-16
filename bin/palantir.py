import os, sys, json, shutil
import argparse
from datetime import date, timedelta

import crawler
import palantir
from simulator import Simulator, BacktestPredictor

VERSION = '0.0.1'

def rootdir():
    return os.path.dirname(os.path.abspath(__file__))

def structure_check():

    required_files = ['palantir.txt', 'callback.py', 'config.json']

    needed_files = [file_ for file_ in required_files if not os.path.exists(file_)]

    for file_ in needed_files:
        shutil.copyfile(os.path.join(rootdir(), 'defaultfiles', file_), os.path.join(os.getcwd(), file_))
        print('Created ', file_)

    print('Palantir structure exists. Moving on...')

def initialize():
    print('Creating and training models...')
    raw_data = palantir.load_data('dataset-btc-hourly')
    palantir.create_models(raw_data, verbose=1)


def backtest():
    print("backtesting models through palantir-simulation...")

    clfs = palantir.load_models()
    sim = Simulator(palantir.load_data('datasets').astype(float).drop(['Timestamp'], axis=1), 
                    BacktestPredictor(preceding=200, time=199, clfs=clfs), 
                    cash=500, fee=0.0026)
    sim.play()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v', action='version',
                        version=f"palantir {VERSION}")

    help = "Download historical data for bitcoin"
    parser.add_argument('get-btc', help=help)

    if len(sys.argv)==1:
        structure_check()
        initialize()
        backtest()
        sys.exit(0)

    args = parser.parse_args()

    return args

def main():
    

    args = parse_args()

    if 'get-btc' in args:
        print("collecting files...")
        crawler.get_btc('dataset-btc-hourly', date.today()-timedelta(days=100), date.today(), period='Hourly', delay=0.001)


    print(args)
    return "palantir test"