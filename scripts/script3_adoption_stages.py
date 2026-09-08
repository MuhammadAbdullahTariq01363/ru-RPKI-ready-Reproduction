import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("Loading datasets...")
df4 = pd.read_parquet('../data/prefix_tags_2025-04-01_v4.parquet')
df6 = pd.read_parquet('../data/prefix_tags_2025-04-01_v6.parquet')

def has_tag(tag_series, tag):
    def check(x):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return False
        if isinstance(x, (np.ndarray, list)):
            return tag in x
        return False
    return tag_series.apply(check)

total4 = len(df4)

# ── ADOPTION STAGES (Rogers Model) ───────────────────────────────────────
print("\n" + "="*55)
print("RPKI ADOPTION STAGES - IPv4")
print("="*55)

# Stage 5: Fully Adopted — Valid ROA
s5 = (df4['RPKI Status'] == 'Valid').sum()

# Stage 4: RPKI-Ready — Certified + Leaf + Same SKI + NotFound
notfound4 = df4[df4['RPKI Status'] == 'NotFound']
s4 = (
    has_tag(notfound4['Tag List'], 'Certified') &
    has_tag(notfound4['Tag List'], 'Leaf') &
    has_tag(notfound4['Tag List'], 'Same SKI pfx,ASN')
).sum()

# Stage 3: Certified + Leaf + Diff SKI (different org holds cert)
s3 = (
    has_tag(notfound4['Tag List'], 'Certified') &
    has_tag(notfound4['Tag List'], 'Leaf') &
    has_tag(notfound4['Tag List'], 'Diff SKI pfx,ASN')
).sum()

# Stage 2: Certified + Reassigned (prefix given to customer)
s2 = (
    has_tag(notfound4['Tag List'], 'Certified') &
    has_tag(notfound4['Tag List'], 'Reassigned')
).sum()

# Stage 1: Uncertified (no RPKI certificate at all)
s1 = has_tag(df4['Tag List'], 'Uncertified').sum()

stages = {
    'Stage 1\nUncertified\n(Unaware)':      s1,
    'Stage 2\nReassigned\n(Aware)':          s2,
    'Stage 3\nDiff-SKI Leaf\n(Persuaded)':   s3,
    'Stage 4\nRPKI-Ready\n(Planning)':       s4,
    'Stage 5\nROA Valid\n(Adopted)':         s5,
}

print(f"\n{'Stage':<35} {'Count':>10} {'Pct':>8}")
print("-"*55)
for stage, count in stages.items():
    label = stage.replace('\n', ' ')
    print(f"{label:<35} {count:>10,} {count/total4*100:>7.1f}%")

accounted = sum(stages.values())
print(f"\n{'Total accounted:':<35} {accounted:>10,}")
print(f"{'Total prefixes:':<35} {total4:>10,}")

# ── FIGURE: Adoption Stages Bar ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
labels = list(stages.keys())
counts = list(stages.values())
pcts   = [c / total4 * 100 for c in counts]
colors = ['#F44336', '#FF9800', '#FFC107', '#8BC34A', '#2196F3']

bars = ax.bar(labels, pcts, color=colors, edgecolor='white', linewidth=1.5, width=0.6)

for bar, pct, count in zip(bars, pcts, counts):
    ax.text(bar.get_x() + bar.get_width()/2,
            bar.get_height() + 0.3,
            f'{pct:.1f}%\n({count:,})',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_ylabel('Percentage of IPv4 Prefixes (%)', fontsize=12)
ax.set_title('Figure 4 Reproduced: RPKI Adoption Stages (Rogers Model)\n'
             'IPv4 Prefixes by Stage — April 2025',
             fontsize=13, fontweight='bold')
ax.set_ylim(0, max(pcts) * 1.3)
ax.yaxis.grid(True, linestyle='--', alpha=0.4)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig('../output/figure4_adoption_stages.png', dpi=150, bbox_inches='tight')
print("\nSaved: output/figure4_adoption_stages.png")
plt.show()

# ── FINAL SUMMARY ─────────────────────────────────────────────────────────
print("\n" + "="*55)
print("FINAL SUMMARY — COMPARE WITH PAPER")
print("="*55)
v4p = s5/total4*100
v6p = (df6['RPKI Status']=='Valid').sum()/len(df6)*100
lh4p= s4/len(notfound4)*100
lh6_notfound = df6[df6['RPKI Status']=='NotFound']
lh6 = (
    has_tag(lh6_notfound['Tag List'],'Certified') &
    has_tag(lh6_notfound['Tag List'],'Leaf') &
    has_tag(lh6_notfound['Tag List'],'Same SKI pfx,ASN')
).sum()
lh6p = lh6/len(lh6_notfound)*100

print(f"\n{'Metric':<35} {'Paper':>10} {'Mine':>10} {'Diff':>8}")
print("-"*65)
print(f"{'IPv4 ROA Coverage':<35} {'~51.5%':>10} {v4p:>9.1f}% {abs(v4p-51.5):>7.1f}pp")
print(f"{'IPv6 ROA Coverage':<35} {'~61.7%':>10} {v6p:>9.1f}% {abs(v6p-61.7):>7.1f}pp")
print(f"{'Low-Hanging IPv4':<35} {'~47%':>10} {lh4p:>9.1f}% {abs(lh4p-47):>7.1f}pp")
print(f"{'Low-Hanging IPv6':<35} {'~71%':>10} {lh6p:>9.1f}% {abs(lh6p-71):>7.1f}pp")

print("\nAll done! Check output/ folder for all 4 figures.")
