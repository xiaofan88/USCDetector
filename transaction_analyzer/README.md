# transaction_analyzer

*transaction_analyzer* contains two parts, first part *transaction_decoupling* is to generate abi according to the first four bytes in the *input* value in the transactions. The abi contains the function name, function parameters, which will be used to extract the value of parameters in the *input*.

*transaction_decoupling* generates a new json file in the end.

The second part is the *transaction_analyzer*, which reads the file generated by the *transaction_decoupling* to extract the value of parameters in the *input*.

*transaction_analyzer* generates a new json in the end.
