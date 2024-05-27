# logic_contract_collector


*logic_contract_collector* collects logic contract of smart contracts that contain *delegatecall* from RPC.

You can view the status of an RPC address at [ChainList](https://chainlist.org/chain/1), and select one active address to use.

You can replace the RPC address in this line of code
```
const jsonRpcProvider = new JsonRpcProvider("https://rpc.ankr.com/eth");
```

*logic_contract_collector* reads a **json file** that contains a list of smart contract addresses, and then gets logic contracts and generates a new json file in the end.

There are two variables, *folder* is where the json file lies, and *target_file_path* is the name of the json file.

The function *getProxyAddressAsy* is the entrance.

To run
```
node logic_contract_collector.js
```
