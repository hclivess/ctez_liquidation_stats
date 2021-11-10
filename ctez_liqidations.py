import time
import requests
import json

lookback = 86400*2

def qualify(candidates):
    liquidations_list = []
    for c in candidates:
        if c["body"]["network"] == "mainnet" and (c["body"]["destination"]) == "KT1GWnsoFZVHGh7roXEER3qeCcgJgrXT3de2":
            liquidations_list.append(c["body"]["hash"])
    return liquidations_list


def parse_search():
    ts = int(time.time())
    url = f"https://api.better-call.dev/v1/search?q=liquidate&s={(ts - lookback)}&i=operation"  # week to date
    parsed = requests.get(url).text
    parsed_json = json.loads(parsed)
    return parsed_json["items"]


def parse_operations(hash_list):
    operation_list = []
    for operation in hash_list:
        url = f"https://api.better-call.dev/v1/opg/{operation}"
        parsed = requests.get(url).text
        parsed_json = json.loads(parsed)
        operation_list.append(parsed_json)

    return operation_list


def prettify(liquidations_list):
    liquidation_dict = {}

    for liquidation in liquidations_list:
        try:
            ctez_outstanding_from = (liquidation[0]
            ["storage_diff"]
            ["children"][5]
            ["children"][0]
            ["children"][1]
            ["from"])

            ctez_outstanding_to = (liquidation[0]
            ["storage_diff"]
            ["children"][5]
            ["children"][0]
            ["children"][1]
            ["value"])

            tez_balance_from = (liquidation[0]
            ["storage_diff"]
            ["children"][5]
            ["children"][0]
            ["children"][2]
            ["from"])

            tez_balance_to = (liquidation[0]
            ["storage_diff"]
            ["children"][5]
            ["children"][0]
            ["children"][2]
            ["value"])

            owner = (liquidation[0]
            ["parameters"][0]
            ["children"][0]
            ["children"][1]
            ["value"]
            )

            liquidator = (liquidation[0]
            ["parameters"][0]
            ["children"][2]
            ["value"]
            )

            timestamp = (liquidation[0]
            ["timestamp"]
            )

            hash = (liquidation[0]
            ["hash"])

            ctez_lost = (int(ctez_outstanding_from) - int(ctez_outstanding_to)) / 1000000
            xtz_lost = (int(tez_balance_from) - int(tez_balance_to)) / 1000000

            liquidation_dict[hash] = {
                "ctez_outstanding_from": ctez_outstanding_from,
                "ctez_outstanding_to": ctez_outstanding_to,
                "tez_balance_from": tez_balance_from,
                "tez_balance_to": tez_balance_to,
                "owner": owner,
                "liquidator": liquidator,
                "xtz_lost": xtz_lost,
                "ctez_lost": ctez_lost,
                "timestamp": timestamp
            }
        except Exception as e:
            print(f"Error {e} for {liquidation}")

    return liquidation_dict


def merge_save(data):
    try:
        with open("database.json", "r") as infile:
            indata = json.loads(infile.read())
    except:
        indata = {}
        print("No database file found, creating...")

    merged = {**indata, **data}

    with open("database.json", "w") as outfile:
        outfile.write(json.dumps(merged))


def run():
    candidates = parse_search()
    hashes = qualify(candidates)
    liquidations = parse_operations(hashes)
    nice = prettify(liquidations)
    merge_save(nice)


if __name__ == "__main__":
    while True:
        run()
        time.sleep(360)
