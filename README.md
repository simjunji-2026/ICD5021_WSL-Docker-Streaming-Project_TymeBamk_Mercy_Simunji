# TymeBank Real-Time Lakehouse

CSV -> Kafka -> Bronze -> Silver -> Gold

## Pipeline
1. Producer: producer.py reads CSV -> Kafka topic tymebank.transactions
2. Bronze: bronze_consumer.py uses assign() + seek_to_beginning(), skips bad JSON, saves 522 rows
3. Silver: silver.py drops test rows, cleans ACCT_NO, REQAMT -> amount, dedupes. Saves 520 rows
4. Gold: gold.py aggregates to lakehouse/gold/ - summary, by_merchant (89), by_city (12), by_status (2), by_terminal (3)

## Results
- Total Silver: 520 transactions
- Total Amount: ~R19.87M, Avg: R38,212, Max: R129,505
- Top City: Johannesburg - 95 txns, R3.87M
- Status: SUCCESS 384 (R14.17M) vs DECLINED 136 (R5.70M) = 26% decline rate
- Terminal: ATM 187, ECOM 169, POS 164

## Run
docker ps
python3 producer.py
python3 bronze_consumer.py
python3 silver.py
python3 gold.py

## Tech
Python, Apache Kafka (Docker), kafka-python, Pandas, Parquet, WSL Ubuntu

## Demo Video 
Watch the demo here: https://drive.google.com/file/d/1vMupJexOIPTUSPV5-LlciqAg0mjPSNo8/view?usp=sharing

