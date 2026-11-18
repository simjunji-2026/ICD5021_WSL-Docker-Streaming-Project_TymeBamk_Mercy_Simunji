import pandas as pd

df = pd.read_parquet("lakehouse/bronze/transactions.parquet")
print(f"Bronze in: {len(df)} rows, {len(df.columns)} cols")

# Keep only real TymeBank rows (drop the test 'account 123' rows)
df = df[df['ACCT_NO'].notna()].copy()
print(f"After dropping test rows: {len(df)}")

# Clean
df['ACCT_NO'] = df['ACCT_NO'].astype(str).str.strip()
# Amount column in your CSV is REQAMT
if 'REQAMT' in df.columns:
    df['amount'] = pd.to_numeric(df['REQAMT'], errors='coerce')
df = df.dropna(subset=['amount'])
df = df.drop_duplicates()
df['_silver_at'] = pd.Timestamp.now(tz='UTC').isoformat()

df.to_parquet("lakehouse/silver/transactions.parquet", index=False) if False else None
import os
os.makedirs("lakehouse/silver", exist_ok=True)
df.to_parquet("lakehouse/silver/transactions.parquet", index=False)
print(f"Silver DONE. Total: {len(df)}")
print(df[['ACCT_NO','amount']].head(3).to_string())
print(df['amount'].describe().to_string())
