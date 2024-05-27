# bytecode_collector

*bytecode_collector* collects bytecode of smart contracts from RPC.

You can view the status of an RPC address at [ChainList](https://chainlist.org/chain/1), and select one active address to use.

You can replace the RPC address in this line of code
```
const web3 = new Web3(new Web3.providers.HttpProvider("https://rpc.ankr.com/eth"));
```

*bytecode_collector* reads a **json file** that contains a list of smart contract addresses, and then downloads the bytecode of the address list into the default folder *Bytecodes*.

There are two variables, *folder* is where the json file lies, and *file_name* is the name of the json file.

The function *getGroundAddressAsy* is the entrance to download the bytecode, this function has two parameters, *filename* is the path of the json file, *isImplementation* is to determine whether download the bytecode of logic contracts, which are obtained by *logic_contract_collector*, the default value of *isImplementation* is false.

To run
```
node bytecode_collector.js
```

*bytecode_collector* generates a new json file in the end.
