import json, os
from datetime import datetime, timezone
from kafka import KafkaConsumer, TopicPartition
import pandas as pd

os.makedirs("lakehouse/bronze", exist_ok=True)
consumer = KafkaConsumer(
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False,
)
tp = TopicPartition('tymebank.transactions', 0)
consumer.assign([tp])
consumer.seek_to_beginning(tp)
print("Assigned to partition 0, seeking to beginning...")
rows = []
skipped = 0
empty = 0
while empty < 3:
    records = consumer.poll(timeout_ms=5000)
    if not records:
        empty += 1
        print(f"Empty poll {empty}/3, have {len(rows)} so far, skipped {skipped} bad...")
        continue
    empty = 0
    for msgs in records.values():
        for msg in msgs:
            try:
                raw = msg.value.decode('utf-8').strip()
                if not raw:
                    skipped += 1
                    continue
                r = json.loads(raw)
            except Exception as e:
                skipped += 1
                print(f"Skipped offset {msg.offset}: {e}")
                continue
            r['_kafka_offset'] = msg.offset
            r['_ingested_at'] = datetime.now(timezone.utc).isoformat()
            r['_source'] = 'kafka:tymebank.transactions'
            rows.append(r)
    print(f"Bronze received {len(rows)}... skipped {skipped}")
print(f"Bronze DONE. Total: {len(rows)} Skipped bad: {skipped}")
with open("lakehouse/bronze/transactions.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
df = pd.DataFrame(rows)
df.to_parquet("lakehouse/bronze/transactions.parquet", index=False)
print(df.head(2).to_string())
print("Saved to lakehouse/bronze/")
