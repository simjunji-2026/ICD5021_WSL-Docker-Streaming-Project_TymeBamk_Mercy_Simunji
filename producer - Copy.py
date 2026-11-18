import csv, json, time, glob
from kafka import KafkaProducer

# Find the CSV no matter the capital/small letters
csv_file = glob.glob("*.csv")[0]
print(f"Using file: {csv_file}")

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
print("Producer started... Streaming TymeBank CSV...")

count = 0
with open(csv_file, newline='', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    print("Columns:", reader.fieldnames)
    for row in reader:
        data = {
            "ACCT_NO": row.get("ACCT_NO"),
            "ACTAMT": row.get("ACTAMT"),
            "REQAMT": row.get("REQAMT"),
            "ADDRESS_CITY": row.get("ADDRESS_CITY"),
            "MERCHANT": row.get("MERCHANT"),
            "TRANS_STAT": row.get("TRANS_STAT"),
            "TERMINAL_TYPE": row.get("TERMINAL_TYPE"),
            "AUTH_START": row.get("AUTH_START"),
            "TRACE": row.get("TRACE"),
            "REFNUM": row.get("REFNUM")
        }
        producer.send("tymebank.transactions", value=data)
        count += 1
        if count % 50 == 0:
            print(f"Sent {count}...")
        time.sleep(0.1)

producer.flush()
print(f"Done. Total sent: {count}")
