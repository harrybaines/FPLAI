import requests
import json
import pandas as pd
import numpy as np

FPL_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


def main():
    req = requests.get(FPL_URL)
    res_json = req.json()

    elements_df = pd.DataFrame(json["elements"])
    elements_types_df = pd.DataFrame(json["element_types"])
    teams_df = pd.DataFrame(json["teams"])

    print(elements_df.head())


if __name__ == "__main__":
    main()