import os, sys, json, shutil
import argparse
from datetime import date, timedelta, datetime
from pathlib import Path

import crawler
import palantir
from simulator import Simulator, BacktestPredictor

VERSION = "0.0.1"


def rootdir():
    return os.path.dirname(os.path.abspath(__file__))


def structure_check():

    required_files = ["palantir.txt", "callback.py", "config.json"]

    needed_files = [file_ for file_ in required_files if not os.path.exists(file_)]

    for file_ in needed_files:
        shutil.copyfile(
            os.path.join(rootdir(), "defaultfiles", file_),
            os.path.join(os.getcwd(), file_),
        )
        print("Created ", file_)

    print("Palantir structure exists. Moving on...")


def initialize():
    print("Creating and training models...")
    raw_data = palantir.load_data("dataset-btc-hourly")
    palantir.create_models(raw_data, verbose=1)


def backtest(fee=palantir.TRADING_FEE, cash=500):
    print("backtesting models through palantir-simulation...\n")

    clfs = palantir.load_models()
    sim = Simulator(
        palantir.load_data("dataset-btc-hourly")
        .astype(float)
        .drop(["Timestamp"], axis=1),
        BacktestPredictor(
            preceding=palantir.MINIMUM_DATA, time=palantir.MINIMUM_DATA - 1, clfs=clfs
        ),
        cash=cash,
        fee=fee,
    )
    print("\n\n", sim.play(), "\n")

    Path(palantir.COMPLETED_SIMULATIONS_PATH).mkdir(parents=True, exist_ok=True)

    sim_file = os.path.join(
        palantir.COMPLETED_SIMULATIONS_PATH,
        datetime.now().strftime("%d-%H-%M-%S") + ".csv",
    )
    sim.history.to_csv(sim_file)
    print(f"Simulation results saved to '{sim_file}'.\n")


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", "-v", action="version", version=f"palantir {VERSION}"
    )

    help = "Initialize palantir in a folder"
    parser.add_argument("--init", help=help, action="store_true")

    help = "Download historical data for bitcoin"
    parser.add_argument("--get-btc", help=help, action="store_true")

    help = "Test models on built-in simulator"
    parser.add_argument("--backtest", help=help, action="store_true")

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    if args.get_btc:
        print("collecting files...")
        crawler.get_btc(
            "dataset-btc-hourly",
            date.today() - timedelta(days=100),
            date.today(),
            period="Hourly",
            delay=0.001,
        )

    elif args.backtest:
        backtest()

    elif args.init:
        initialize()
    else:
        structure_check()

    print(args)
    return "palantir test"
