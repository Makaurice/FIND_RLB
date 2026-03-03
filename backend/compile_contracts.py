"""Helper to compile solidity contracts using solcx.

Usage:
    python compile_contracts.py

Writes ABI and bytecode into ``backend/compiled`` directory for later deployment.
"""
import os
from solcx import compile_standard, install_solc

CONTRACT_DIR = os.path.join(os.path.dirname(__file__), '..', 'contracts')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'compiled')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ensure solc is installed
install_solc('0.8.20')

# gather all .sol files
sources = {}
for fname in os.listdir(CONTRACT_DIR):
    if fname.endswith('.sol'):
        path = os.path.join(CONTRACT_DIR, fname)
        with open(path, 'r') as f:
            sources[fname] = {'content': f.read()}

compiled = compile_standard({
    'language': 'Solidity',
    'sources': sources,
    'settings': {
        'outputSelection': {
            '*': {
                '*': ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
            }
        }
    }
}, solc_version='0.8.20')

# save each contract ABI and bytecode
for fname, file_output in compiled['contracts'].items():
    for contract_name, artifact in file_output.items():
        safe_name = f"{fname.replace('.sol','')}_{contract_name}"
        abi_path = os.path.join(OUTPUT_DIR, f"{safe_name}.abi.json")
        bin_path = os.path.join(OUTPUT_DIR, f"{safe_name}.bin")
        with open(abi_path, 'w') as abi_file:
            import json
            json.dump(artifact['abi'], abi_file)
        with open(bin_path, 'w') as bin_file:
            bin_file.write(artifact['evm']['bytecode']['object'])
        print(f"Compiled {safe_name}")
