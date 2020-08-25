import os, sys, json, shutil
import argparse
from datetime import date, timedelta, datetime
from pathlib import Path
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from ast import literal_eval
import yaml
import requests
import crawler
import palantir
from simulator import Simulator, BacktestPredictor
import schedule
import pandas as pd

VERSION = "0.1.0"


def rootdir():
    return os.path.dirname(os.path.abspath(__file__))


def structure_check():

    required_files = ["palantir", "callback.py", "config.yml"]

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
    assert os.path.exists(path), print("Path does not exist!")

    print("Creating and training models...")

    raw_data = palantir.load_data(path)
    assert len(raw_data) > 200, print("Skipping. Dataset is too small.")
    palantir.create_models(raw_data, verbose=1)




def backtest(path, fee=palantir.TRADING_FEE, cash=500, bitcoin=1, save=None):

    assert os.path.exists(path), print("Path does not exist!")

    print("backtesting models through palantir-simulation...\n")

    clfs = palantir.load_models()
    sim = Simulator(
        palantir.load_data(path).astype(float).drop(["Timestamp"], axis=1),
        BacktestPredictor(
            preceding=palantir.MINIMUM_DATA, time=palantir.MINIMUM_DATA - 1, clfs=clfs
        ),
        cash=cash,
        fee=fee,
        bitcoin=bitcoin,
    )

    sim.play()

    Path(palantir.COMPLETED_SIMULATIONS_PATH).mkdir(parents=True, exist_ok=True)

    name = datetime.now().strftime("%d-%H-%M-%S") if not save else save
    sim_file = os.path.join(palantir.COMPLETED_SIMULATIONS_PATH, name + ".csv",)

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
        initialize(args.init)

    else:

        clear()
        clear()

        with open(os.path.join(rootdir(), "defaultfiles", "palantir")) as f:
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
        while text[0] not in ["exit", "exit()"]:

            dir_files = {f.name for f in os.scandir(os.getcwd()) if f.is_dir()}

            completer = NestedCompleter.from_nested_dict(
                {
                    "get-btc": None,
                    "init": dir_files,
                    "backtest": dir_files,
                    "rename": None,
                    "callback": None,
                    "live-btc":None,
                }
            )

            text = session.prompt("PALANTIR> ", completer=completer, complete_in_thread=True).split()
            if len(text) == 0:
                text.append("")

            kwargs = (
                {}
            )  # I will soon implement a regex based solution for literal kwarg evals
            for i, t in enumerate(text):
                index = t.find("=")

                if t == "=":
                    kwargs[text[i - 1]] = literal_eval(text[i + 1])
                elif index != -1:
                    kwargs[t[:index]] = literal_eval(t[index + 1 :])

            if text[0] == "help":
                print("Commands: ")
                print(
                    "collects historical hourly bitcoin data. usage: get-btc [directory:str] [days:int]"
                )
                print("Initialize palantir in a folder. usage: init [directory:str]")

            elif text[0] == "get-btc":

                if len(text) < 2 or text[1] == "help":
                    print(
                        "collects historical hourly bitcoin data. usage: get-btc *[directory:str] **[days:int]"
                    )

                else:
                    print("collecting bitcoin data")
                    try:
                        crawler.get_btc(
                            text[1],
                            date.today() - timedelta(days=int(kwargs.get("days", 50))),
                            date.today(),
                            period=kwargs.get("period", "Hourly"),
                            delay=0.001,
                        )

                        crawler.clean(text[1])

                    except:
                        "Failed! Check your inputs!"

            elif text[0] == "init":

                if len(text) < 2 or text[1] == "help":
                    print(
                        "Initialize palantir in a folder. usage: init *[data-directory:str]"
                    )
                else:

                    try:
                        initialize(text[1])
                    except:
                        "Failed! Check your inputs!"

            elif text[0] == "backtest":

                if len(text) < 2 or text[1] == "help":
                    print(
                        "Backtest model with historical data. usage: backtest *[data-directory:str] **[sim-results-filename:str]"
                    )

                else:

                    try:
                        backtest(text[1], **kwargs)
                    except:
                        "Failed! Check your inputs!"

            elif text[0] == "rename":

                if len(text) < 2:
                    print("Rename palantir instance. usage: rename *[new_name:str]")

                else:

                    config_data["name"] = text[1]
                    with open("config.yml", "w") as f:
                        yaml.dump(config_data, f, default_flow_style=False)
                        print(f"Instance renamed {text[1]}!")


            elif text[0] == 'live-btc':
                print("You are now starting live predictions using the palantir instance of ", config_data['name'])

                """
                Part 1: Collect preceding data to create processed data
                Part 2: Get new datapoint from api

                """

                if kwargs.get('skip1', None):

                    print("collecting necessary data...")
                    crawler.get_btc(
                        "livedata",
                        date.today() - timedelta(days=int(9)),
                        date.today() + timedelta(days=3),
                        period="Hourly",
                        delay=0.001,
                    )
                    crawler.clean("livedata", verbose=0)

                    with open("config.yml", "w") as f:
                        config_data["last-update"] = "now"
                        yaml.dump(config_data, f, default_flow_style=False)
                


                # Get user-defined functions
                with open("callback.py", "r") as f:
                    s = f.read()
                callbacks = {}
                exec(s, callbacks)
                live_data = callbacks["security_api"]()
                
                pd.DataFrame({"Open":live_data["price"]})

                pre_data = palantir.load_data('livedata').reset_index(drop=True)




            elif text[0] == "callback":

                with open("callback.py", "r") as f:
                    s = f.read()

                dd = {}
                exec(s, dd)
                print(dd["callback"]((1, 2)))
            
            elif text[0] == "version":
                print("palantir-cli " ,VERSION)

            elif text[0] in ["exit", "exit()"]:
                break
            elif text[0] in ["cls", "clear"]:
                clear()

            elif not text[0]:
                pass
            else:
                print("Command not found!")

    # print(args)
