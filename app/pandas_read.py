from genericpath import exists
from importlib.resources import path
import pandas as pd
import os


def read_intern_billing(data_name):
    if not os.path.exists(data_name):
        print("沒有這個檔案")
        exit()
    df = pd.read_csv(data_name)
    return df
