import json

import WriteData


def build_transactions_abi(folder, file_name):

    function_selectors = {"0x6aae83f3": "setrouteChain(address)"}

    with open(r'D:/Code/USCDetector/common_upgrade_function_keywords/All_Upgrade_Signature.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        hex = json_obj["hex_signature"]
        text = json_obj["text_signature"]

        if hex not in function_selectors.keys():
            function_selectors[hex] = text

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
   

    for line in all_lines:
        json_obj = json.loads(line.rstrip())


        to_address = json_obj["to_address"]
        print(to_address)
        input = json_obj["input"]

        from_address = json_obj["from_address"]

        function_selector = input[0:10]
        
        
        ready_input = []
        ready_input.append(function_selector)
        ready_input.append(function_selectors[function_selector])

        text_signature = function_selectors[function_selector]

        function_name = text_signature.split('(')[0]

        function_args = text_signature.split('(')[1].split(')')[0].split(',')

        abi_obj = {}
        abi_obj["constant"] = False
        abi_obj["inputs"] = []
        
        for index in range(0, len(function_args)):
            arg_obj = {}
            arg_obj["name"] = f"name{index}"
            arg_obj["type"] = function_args[index]

            abi_obj["inputs"].append(arg_obj)
        
        abi_obj["name"] = function_name
        abi_obj["outputs"] = []
        abi_obj["payable"] = False
        abi_obj["type"] = "function"

        abi_list = []
        abi_list.append(abi_obj)


        obj = json.loads(json.dumps({}))
        obj["hash"] = json_obj["hash"]
        obj["from_address"] = json_obj["from_address"]
        obj["to_address"] = json_obj["to_address"]
        obj["block_timestamp"] = json_obj["block_timestamp"]
        obj["abi"] = abi_list
        obj["input"] = input


        WriteData.write_in_path(json.dumps(obj), f'{folder}/{file_name}_abi')


folder = "D:/Code/USCDetector"
file_name = "example_transaction_list"
build_transactions_abi(folder, file_name)

