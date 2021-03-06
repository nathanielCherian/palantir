import csv
import os
import numpy as np


def clean(path, verbose=0):

    headers = [
        "Timestamp",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume(BTC)",
        "Volume(Currency)",
        "WeightedPrice",
    ]

    for filename in os.listdir(path):

        with open(os.path.join(path, filename)) as f:
            reader = csv.reader(f, delimiter=",")
            data = np.array(list(reader)[1:]).astype(float)

        for s in set(np.where(data == 1.70000000e308)[0]):
            data[s] = data[s - 1]
            with open(os.path.join(path, filename), mode="w", newline="") as data_file:
                writer = csv.writer(data_file)
                writer.writerow(headers)
                writer.writerows(data)


            if verbose > 0:
                print("replaced in ", filename)
    if verbose > 0:
        print("Done!")
