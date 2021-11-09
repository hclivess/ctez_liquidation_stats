import time
import requests
import json


def qualify(candidates):
    liquidations_list = []
    for c in candidates:
        if c["body"]["network"] == "mainnet" and (c["body"]["destination"]) == "KT1GWnsoFZVHGh7roXEER3qeCcgJgrXT3de2":
            liquidations_list.append(c["body"]["hash"])
    return liquidations_list


def parse_search():
    ts = int(time.time())
    url = f"https://api.better-call.dev/v1/search?q=liquidate&s={(ts - 604800)}&i=operation"  # week to date
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
    output_list = []

    for liquidation in liquidations_list:

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

        hash = (liquidation[0]
        ["hash"])

        ctez_lost = (int(ctez_outstanding_from) - int(ctez_outstanding_to)) / 1000000
        xtz_lost = (int(tez_balance_from) - int(tez_balance_to)) / 1000000

        liquidation_dict = {"ctez_outstanding_from": ctez_outstanding_from,
                            "ctez_outstanding_to": ctez_outstanding_to,
                            "tez_balance_from": tez_balance_from,
                            "tez_balance_to": tez_balance_to,
                            "owner": owner,
                            "liquidator": liquidator,
                            "hash": hash,
                            "xtz_lost": xtz_lost,
                            "ctez_lost": ctez_lost
                            }
        output_list.append(liquidation_dict)

    return output_list

def save(output):
    with open("output.json", "w") as outfile:
        outfile.write()

if __name__ == "__main__":
    candidates = parse_search()
    hashes = qualify(candidates)
    liquidations = parse_operations(hashes)
    nice = prettify(liquidations)

    print(nice)
