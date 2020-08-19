import os, sys, json, shutil
import argparse
from datetime import date, timedelta, datetime
from pathlib import Path
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.key_binding import KeyBindings
import yaml

import crawler
import palantir
from simulator import Simulator, BacktestPredictor

VERSION = "0.0.1"


def rootdir():
    return os.path.dirname(os.path.abspath(__file__))


def structure_check():

    required_files = ["palantir.txt", "callback.py", "config.yml"]

    required_configs = ["name", "security"]

    needed_files = [file_ for file_ in required_files if not os.path.exists(file_)]

    for file_ in needed_files:
        shutil.copyfile(
            os.path.join(rootdir(), "defaultfiles", file_),
            os.path.join(os.getcwd(), file_),
        )
        print("Created ", file_)

    with open("config.yml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        data = data if data else {}
        not_in = [c for c in required_configs if c not in data.keys()]
        if not_in:
            print("Incorrect palantir config.yml ")
            sys.exit(1)

    print("Palantir structure exists. Moving on...")
    return data


def initialize(path):
    print("Creating and training models...")
    raw_data = palantir.load_data(path)
    palantir.create_models(raw_data, verbose=1)


def backtest(path, fee=palantir.TRADING_FEE, cash=500):
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
    parser.add_argument("--init", help=help, action="store")

    help = "Download historical data for bitcoin"
    parser.add_argument("--get-btc", help=help, action="store")

    help = "Test models on built-in simulator"
    parser.add_argument("--backtest", help=help, action="store")

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    if args.get_btc:
        print("collecting files...")
        crawler.get_btc(
            args.get_btc,
            date.today() - timedelta(days=100),
            date.today(),
            period="Hourly",
            delay=0.001,
        )

    elif args.backtest:
        backtest(args.backtest)

    elif args.init:
        initialize()

    else:

        clear()
        clear()

        with open(os.path.join(rootdir(), "defaultfiles", "palantir.txt")) as f:
            logo = [line for line in f][:9]
            print("\n\n", "".join(logo))
            print("\n                                           By Nathaniel Cherian\n")

        session = PromptSession()

        config_data = structure_check()
        if config_data["name"]:
            print(f"Loaded instance named '{config_data.get('name', 'unnamed')}'")
        else:
            print("\nEnter a name for this palantir instance")
            text = session.prompt("PALANTIR> ")
            config_data["name"] = text

            with open("config.yml", "w") as f:
                yaml.dump(config_data, f, default_flow_style=False)
            print(f"Instance named {text}!\n")

        text = [""]
        while text[0] != ("exit", "exit()"):
            text = session.prompt("PALANTIR> ").split()
            if len(text) is 0:
                text.append("")

            if text[0] == "help":
                print("Commands: ")
                print(
                    "collects historical hourly bitcoin data. usage: get-btc [directory:str] [days:int]"
                )
                print("Initialize palantir in a folder. usage: init [directory:str]")

            elif text[0] == "get-btc":

                if len(text) < 3 or text[1] == "help":
                    print(
                        "collects historical hourly bitcoin data. usage: get-btc [directory:str] [days:int]"
                    )
                else:
                    print("collecting bitcoin data")
                    try:
                        crawler.get_btc(
                            text[1],
                            date.today() - timedelta(days=int(text[2])),
                            date.today(),
                            period="Hourly",
                            delay=0.001,
                        )
                    except:
                        "Failed! Check your inputs!"

            elif text[0] == "init":

                if len(text) < 2 or text[1] == "help":
                    print(
                        "Initialize palantir in a folder. usage: init [data-directory:str]"
                    )
                else:

                    try:
                        initialize(text[1])
                    except:
                        "Failed! Check your inputs!"

            else:
                print("Command not found!")

    print(args)
