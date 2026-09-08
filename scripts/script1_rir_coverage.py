import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("Loading datasets...")
df4 = pd.read_parquet('../data/prefix_tags_2025-04-01_v4.parquet')
df6 = pd.read_parquet('../data/prefix_tags_2025-04-01_v6.parquet')
print(f"IPv4 rows: {len(df4):,}  |  IPv6 rows: {len(df6):,}")

# ── CLAIM 1: Overall Coverage ─────────────────────────────────────────────
print("\n" + "="*55)
print("CLAIM 1: Overall ROA Coverage")
print("="*55)

v4_valid = (df4['RPKI Status'] == 'Valid').sum()
v6_valid = (df6['RPKI Status'] == 'Valid').sum()
pct4 = v4_valid / len(df4) * 100
pct6 = v6_valid / len(df6) * 100

print(f"IPv4: {v4_valid:,} / {len(df4):,} = {pct4:.1f}%  (Paper: ~51.5%)")
print(f"IPv6: {v6_valid:,} / {len(df6):,} = {pct6:.1f}%  (Paper: ~61.7%)")

# ── CLAIM 2: RIR-wise Coverage ────────────────────────────────────────────
print("\n" + "="*55)
print("CLAIM 2: RIR-wise IPv4 ROA Coverage")
print("="*55)

# Fix: handle NaN in RPKI Status before filtering
df4_clean = df4.copy()
df4_clean['RPKI Status'] = df4_clean['RPKI Status'].fillna('Unknown')

rir_total    = df4_clean.groupby('RIR')['prefix'].count()
rir_valid    = df4_clean[df4_clean['RPKI Status'] == 'Valid'].groupby('RIR')['prefix'].count()
rir_invalid  = df4_clean[df4_clean['RPKI Status'].str.contains('Invalid', na=False)].groupby('RIR')['prefix'].count()
rir_notfound = df4_clean[df4_clean['RPKI Status'] == 'NotFound'].groupby('RIR')['prefix'].count()

rir_pct_valid    = (rir_valid.reindex(rir_total.index, fill_value=0)    / rir_total * 100).round(1)
rir_pct_invalid  = (rir_invalid.reindex(rir_total.index, fill_value=0)  / rir_total * 100).round(1)
rir_pct_notfound = (rir_notfound.reindex(rir_total.index, fill_value=0) / rir_total * 100).round(1)

print(f"\n{'RIR':<10} {'Total':>10} {'Valid%':>8} {'Invalid%':>10} {'NotFound%':>11}")
print("-"*52)
for rir in rir_total.index:
    print(f"{rir:<10} {rir_total[rir]:>10,} {rir_pct_valid[rir]:>8.1f} {rir_pct_invalid[rir]:>10.1f} {rir_pct_notfound[rir]:>11.1f}")

# ── FIGURE 1: Stacked bar — RIR wise ─────────────────────────────────────
rirs = ['RIPE', 'LACNIC', 'APNIC', 'ARIN', 'AFRINIC']
rirs = [r for r in rirs if r in rir_pct_valid.index]

v_vals  = [rir_pct_valid[r]    for r in rirs]
i_vals  = [rir_pct_invalid[r]  for r in rirs]
nf_vals = [rir_pct_notfound[r] for r in rirs]
x = np.arange(len(rirs))

fig, ax = plt.subplots(figsize=(10, 6))
b1 = ax.bar(x, v_vals,  0.5, label='Valid (ROA Found)',  color='#2196F3', edgecolor='white')
b2 = ax.bar(x, i_vals,  0.5, bottom=v_vals,              label='Invalid',  color='#F44336', edgecolor='white')
b3 = ax.bar(x, nf_vals, 0.5,
            bottom=[a+b for a,b in zip(v_vals,i_vals)],  label='Not Found', color='#BDBDBD', edgecolor='white')

for i, v in enumerate(v_vals):
    if v > 3:
        ax.text(i, v/2, f'{v:.1f}%', ha='center', va='center',
                fontsize=9, color='white', fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(rirs, fontsize=11)
ax.set_ylabel('Percentage of IPv4 Prefixes (%)', fontsize=12)
ax.set_title('Figure 1 Reproduced: RIR-wise IPv4 ROA Coverage (April 2025)',
             fontsize=13, fontweight='bold')
ax.set_ylim(0, 108)
ax.legend(loc='upper right', fontsize=10)
ax.yaxis.grid(True, linestyle='--', alpha=0.4)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('../output/figure1_rir_coverage.png', dpi=150, bbox_inches='tight')
print("\nSaved: output/figure1_rir_coverage.png")
plt.show()

# ── FIGURE 2: IPv4 vs IPv6 overall ───────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(7, 5))
cats = ['IPv4', 'IPv6']
cov  = [pct4, pct6]
uncov= [100-pct4, 100-pct6]
x2   = np.arange(2)
ax2.bar(x2, cov,  0.4, label='Covered by ROA',  color='#2196F3', edgecolor='white')
ax2.bar(x2, uncov,0.4, bottom=cov,               label='Not Covered', color='#BDBDBD', edgecolor='white')
for i, v in enumerate(cov):
    ax2.text(i, v/2, f'{v:.1f}%', ha='center', va='center',
             fontsize=13, color='white', fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(cats, fontsize=12)
ax2.set_ylabel('Percentage (%)', fontsize=12)
ax2.set_title('Figure 2 Reproduced: Overall ROA Coverage IPv4 vs IPv6\n(April 2025)',
              fontsize=13, fontweight='bold')
ax2.set_ylim(0, 115)
ax2.legend(fontsize=10)
ax2.yaxis.grid(True, linestyle='--', alpha=0.4)
ax2.set_axisbelow(True)
plt.tight_layout()
plt.savefig('../output/figure2_overall_coverage.png', dpi=150, bbox_inches='tight')
print("Saved: output/figure2_overall_coverage.png")
plt.show()

print("\nScript 1 COMPLETE!")
