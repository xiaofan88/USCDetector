

import json

import pandas as pd
import os
import WriteData


def analysis(folder, filename):

    function_selectors = {}

    with open(r'D:/Code/USCDetector/common_upgrade_function_keywords/All_Upgrade_Signature.json',encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    with open(folder + '/' + filename + '.json',encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        hex = json_obj["hex_signature"]
        text = json_obj["text_signature"]

        if hex not in function_selectors.keys():
            function_selectors[hex] = text

    total = 0
    for line in all_lines1:

        total = total + 1
        obj = json.loads(line.rstrip())

        print(f"{total}: {obj['address']}")

        funcs = obj["functions"]

        delegatecall = obj["delegatecall"]
        selfdestruct = obj["selfdestruct"]
        call = obj["call"]
        staticcall = obj["staticcall"]
        returndatasize = obj["returndatasize"]
        returndatacopy = obj["returndatacopy"]
        otherfunc = obj["otherfunctions"]
        create = obj["create"]
        create2 = obj["create2"]
        onlyfunctions = obj["onlyfunctions"]

        if delegatecall > 0 or selfdestruct > 0:
            continue


        fileter_otherfunctions = ["0x150b7a02", "0xa9059cbb", "0xa3e76c0f", "0x23b872dd", "0xf3993d11", "0x42842e0e", "0xf23a6e61", "0xbc197c81", "0x08c379a0"]
        # fileter_otherfunctions = ["0x150b7a02", "0xa9059cbb", "0xa3e76c0f", "0x23b872dd", "0xf3993d11", "0x42842e0e", "0xf23a6e61", "0xbc197c81", "0x4e487b71", "0x08c379a0"]

        call_count = call + staticcall
        call_flag = (call > 0 or staticcall > 0) and ((returndatacopy >= call_count and returndatasize >= call_count) or len(otherfunc) > 0)

        if len(otherfunc) <= 1:
            for func in otherfunc:
                if func in fileter_otherfunctions:
                    call_flag = False

        proxy_flag = False


        hit_arr = []
        hit_arr_only = []

        for func in funcs:

            if func in function_selectors.keys():
                func_str = f"{func}({function_selectors[func]})"
                hit_arr.append(func_str)
        
        if create > 0 or create2 > 0:
            for onlyfunc in onlyfunctions:
                if onlyfunc in function_selectors.keys():
                    func_str_only = f"{onlyfunc}({function_selectors[onlyfunc]})"
                    hit_arr_only.append(func_str_only)

        obj["factory"] = 0
        if len(hit_arr) > 0:
            
            if (create > 0 or create2 > 0) and len(hit_arr_only) <= 0:
                obj["factory"] = 1

            obj["hit"] = hit_arr

            if proxy_flag is False and call_flag is True:
                if "0xadfca15e(facetFunctionSelectors(address))" in hit_arr:
                    WriteData.writeIn(json.dumps(obj), f'{folder}/Upgrade')
                else:
                    if call > 0:
                        WriteData.writeIn(json.dumps(obj), f'{folder}/Call_Upgrade')
                    else:
                        WriteData.writeIn(json.dumps(obj), f'{folder}/Upgrade')

            if proxy_flag is False and call_flag is False:
                up_flag = True
                if len(otherfunc) <= 1:
                    for func in otherfunc:
                        if func in fileter_otherfunctions and func != "0x08c379a0":
                            up_flag = False
                if up_flag is True:
                    WriteData.writeIn(json.dumps(obj), f'{folder}/Upgrade')
                else:
                    WriteData.writeIn(json.dumps(obj), f'{folder}/Not_Upgrade')

        else:
            WriteData.writeIn(json.dumps(obj), f'{folder}/Not_Upgrade')


def parse_delegatecall_target(folder, filename):

    function_selectors = {}

    with open(r'D:/Code/USCDetector/common_upgrade_function_keywords/All_Upgrade_Signature.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    for line in all_lines:
        json_obj = json.loads(line.rstrip())

        hex = json_obj["hex_signature"]
        text = json_obj["text_signature"]

        if hex not in function_selectors.keys():
            function_selectors[hex] = text

    with open(folder + '/' + filename + '.json',encoding='utf-8') as f:
        all_lines1 = f.readlines()
        f.close()
    

    total = 0
    for line in all_lines1:

        total = total + 1
        obj = json.loads(line.rstrip())

        print(f"{total}: {obj['address']}")

        funcs = obj["functions"]

        delegate = obj["delegatecall"]
        callcode = obj["callcode"]
        call = obj["call"]
        staticcall = obj["staticcall"]
        implementation = obj["implementation"]
        # implementation = None
        returndatasize = obj["returndatasize"]
        returndatacopy = obj["returndatacopy"]
        otherfunc = obj["otherfunctions"]
        create = obj["create"]
        create2 = obj["create2"]
        onlyfunctions = obj["onlyfunctions"]
        nofallback = obj["nofallback"]

        fileter_otherfunctions = ["0x150b7a02", "0xa9059cbb", "0xa3e76c0f", "0x23b872dd", "0xf3993d11", "0x42842e0e", "0xf23a6e61", "0xbc197c81", "0x4e487b71", "0x08c379a0"]
        fileter_otherfunctions_both = ["0x150b7a02", "0xa9059cbb", "0xa3e76c0f", "0x23b872dd", "0xf3993d11", "0x42842e0e", "0xf23a6e61", "0xbc197c81", "0x4e487b71", "0x08c379a0", "0x52d1902d"]

        call_count = call + staticcall + delegate

        call_flag = (call > 0 or staticcall > 0) and ((returndatacopy >= call_count and returndatasize >= call_count) or len(otherfunc) > 0)

        proxy_flag = delegate > 0 or callcode > 0

        if len(otherfunc) <= 1:
            for func in otherfunc:
                if func in fileter_otherfunctions:
                    call_flag = False

        hit_count = 0
        not_hit_count = 0

        hit_arr = []
        hit_arr_only = []

        for func in funcs:

            if func in function_selectors.keys():
                func_str = f"{func}({function_selectors[func]})"
                hit_arr.append(func_str)
        
        if create > 0 or create2 > 0:
            for onlyfunc in onlyfunctions:
                if onlyfunc in function_selectors.keys():
                    func_str_only = f"{onlyfunc}({function_selectors[onlyfunc]})"
                    hit_arr_only.append(func_str_only)

        obj["factory"] = 0
        if len(hit_arr) > 0:

            obj["hit"] = hit_arr
            
            if proxy_flag is True:

                if (create > 0 or create2 > 0) and len(hit_arr_only) <= 0:
                    obj["factory"] = 1


                if call_flag is False:
                    
                    if nofallback <= 0:
                        WriteData.writeIn(json.dumps(obj), f'{folder}/Proxy_Upgrade')
                    else:
                        WriteData.writeIn(json.dumps(obj), f'{folder}/Not_Upgrade')

                else:
                    
                    if nofallback <= 0:

                        if call > 0:
                            if len(otherfunc) <= 5 and len([False for c in otherfunc if c not in fileter_otherfunctions_both]) <= 0:
                                WriteData.writeIn(json.dumps(obj), f'{folder}/Proxy_Upgrade')
                            else:
                                # using call there will be state changed
                                WriteData.writeIn(json.dumps(obj), f'{folder}/Both_Upgrade')
                        else:
                            # using staticcall without state changed
                            WriteData.writeIn(json.dumps(obj), f'{folder}/Proxy_Upgrade')
                    else:
                        if call > 0:
                            WriteData.writeIn(json.dumps(obj), f'{folder}/Call_Upgrade')
                        else:
                            WriteData.writeIn(json.dumps(obj), f'{folder}/Upgrade')
                    
            else:
                WriteData.writeIn(json.dumps(obj), f'{folder}/Not_Proxy_Upgrade')

            
        else:
            if implementation is not None and implementation != "":
                addr = implementation.replace("0x", "")
                prefix = addr[0:2]
                path = r"D:/Code/USCDetector/bytecode_collector/ImplementationBytecodes/" + prefix + "/" + addr
            
                filename = f"{path}/{addr}_reparse.json"
                print(os.path.join(path, filename))
            
                if os.path.exists(path):
                    with open(os.path.join(path, filename).replace('\\', '/'), encoding="utf-8") as json_obj:
                        json_str = json_obj.read()
            
                        obj_imp = json.loads(json_str)
            
                        funcs = obj_imp["functions"]
                        nofallback = obj["nofallback"]
            
                        hit_impl_arr = []
            
                        for func in funcs:
                            if func in function_selectors.keys():
                                func_str = f"{func}({function_selectors[func]})"
                                hit_impl_arr.append(func_str)
            
                        if len(hit_impl_arr) > 0 and nofallback <= 0:
                            obj["hit"] = hit_impl_arr
                            WriteData.writeIn(json.dumps(obj), f'{folder}/Proxy_Upgrade')
                            WriteData.writeIn(json.dumps(obj), f'{folder}/Proxy_Upgrade_UUPS')
                        else:
                            WriteData.writeIn(json.dumps(obj), f'{folder}/Not_Upgrade')
                else:
                    WriteData.writeIn(json.dumps(obj), f'{folder}/Not_Determine')
            
            else:
                WriteData.writeIn(json.dumps(obj), f'{folder}/Not_Upgrade')



def parse_selfdestruct_file(folder, file_name):

    with open(f'{folder}/{file_name}.json', encoding='utf-8') as f:
        all_lines = f.readlines()
        f.close()

    total = 0
    for line in all_lines:
        
        total = total + 1

        obj = json.loads(line.rstrip())

        print(f"{total}: {obj['address']}")

        codehash = obj["codehash"]
        createOpcode = obj["createOpcode"]

        if codehash != "" or createOpcode != "":
            WriteData.writeIn(json.dumps(obj), f'{folder}/Meta_hit')
        
        else:
            WriteData.writeIn(json.dumps(obj), f'{folder}/Meta_not_hit')


folder = "D:/Code/USCDetector"

delegatecall_file = "example_address_list_parse_logic"
rest_file = "example_address_list_parse"
selfdestruct_file = "example_address_list_parse_creator_call_trace"

analysis(folder, rest_file)
parse_delegatecall_target(folder, delegatecall_file)
parse_selfdestruct_file(folder, selfdestruct_file)
