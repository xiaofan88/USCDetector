const fs = require('fs');

const { EVM } = require("evm");
const Web3 = require('web3');

const web3 = new Web3(new Web3.providers.HttpProvider("https://rpc.ankr.com/eth"));

const parser = require('truffle-code-utils');

const Web3EthAbi = require('web3-eth-abi');

const AbiFunctions = require('abi-decode-functions').default


function GetBytecode(address, isImplementation){

    try {
        
        web3.eth.getCode(`0x${address}`).then((code) => {
    
            let prefix = address.substring(0, 2);
            
            let filepath;
            if (!isImplementation){
            
                filepath = `Bytecodes/${prefix}`;

            } else {
                filepath = `ImplementationBytecodes/${prefix}`;
            }
    
            fs.access(filepath, (e) => {
    
                if(e != null && e.toString().indexOf("no such file") != -1){
                    
                    fs.mkdir(filepath, (err) => {
                        if(err) console.log(err);
                        
                        writeIntoLocal(address, `${filepath}/${address}`, code, isImplementation);
    
                    });
    
                } else {
                    writeIntoLocal(address, `${filepath}/${address}`, code, isImplementation);
    
                }
    
            });
    
        });


    } catch (error) {
        fs.appendFile('new_contracts_errors.json', `${address}: ${JSON.stringify(error)}\n`, (err) => {
            console.log(`${address}: error recored...`);
        })
    }
    
}

function writeIntoLocal(address, path, code, isImplementation){
    
    let opcodes = parser.parseCode(code);


    let decoder = new AbiFunctions(code)

    let funcsIds = decoder.getFunctionIds();
    let funcs = Array.from(new Set(funcsIds));

    let funcPcs = decoder.getFunctionPcs();
    let maxFuncPc = Math.max(...funcPcs);

    let delegatecall = 0;
    let callcode = 0;
    let call = 0;
    let staticcall = 0;
    let create2 = 0;
    let create = 0;
    let selfdestruct = 0;
    let returndatasize = 0;
    let returndatacopy = 0;
    let otherfuncs = [];

    // detect fallback function
    let DETECT_FALLBACK_OPCODES = JSON.stringify(['PUSH4', 'EQ', 'PUSH2', 'JUMPI', 'JUMPDEST', 'PUSH1', 'DUP1', 'REVERT']);
    let push4Indexes = opcodes.map((e, i) => e.name === 'PUSH4' ? i : -1).filter((i) => i > -1);
    let expections = push4Indexes.map((i) => opcodes.slice(i, i + 8));
    let result = expections.filter((e) => {
        let name = e.map((o) => o.name);
        return JSON.stringify(name) === DETECT_FALLBACK_OPCODES
    });
   
    let controlPcLine = 0;
    if (opcodes.length > 0){
        let last = opcodes[opcodes.length-1];
        let lastPc = last["pc"];
        controlPcLine = lastPc - parseInt(lastPc / 5);
    }

    let createPcLine = 0;
    let newFuncs = [];

    for(let index in opcodes){

        let op = opcodes[index];

        if(op["name"] == "DELEGATECALL"){
            delegatecall += 1;
            continue;
        }

        if(op["name"] == "CALLCODE"){
            callcode += 1;
            continue;
        }

        if(op["name"] == "CALL"){
            call += 1;
            continue;
        }

        if(op["name"] == "STATICCALL"){
            staticcall += 1;
            continue;
        }

        if(op["name"] == "CREATE2"){
            let pc = op["pc"];

            if (createPcLine < pc){
                createPcLine = pc;
            }

            create2 += 1;
            continue;
        }

        if(op["name"] == "CREATE"){

            let pc = op["pc"];

            if (createPcLine < pc){
                createPcLine = pc;
            }

            create += 1;
            continue;
        }

        if (op["name"] == "SELFDESTRUCT"){
            selfdestruct += 1
            continue;
        }

        if (op["name"] == "RETURNDATASIZE"){
            returndatasize += 1
            continue;
        }

        if (op["name"] == "RETURNDATACOPY"){
            returndatacopy += 1
            continue;
        }

        if (op["name"] == "PUSH4"){
            let pushData = op["pushData"];
            let pc = op["pc"];

            
            if (pushData != "0xffffffff" && !otherfuncs.includes(pushData) && (pc > maxFuncPc)){

                otherfuncs.push(pushData)

            }
            

            if((createPcLine == 0 || pc <= createPcLine) && funcs.includes(pushData) && !newFuncs.includes(pushData)){
                newFuncs.push(pushData);
            }
            
            continue;
        }

        if(op["name"] == "INVALID") {

            let pc = op["pc"];

            if (pc > controlPcLine)
                break;
        };
    }

    let json_obj = {
        "address": `0x${address}`,
        // "address": `${addr}`,
        "delegatecall": delegatecall,
        "callcode": callcode,
        "call": call,
        "staticcall": staticcall,
        "nofallback": result.length,
        "create": create,
        "create2": create2,
        "selfdestruct": selfdestruct,
        "returndatasize": returndatasize,
        "returndatacopy": returndatacopy,
        "functions": funcs,
        "onlyfunctions": newFuncs,
        "otherfunctions": otherfuncs
    };


    fs.access(`${path}`, (e) => {
        // console.log(e);
        if(e != null && e.toString().indexOf("no such file") != -1){

            fs.mkdir(`${path}`, function(error){
                if(error) {
                    fs.appendFile('new_ontracts_errors.json', `${address}: ${JSON.stringify(error)}\n`, (err) => {
                        console.log(`${address}: error recored...`);
                    })
                }
                    
                console.log(`${address} mkdir...`)

                fs.writeFile(`${path}/${address}_bytecode.json`, `${JSON.stringify(code)}\n`, (err) => {
                    if (err) {
                        fs.appendFile('new_contracts_errors.json', `${address}: ${JSON.stringify(err)}\n`, (err) => {
                            console.log(`${address}: error recored...`);
                        })
                    }
                
                    console.log(`${address}: bytecode saved...`);
                })
        
                fs.writeFile(`${path}/${address}_reparse.json`, `${JSON.stringify(json_obj)}\n`, (err) => {
                    if (err) {
                        fs.appendFile('new_contracts_errors.json', `${address}: ${JSON.stringify(err)}\n`, (err) => {
                            console.log(`${address}: error recored...`);
                        })
                    }
                
                    console.log(`${address}: reparse saved...`);
                })
                
            });

        } else {

            fs.appendFile(`new_contracts_repeat.json`, `${JSON.stringify(address + ": " + path)}\n`, (err) => {
                if (err) console.log(err);
            
                console.log(`${address}: contracts_repeat saved...`);
            });
        }
    });

    if (!isImplementation){
        fs.appendFile(`${foler}/${file_name}_parse.json`, `${JSON.stringify(json_obj)}\n`, (err) => {
            if (err) {
                fs.appendFile('new_contracts_errors.json', `${address}: ${JSON.stringify(err)}\n`, (err) => {
                    console.log(`${address}: error recored...`);
                })
            }
        
            console.log(`${address}: reparse file saved...`);
        })
    }

}


