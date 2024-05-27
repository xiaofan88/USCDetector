const fs = require('fs');

const InputDataDecoder = require('ethereum-input-data-decoder')

var inputDataDecoder = async function(folder, file_name){
    console.log(file_name)

    var data = fs.readFileSync(`${folder}/${file_name}.json`, "utf-8");

    var lines = data.split(/\r?\n/);

    for(let index in lines){
        let line = lines[index];

        if(line == "") continue;

        let obj = JSON.parse(line);
        abi = obj["abi"]

        to_address = obj["to_address"]


        console.log(to_address)

        let decoder = new InputDataDecoder(abi);

        let input = obj["input"]

        let result = decoder.decodeData(input);
        
        let json_obj = {
            "hash": obj["hash"],
            "from_address": obj["from_address"],
            "to_address": obj["to_address"],
            "block_timestamp": obj["block_timestamp"],
            "function_name": result["method"],
            "types": result["types"],
            "inputs": result["inputs"]
        }

        fs.appendFile(`${folder}/${file_name}_reparse.json`, `${JSON.stringify(json_obj)}\n`, (err) => {
            if (err) {
                console.log(`${to_address}: ${err}`);
            }
        
            console.log(`${to_address}: reparse saved...`);
        })

        await new Promise(resolve => setTimeout(resolve, 20));



    }

}

let folder = "D:/Code/USCDetector"
let file_name = "example_transaction_list_abi"
inputDataDecoder(folder, file_name)

