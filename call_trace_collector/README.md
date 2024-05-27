# call_trace_collector

*call_trace_collector* collects call traces of smart contracts from apis.

*call_trace_collector* first collects the creation transactions from etherscan api. Please generate your own apikey on the [etherscan](https://etherscan.io/).

You can replace the apikey in this line of code
```
apikey = "*****"
```

Then *call_trace_collector* collects the call traces of collected transactions from openchain api.

There are two variables, *folder* is where the json file lies, and *file_name* is the name of the json file that contains a list of smart contract addresses.

To run
```
python call_trace_collector.py
```

*call_trance_collector* generates a new json file in the end.
