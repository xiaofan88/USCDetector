
const detectProxyTarget = require("evm-proxy-detection").default;

const { JsonRpcProvider } = require("@ethersproject/providers");

const jsonRpcProvider = new JsonRpcProvider("https://rpc.ankr.com/eth");

// const jsonRpcProvider = new JsonRpcProvider("https://ethereum.blockpi.network/v1/rpc/public");

const requestFunc = ({ method, params }) => jsonRpcProvider.send(method, params);

const fs = require('fs');


async function getTarget(obj, filename){

    let address = obj["address"]

    let delegatecall = obj["delegatecall"]

    if (delegatecall > 0){
      let target = await detectProxyTarget(
        address,
        requestFunc
      );

      console.log(target)

      obj["implementation"] = target;

      fs.appendFile(`${folder}/${target_file_path}_logic.json`, `${JSON.stringify(obj)}\n`, (err) => {
        // if (err) throw err;
    
        console.log(`${address}: saved...`);
      });

    } else {

      console.log(`${address} doesn't contain the delegatecall opcode, skip...`)
      
    }    

}

async function test(address){
    let target = await detectProxyTarget(
        address,
        requestFunc
      );

      console.log(target)
}

// test("0x5c545ca7f9d34857664fdce6adc22edcf1d5061f");

var getProxyAddressAsy = async function(filename){

  console.log(filename);

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
            address = obj["address"].split("0x")[1];

            console.log(`${count}, ${address}: begin...`);

            getTarget(obj, filename);
         
          
      } catch (error) {
          
            fs.appendFile('contracts_errors.json', `${address}: ${JSON.stringify(error)}\n`, (err) => {
                // if (err) throw err;
          
                console.log(`${address}: error recored...`);
        })

      }

      await new Promise(resolve => setTimeout(resolve, 1500));

  }
  console.log(`${count} complete...`)
}

let folder = "D:/Code/USCDetector"
let target_file_path = "example_address_list_parse"

getProxyAddressAsy(`${folder}/${target_file_path}.json`)

