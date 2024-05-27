
import json
import WriteData


def group_transaction_address(folder, file_name):

    with open(folder + '/' + file_name + '.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()
    
    to_address_list = {}
    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        to_address = json_obj["to_address"]

        if to_address not in to_address_list.keys():
            # WriteData.write_in_path(to_address, "JS/transactions/transactions_keys")
            to_address_list[to_address] = []
        
        temp_ary = []
        temp_ary.append(json_obj["hash"])
        temp_ary.append(json_obj["from_address"])
        temp_ary.append(json_obj["block_timestamp"])
        temp_ary.append(json_obj["function_name"])
        temp_ary.append(json_obj["types"])
        temp_ary.append(json_obj["inputs"])
        if "ext" in json_obj:
            temp_ary.append(json_obj["ext"])

        to_address_list[to_address].append(temp_ary)

    upgrade_more_than_twice = {}
    for key in to_address_list.keys():
        arr = to_address_list[key]
        arr.sort(key=lambda arr: arr[2])
        to_address_list[key] = arr

        if len(arr) >= 2:
            upgrade_more_than_twice[key] = arr



    print(len(to_address_list.keys()))
    WriteData.write_in_path(json.dumps(dict(to_address_list)), f'{folder}/{file_name}_group_all')


folder = "D:/Code/USCDetector"
file_name = "example_transaction_list_abi_reparse"

group_transaction_address(folder, file_name)


