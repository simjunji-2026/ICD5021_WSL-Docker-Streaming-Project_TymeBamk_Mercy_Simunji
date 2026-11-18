import pandas as pd, os
os.makedirs("lakehouse/gold", exist_ok=True)
df = pd.read_parquet("lakehouse/silver/transactions.parquet")
print(f"Silver in: {len(df)}")

gold = {}
gold['summary'] = pd.DataFrame([{
    'total_transactions': len(df),
    'total_amount': df['amount'].sum(),
    'avg_amount': df['amount'].mean(),
    'max_amount': df['amount'].max(),
    'min_amount': df['amount'].min(),
    'unique_accounts': df['ACCT_NO'].nunique(),
}])

# By merchant / city / status - only if column exists
for col, name in [('MERCHANT','by_merchant'), ('ADDRESS_CITY','by_city'), ('TRANS_STAT','by_status'), ('TERMINAL_TYPE','by_terminal')]:
    if col in df.columns:
        g = df.groupby(col).agg(transactions=('amount','count'), total_amount=('amount','sum'), avg_amount=('amount','mean')).reset_index().sort_values('total_amount', ascending=False)
        gold[name] = g
        print(f"\n--- {name} ---")
        print(g.head(5).to_string())

for name, g in gold.items():
    g.to_parquet(f"lakehouse/gold/{name}.parquet", index=False)
    print(f"Saved lakehouse/gold/{name}.parquet - {len(g)} rows")

print("\nGold DONE. All layers complete: Bronze -> Silver -> Gold")
