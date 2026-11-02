import csv, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

src, out = sys.argv[1], sys.argv[2]
data = {}
with open(src) as f:
    for r in csv.DictReader(f):
        data.setdefault((r["as"], r["date_utc"]), [0] * 24)[int(r["hour_utc"])] = int(r["announcements"])

plt.rcParams.update({"font.family": "serif", "font.size": 9})
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=True)
hours = list(range(24))
for ax, asn, nome in zip(axes, ["AS30990", "AS8895"], ["Djibouti Telecom", "KACST"]):
    ax.bar([h + 0.3 for h in hours], data[(asn, "2024-02-23")], width=0.4,
           color="#9aa5b1", label="23/02/2024 (referência)")
    ax.bar([h + 0.7 for h in hours], data[(asn, "2024-02-24")], width=0.4,
           color="#c0392b", label="24/02/2024 (incidente)")
    ax.axvline(9 + 46 / 60, color="black", ls="--", lw=0.8)
    ax.text(10.1, 3.5e5, "cortes 09:46 / 09:51", fontsize=7)
    ax.set_yscale("log")
    ax.set_ylim(5, 1.5e6)
    ax.set_xticks(range(0, 25, 3)); ax.set_xlim(0, 24)
    ax.set_xlabel("hora (UTC)")
    ax.set_title(f"{asn} ({nome})", fontsize=9)
    ax.grid(axis="y", lw=0.3, alpha=0.6)
axes[0].set_ylabel("anúncios BGP por hora")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, fontsize=7, loc="lower center", ncol=2, frameon=False)
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(out)
