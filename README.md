# bitcoin-wallet-analyzer

CLI tool that fetches the full transaction history of a Bitcoin address and calculates the EUR value at the time of each transaction, plus the current wallet value.

## Features

- Fetches all transactions for a given Bitcoin address via blockchain.info
- Calculates net BTC flow per transaction (received minus sent), ignoring zero-net entries
- Retrieves historical BTC/EUR price at the date of each transaction via CoinDesk API
- Falls back to current BTC price when historical data is unavailable
- Calculates transaction fees in BTC (inputs minus outputs)
- Displays current wallet balance and EUR value using the live BTC/EUR price from blockchain.com
- Respects API rate limits with a 1.5-second delay between transaction lookups

## Stack

| Component | Choice |
|-----------|--------|
| Language | Python 3 |
| Blockchain data | blockchain.info REST API (free, no key) |
| Historical prices | CoinDesk BPI API (free, no key) |
| Live BTC/EUR price | blockchain.com Exchange API (free, no key) |
| HTTP client | requests |

## Setup / Installation

```bash
pip install requests
```

Set your Bitcoin address as an environment variable:

```bash
# Linux / macOS
export BITCOIN_ADDRESS="bc1q..."

# Windows (PowerShell)
$env:BITCOIN_ADDRESS = "bc1q..."

# Windows (cmd)
set BITCOIN_ADDRESS=bc1q...
```

## Usage

```bash
python retorno.py
```

Example output:

```
Consultando transações para o endereço: bc1q...
Conectando à API da Blockchain.info...

Histórico de Transações:
--------------------------------------------------------------------------------
Data: 2023-04-12
Hash: a1b2c3d4...
Quantidade BTC: 0.00250000
Valor na época: 68.42 EUR
Taxa: 0.00001200 BTC
--------------------------------------------------------------------------------

Valores Atuais:
Saldo BTC: 0.00250000
Preço atual do Bitcoin: 58320.00 EUR
Valor atual da carteira: 145.80 EUR
```

## File Structure

```
carteira bitcoin retorno/
└── retorno.py    # Single-file CLI application
```
