# Mini Blockchain

A simplified blockchain implementation in Python for educational purposes, demonstrating core blockchain concepts including cryptographic hashing, transaction validation, and network communication.

## Overview

This project implements a basic blockchain system with a client-server architecture where clients can perform deposit and withdrawal operations with a virtual currency called "minicoins". The blockchain maintains transaction integrity through SHA-256 cryptographic hashing, with each block linked to its predecessor.

## Features

- **Client-Server Architecture**: TCP/IP communication between multiple clients and a central server
- **Blockchain Implementation**: Tamper-evident chain of blocks with cryptographic hashing
- **Transaction Types**: 
  - Account registration (name)
  - Deposits (add minicoins)
  - Withdrawals (remove minicoins)
- **Special Block Types**:
  - Standard transaction blocks
  - Account creation blocks (for first deposits with timestamps)
- **Concurrency Support**: Multi-threaded server handling multiple simultaneous clients
- **Graceful Shutdown**: Signal handlers for clean termination (SIGINT, SIGTERM, SIGHUP)
- **Input Modes**: Interactive (stdin) and automated (file-based) client operation

## Architecture

### Core Components

#### Server (`src/models/server.py`)
- Maintains the blockchain state
- Handles concurrent client connections using threading
- Validates transactions and blockchain integrity
- Protected shared state with thread locks

#### Client (`src/models/client.py`)
- Connects to the server via TCP
- Sends operations (deposit, withdraw, quit)
- Supports both interactive and automated modes

#### Block (`src/models/block.py`)
- Stores transaction data (owner, amount, operation)
- Serializable for hash computation
- Linked to previous block via cryptographic hash

#### AccCreationBlock (`src/models/acc_creation_block.py`)
- Special block for first client deposit
- Includes account creation timestamp
- Inherits from Block class

#### Hash (`src/models/hash.py`)
- Computes SHA-256 hashes for blocks
- Validates individual blocks and entire blockchain
- Implements tamper-detection mechanism

#### Transaction Handler (`src/models/transaction_handler.py`)
- Validates transaction rules
- Creates appropriate block types
- Manages client balances
- Prevents overdrafts

## Installation

### Prerequisites

- Python 3.11.2 (or compatible version)
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Andre-Grassi/mini_blockchain.git
cd mini_blockchain
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

This will create a virtual environment and install the package in editable mode.

3. Activate the virtual environment:
```bash
source .venv/bin/activate
```

## Usage

### Starting the Server

```bash
python3 src/run_server.py <port>
```

Example:
```bash
python3 src/run_server.py 8080
```

The server will display its IP address and start listening for client connections.

### Running a Client

#### Interactive Mode

```bash
python3 src/run_client.py <client_name> <server_ip> <server_port>
```

Example:
```bash
python3 src/run_client.py Alice 127.0.0.1 8080
```

Available commands:
- `deposit <amount>` - Deposit minicoins
- `withdraw <amount>` - Withdraw minicoins
- `q` - Quit

#### Automated Mode (File Input)

```bash
python3 src/run_client.py <client_name> <server_ip> <server_port> --input <file>
```

Example:
```bash
python3 src/run_client.py Bob 127.0.0.1 8080 --input tests/inputs/correct.txt
```

Input file format (one command per line):
```
deposit 100
withdraw 50
q
```

### Running Tests

The project includes test scenarios in `tests/inputs/`:
- `correct.txt` - Valid transaction sequence
- `incorrect_withdraw.txt` - Attempted overdraft
- `incorrect_withdraw2.txt` - Withdrawal without deposit
- `unknown.txt` - Unknown commands

Run automated tests:
```bash
cd tests
python3 auto_execution.py <server_ip> <server_port>
```

## Project Structure

```
mini_blockchain/
├── src/
│   ├── run_server.py          # Server entry point
│   ├── run_client.py          # Client entry point
│   └── models/
│       ├── server.py          # Server implementation
│       ├── client.py          # Client implementation
│       ├── block.py           # Block class
│       ├── acc_creation_block.py  # Account creation block
│       ├── hash.py            # Hashing utilities
│       ├── transaction_handler.py # Transaction logic
│       ├── operation.py       # Operation enum
│       └── network_node.py    # Base network class
├── tests/
│   ├── auto_execution.py      # Automated test runner
│   ├── inputs/                # Test input files
│   └── logs/                  # Test execution logs
├── docs/                      # Sphinx documentation
├── site/                      # Project website
├── setup.sh                   # Setup script
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## How It Works

### Transaction Flow

1. **Client Registration**: Client connects and sends name to server
2. **Operation Request**: Client sends deposit/withdraw command
3. **Validation**: Server validates transaction (balance check, amount > 0)
4. **Block Creation**: Server creates appropriate block type
5. **Hash Computation**: Server computes SHA-256 hash (includes previous block's hash)
6. **Blockchain Validation**: Server validates entire chain integrity
7. **Response**: Server sends status back to client

### Blockchain Integrity

Each block's hash is computed from:
- Block's serialized data (owner, amount, operation)
- Previous block's hash (except genesis block)

This creates a tamper-evident chain where any modification to a block invalidates all subsequent blocks.

### Concurrency Model

- Server spawns a new thread for each client connection
- Shared blockchain state protected by threading locks
- Each client thread runs independently but synchronizes on state modifications

## Documentation

Generate API documentation using Sphinx:

```bash
./generate_docs.sh
```

View documentation:
```bash
open build/html/index.html
```

## Validation Rules

- Amounts must be positive
- Withdrawals cannot exceed current balance
- Client must register name before transactions
- Each block hash must be valid
- Genesis block validated separately
- Chain validated after each new block

## Error Handling

- Invalid operations return error messages
- Overdrafts rejected with balance info
- Corrupted blocks automatically removed
- Graceful shutdown on signals
- Socket timeouts for responsiveness

## Code Style

Follows [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

Configuration in `pylintrc`

## Authors

- Andre Grassi de Jesus
- Ricardo Faria

## License

Educational project for Networks II course (Redes 2)

## Contributing

This is an educational project. Feel free to fork and experiment!

## Notes

- This is a simplified blockchain for learning purposes
- Not suitable for production use
- No mining or proof-of-work implementation
- Centralized server architecture (not peer-to-peer)
- No persistence layer (blockchain stored in memory)
