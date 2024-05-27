[![Build Status](https://travis-ci.org/abi-decoder/abi-decode-functions.svg?branch=master)](https://travis-ci.org/abi-decoder/abi-decode-functions)

# abi-decode-functions
Extract and list up function ids from opcodes.

## Installation

```
$ npm install --save abi-decode-functions
```

## Usage

```
const AbiFunctions = require('abi-decode-functions')
// or 
// import AbiFunctions from 'abi-decode-functions'
const opcodes = getContractOpcodes()
const decoder = new AbiFunctions(opcodes)
const functionIds = dcoder.getFunctionIds()
```

## NOTE
This tools also get get-function of public storage variable.
