import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from deltalake import DeltaTable

city = DeltaTable("lakehouse/gold_delta_by_city").to_pandas()
status = DeltaTable("lakehouse/gold_delta_by_status").to_pandas()

fig, axes = plt.subplots(1, 2, figsize=(12,5))
axes[0].barh(city["ADDRESS_CITY"], city["total_amount"], color="#1f77b4")
axes[0].set_title("Total Amount by City (Gold Delta)")
axes[0].set_xlabel("Total Amount (R)")
axes[1].bar(status["status"], status["transactions"], color=["#2ca02c","#d62728"])
axes[1].set_title("Transactions by Status (Approved vs Declined)")
axes[1].set_ylabel("Transactions")
for i, v in enumerate(status["transactions"]):
    axes[1].text(i, v+1, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("dashboard.png", dpi=150)
print("Saved dashboard.png")
print(city.to_string())
print(status.to_string())
