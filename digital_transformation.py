import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------------------
# 1. آماده‌سازی داده‌ها
# ---------------------------
data = {
    "Year": [2020, 2021, 2022, 2023],
    "UAE": [65, 70, 78, 85],
    "Turkey": [40, 50, 55, 62],
    "Iran": [35, 38, 40, 45],
    "India": [50, 58, 70, 80],
    "Singapore": [75, 80, 85, 90],
}
df = pd.DataFrame(data)

# ---------------------------
# 2. محاسبه شاخص‌ها
# ---------------------------
start, end = 2020, 2023
periods = end - start

metrics = []
for country in ["UAE", "Turkey", "Iran", "India", "Singapore"]:
    v0 = float(df.loc[df["Year"] == start, country].values[0])
    vN = float(df.loc[df["Year"] == end, country].values[0])
    growth_abs = vN - v0
    cagr = (vN / v0) ** (1 / periods) - 1
    metrics.append({
        "Country": country,
        "Start": v0,
        "End": vN,
        "AbsGrowth": growth_abs,
        "CAGR": cagr
    })

metrics_df = pd.DataFrame(metrics)

# ---------------------------
# 3. رهبران و رتبه‌بندی
# ---------------------------
top_abs = max(metrics, key=lambda x: x["AbsGrowth"])
top_cagr = max(metrics, key=lambda x: x["CAGR"])
rank_end = metrics_df.sort_values("End", ascending=False)

# ---------------------------
# 4. ذخیره خروجی‌ها
# ---------------------------
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

# Excel
excel_path = os.path.join(output_dir, "metrics.xlsx")
metrics_df.to_excel(excel_path, index=False)
print(f"[ok] Saved Excel: {excel_path}")

# Markdown
md_path = os.path.join(output_dir, "insights.md")
lines = []
lines.append("# Digital Transformation Insights (2020–2023)\n")
lines.append("## Key Highlights\n")
lines.append(f"- Highest Absolute Growth: **{top_abs['Country']}** (+{top_abs['AbsGrowth']:.1f})")
lines.append(f"- Highest CAGR: **{top_cagr['Country']}** ({top_cagr['CAGR']*100:.2f}%)")
lines.append(f"- Leader in {end}: **{rank_end.iloc[0]['Country']}** ({rank_end.iloc[0]['End']})\n")
lines.append("## Metrics Table\n")
lines.append(metrics_df.to_markdown(index=False))

with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"[ok] Saved Markdown: {md_path}")

# ---------------------------
# 5. نمودار روند
# ---------------------------
plt.figure(figsize=(8, 5))
for country in ["UAE", "Turkey", "Iran", "India", "Singapore"]:
    plt.plot(df["Year"], df[country], marker="o", label=country)

plt.title("Digital Transformation Index (2020–2023)")
plt.xlabel("Year")
plt.ylabel("Index Value")
plt.legend()
plt.grid(True)

chart_path = os.path.join(output_dir, "chart.png")
plt.savefig(chart_path, dpi=150)
plt.close()
print(f"[ok] Saved Chart: {chart_path}")