function checkBytecodesFolder(){

    console.log("Bytecodes folder check...")

    fs.access("Bytecodes", (e) => {

        if(e != null && e.toString().indexOf("no such file") != -1){

            fs.mkdir('Bytecodes', function(error){
                if(error) {
                    fs.appendFile('new_contracts_errors.json', `${address}: ${JSON.stringify(error)}\n`, (err) => {
                        console.log(`${address}: error recored...`);
                    })
                }
                    
                console.log(`Bytecodes folder mkdir...`)

            });

        }
    });

}

function checkImplementationBytecodesFolder(){

    console.log("ImplementationBytecodes folder check...")

    fs.access("ImplementationBytecodes", (e) => {

        if(e != null && e.toString().indexOf("no such file") != -1){

            fs.mkdir('ImplementationBytecodes', function(error){
                if(error) {
                    fs.appendFile('new_contracts_errors.json', `${address}: ${JSON.stringify(error)}\n`, (err) => {
                        console.log(`${address}: error recored...`);
                    })
                }
                    
                console.log(`ImplementationBytecodes folder mkdir...`)

            });

        }
    });

}


var getGroundAddressAsy = async function(filename, isImplementation = false){

    console.log(filename);

    if (!isImplementation){
        
        checkBytecodesFolder();

    } else {

        checkImplementationBytecodesFolder();

    }
    

    var data = fs.readFileSync(`${filename}`, "utf-8");

    var lines = data.split(/\r?\n/);

    var count = 0;

    var address;

    for(let index in lines){
        address = "";
        
        try {

            let line = lines[index];

            if(line == "") continue;

            count++;

            let obj = JSON.parse(line);
            
            if(!isImplementation){
                
                address = obj["address"].split("0x")[1];

            } else {
                if (obj["implementation"] == null)
                    continue
                
                address = obj["implementation"].split("0x")[1];
            }
            
            

            console.log(`${count}, ${address}: begin...`);

            GetBytecode(address, isImplementation);
            
        } catch (error) {
            
            fs.appendFile('new_contracts_errors.json', `${address}: ${JSON.stringify(error)}\n`, (err) => {
                // if (err) throw err;
            
                console.log(`${address}: error recored...`);
            })

        }

        await new Promise(resolve => setTimeout(resolve, 1000));

    }
    console.log(`${count} complete...`)
}


var encodeSignature = function(sig){
    let en = Web3EthAbi.encodeFunctionSignature(sig);
    console.log(en);
}

let foler = "D:/Code/USCDetector"
// let file_name = "example_address_list"

// getGroundAddressAsy(`${foler}/${file_name}.json`);


let file_name = "example_address_list_parse_logic"
getGroundAddressAsy(`${foler}/${file_name}.json`, true);
