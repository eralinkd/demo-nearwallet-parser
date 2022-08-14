from bs4 import BeautifulSoup
import json
import requests


def get_configs():
    with open("data/account_info.json", "r", encoding="utf-8") as f:
        account = json.load(f)
    with open("data/price_info.json", "r", encoding="utf-8") as f:
        price = json.load(f)
    return account, price


def get_html(transaction):
    html = requests.get(f"https://explorer.mainnet.near.org/transactions/{transaction}").text
    return html


def get_task_info(html):
    j = json.loads(html.find("div", class_="c-CodePreviewWrapper-gJFGlx").text)
    return j["performed_by"], j["reviewers"], j["mnear_per_task"] / 1000, j["mnear_per_review"] / 1000


def get_paid_info(html, acc):
    acc_link_path = f"/accounts/{acc}"
    return \
        float(html.find_all("a", attrs={"href": acc_link_path})[1].find_parent("span").find_previous_sibling(
            "span").text.split(
            "\xa0")[0])


def analysis(price_info, account_info, performer, transaction):
    account = account_info["account"]
    paid = get_paid_info(soup, account)
    transaction_link = f"https://explorer.mainnet.near.org/transactions/{transaction}"

    mgr = price_info["moonglow_review"]
    msr = price_info["moonstone_review"]
    shr = price_info["sunshine_review"]
    mgt = price_info["moonglow_task"]
    mst = price_info["moonstone_task"]
    sht = price_info["sunshine_task"]
    sh = account_info["sunshiner"]
    ms = account_info["moonstoner"]
    mg = account_info["moonglower"]

    if performer != account:  # if review
        if paid >= mgr and mg:
            print(f"moonglow review {transaction_link} {paid}")
        elif paid >= msr and ms:
            print(f"moonstone review {transaction_link} {paid}")
        elif paid >= shr and sh:
            print(f"sunshine review {transaction_link} {paid}")
        else:
            print(f"undefined transaction {transaction_link} {paid}")
    else:
        if paid >= mgt * 0.5 * 0.75 and mg:
            print(f"moonglow task {transaction_link} {paid}")
        elif paid >= mst * 0.75 and ms:
            print(f"moonstone task {transaction_link} {paid}")
        elif paid >= sht * 0.5 and sh:
            print(f"sunshine task {transaction_link} {paid}")
        else:
            print(f"undefined transaction {transaction_link} {paid}")


account_info, price_info = get_configs()
transactions = [
    "5bfAeLhFrpXnHFKRTF1Gqe833QJeN15LUVvwvsTqWU25",
    "DZNJH6iC1xx6aQuXXgfPdbkzw9B7HYsRvrB3xkdxP5im",
    "9SFZCLrJX4BNSazcqspwkFbqwWEhNdYjcsDqiFyCBaBS",
    "GXXAxVh787ptbhzAAREYaA6gwhJTCsccK4qtM4NCMqgB",
    "3ZQhacyvAnDg6M4M1sEZxfBxwWjfBKoCKzmtis7CURNY",
    "AqUSBEeaCh1Nyh3Ey7866vjpveWTrySUFPe6kH3gTiGN",
    "JACRAS7AQNSWWydojPEfdtdft5SK287AgtTZwXYj8ioS",
    "4ZCGCf5VN8sm9b1Z2EWhWgKGNu77GRWKazJxiTjXqheY",
    "GsKSZyvSPcdEPWsHeh8Ka83A9Rs7YfmVukRzMN2ivWuL",
    "2V71i9QoUxcuN4NaZfafrRSP2vY966JjK5eeKcY1PuXh",
    "8NNpgenY8hPxxX4ZPEgr7E5YwkJKU5iCMZ8yvGFqRLBo",
    "DLmaVd3yKbrsRw8eQEXsqPF46AWx8VPtjNGwNXtNYWW8",
    "AHVFCyL54hnvSVyzJyZ5rUPnChn9DFvUUyHnU9P22TDE",
    "BXPrfgxXwfnxS38evmirChtF7pyWejJPcM8vtS13DV2r"
]
for transaction in transactions:
    soup = BeautifulSoup(get_html(transaction), 'html.parser')
    performer, reviewers, task_reward, review_reward = get_task_info(soup)
    analysis(price_info, account_info, performer, transaction)
