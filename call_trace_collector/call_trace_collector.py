import json
import time
import re
import requests
import WriteData



creation_url = "https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses="

tx_trace_url = "https://tx.eth.samczsun.com/api/v1/trace/ethereum/"

transaction_url = "https://api.etherscan.io/api?module=transaction&action=getstatus&txhash="

apikey = "33AT13C3V1DANVRSP6F5DP9BQP2CBKJRD5"


def request_contract_creation(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    

    total = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total = total + 1

        address = json_obj["address"]

        selfdestruct = json_obj["selfdestruct"]
        delegatecall = json_obj["delegatecall"]

        if selfdestruct <= 0 or delegatecall > 0:
            continue

        print(f"{total}, {address} begin...")

        req_url = f"{creation_url}{address}&apikey={apikey}"
        print('req_url:' + req_url)

        try:
            response = requests.get(req_url)
            result = json.loads(response.text)

            print(result["status"] + " " + result["message"])

            if result["status"] == "1" and result["message"] == "OK":
                result_msg = result["result"]

                if len(result_msg) > 0:
                    creator = result["result"][0]["contractCreator"]
                    txHash = result["result"][0]["txHash"]

                print(f"{creator}, {txHash}")
                json_obj["contractCreator"] = creator
                json_obj["txHash"] = txHash

                WriteData.write_in_path(json.dumps(json_obj), f"{folder}/{file_name}_creator")


            else:
                print(f"{address}: request error")

        except Exception as msg:

            print(msg)
            time.sleep(30)

        time.sleep(1)
    


def request_contract_txtrace(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        total = total + 1

        address = json_obj["address"]
        txHash = json_obj["txHash"]

        print(f"{total}, {address} begin...")

        req_url = f"{tx_trace_url}{txHash}"
        print('req_url:' + req_url)

        try:
            response = requests.get(req_url)
            result = json.loads(response.text)

            print(result["ok"])

            if result["ok"] is True:
                result_msg = result["result"]
                entrypoint = result_msg["entrypoint"]

                entrypoint_variant = entrypoint["variant"]
                print(entrypoint_variant)
               
                children = entrypoint["children"]
                json_obj["createOpcode"] = ""
                json_obj["codehash"] = ""

                for child in children:
                    if "variant" in child:
                        variant = child["variant"]
                        to = child["to"]
                        if (variant == "create" or variant == "create2") and to == address:
                            codehash = child["codehash"]
                            json_obj["createOpcode"] = variant
                            json_obj["codehash"] = codehash
                            print(variant)
                            break

                        elif "children" in child:

                            subchildren = child["children"]

                            for subchild in subchildren:
                                if "variant" in subchild:
                                    variant = subchild["variant"]
                                    to = subchild["to"]
                                    if (variant == "create" or variant == "create2") and to == address:
                                        codehash = subchild["codehash"]
                                        json_obj["createOpcode"] = variant
                                        json_obj["codehash"] = codehash
                                        print(variant)
                                        break


                WriteData.write_in_path(json.dumps(json_obj), f"{folder}/{file_name}_call_trace")
            else:
                print(f"{address}: request error")

        except Exception as msg:
            print(msg)
            time.sleep(10)


        time.sleep(1)



folder = "D:/Code/USCDetector"
file_name = "example_address_list_parse"

request_contract_creation(folder, file_name)

request_contract_txtrace(folder, f"{file_name}_creator")



