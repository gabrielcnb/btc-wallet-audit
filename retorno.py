from datetime import datetime
import os
import requests
import json
import time

def get_wallet_address():
    address = os.getenv("BITCOIN_ADDRESS")
    if not address:
        raise ValueError("Set the BITCOIN_ADDRESS environment variable.")
    return address

def get_current_bitcoin_price():
    """Obtém o preço atual do Bitcoin em EUR."""
    try:
        url = "https://api.blockchain.com/v3/exchange/tickers/BTC-EUR"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data['last_trade_price'])
    except Exception as e:
        raise Exception(f"Não foi possível obter o preço atual do Bitcoin: {str(e)}")

def get_wallet_balance(address):
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance_satoshi = data.get('final_balance')
        if balance_satoshi is None:
            raise Exception("Não foi possível obter o saldo da carteira")
        return balance_satoshi / 100000000
    except Exception as e:
        raise Exception(f"Erro ao obter saldo da carteira: {str(e)}")

def calculate_transaction_fee(tx):
    total_input = sum(input_tx.get('prev_out', {}).get('value', 0) 
                     for input_tx in tx.get('inputs', []))
    total_output = sum(output.get('value', 0) 
                      for output in tx.get('out', []))
    return (total_input - total_output) / 100000000

def get_historical_price(timestamp):
    try:
        date_str = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y')
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={date_str}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['market_data']['current_price'].get('eur')
    except Exception as e:
        return None

def get_transaction_data(address):
    print(f"Consultando transações para o endereço: {address}")
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        print("Conectando à API da Blockchain.info...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        transactions = []
        for tx in data.get('txs', []):
            timestamp = tx.get('time', 0)
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            fee_btc = calculate_transaction_fee(tx)
            received_value = sum(out.get('value', 0) for out in tx.get('out', []) 
                               if out.get('addr') == address)
            sent_value = sum(input_tx.get('prev_out', {}).get('value', 0) 
                           for input_tx in tx.get('inputs', [])
                           if input_tx.get('prev_out', {}).get('addr') == address)
            net_value = received_value - sent_value
            if net_value != 0:
                amount_btc = net_value / 100000000
                historical_price = get_historical_price(timestamp)
                if historical_price is not None:
                    historical_value = abs(amount_btc * historical_price)
                else:
                    current_price = get_current_bitcoin_price()
                    historical_value = abs(amount_btc * current_price)
                    print(f"Aviso: Usando preço atual para a transação de {date}")
                time.sleep(1.5)
                transactions.append({
                    "date": date,
                    "amount_btc": amount_btc,
                    "value_eur_at_time": historical_value,
                    "fee_btc": fee_btc,
                    "hash": tx.get('hash')
                })
        return transactions
    except Exception as e:
        raise Exception(f"Erro ao obter dados das transações: {str(e)}")

def process_transactions(transactions):
    print("\nHistórico de Transações:")
    print("-" * 80)
    for transaction in transactions:
        print(f"Data: {transaction['date']}")
        print(f"Hash: {transaction['hash']}")
        print(f"Quantidade BTC: {transaction['amount_btc']:.8f}")
        print(f"Valor na época: {transaction['value_eur_at_time']:.2f} EUR")
        print(f"Taxa: {transaction['fee_btc']:.8f} BTC")
        print("-" * 80)
    try:
        wallet_balance = get_wallet_balance(get_wallet_address())
        current_price = get_current_bitcoin_price()
        current_value = wallet_balance * current_price
        print("\nValores Atuais:")
        print(f"Saldo BTC: {wallet_balance:.8f}")
        print(f"Preço atual do Bitcoin: {current_price:.2f} EUR")
        print(f"Valor atual da carteira: {current_value:.2f} EUR")
    except Exception as e:
        print(f"\nErro ao processar saldo atual: {str(e)}")

try:
    wallet_address = get_wallet_address()
    transactions = get_transaction_data(wallet_address)
    process_transactions(transactions)
except Exception as e:
    print(f"\nErro na execução do programa: {str(e)}")
