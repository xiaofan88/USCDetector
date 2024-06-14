# USCDetector

This repo contains the code for our WWW'24 paper "Characterizing Ethereum Upgradable Smart Contracts and Their Security Implications".

## Workflow

- **bytecode_collector**: collects bytecode of a list address of smart contracts
  
  More detail in this [guide](https://github.com/xiaofan88/USCDetector/blob/main/bytecode_collector/README.md)

- **logic_contract_collector**: collects logic contracts of smart contracts that contain *DELEGATECALL*

  More detail in this [guide](https://github.com/xiaofan88/USCDetector/blob/main/logic_contract_collector/README.md)
  
- **call_trace_collector**: collects call trace of smart contracts that contain *SELFDESTRUCT*

  More detail in this [guide](https://github.com/xiaofan88/USCDetector/blob/main/call_trace_collector/README.md)

- **etherscan_crawler**: collects "Old Contracts" that are labeled by etherscan

  More detail in this [guide](https://github.com/xiaofan88/USCDetector/blob/main/etherscan_crawler/README.md)

- **pattern_detector**: detects smart contract upgrade patterns by using collected information

  More detail in this [guide](https://github.com/xiaofan88/USCDetector/blob/main/patterns_detector/README.md)

- **transaction_analyzer**: extracts values of function parameters in the tranctions

  More detail in this [guide](https://github.com/xiaofan88/USCDetector/blob/main/transaction_analyzer/README.md)

- **upgrade_chain_constructor**: constructs the upgrade chains by using the information extracted in *transaction_analyzer*

  More detail in this [guide](https://github.com/xiaofan88/USCDetector/blob/main/upgrade_chain_constructor/README.md)

# Cite

If you use USCDetector in your research, please cite our paper:

  ```
  @inproceedings{li2024characterizing,
  title={Characterizing Ethereum Upgradable Smart Contracts and Their Security Implications},
  author={Li, Xiaofan and Yang, Jin and Chen, Jiaqi and Tang, Yuzhe and Gao, Xing},
  booktitle={Proceedings of the ACM on Web Conference 2024},
  pages={1847--1858},
  year={2024}
}
  ```
