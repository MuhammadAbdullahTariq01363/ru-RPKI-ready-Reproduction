import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("Loading datasets...")
df4 = pd.read_parquet('../data/prefix_tags_2025-04-01_v4.parquet')
df6 = pd.read_parquet('../data/prefix_tags_2025-04-01_v6.parquet')

# ── Fix: Tag List is numpy.ndarray — use correct checker ─────────────────
def has_tag(tag_series, tag):
    """Check if a tag exists in a numpy array Tag List"""
    def check(x):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return False
        if isinstance(x, np.ndarray):
            return tag in x
        if isinstance(x, list):
            return tag in x
        return False
    return tag_series.apply(check)

# ── Show all unique tags first ────────────────────────────────────────────
print("\nAll unique tags in dataset:")
all_tags = set()
for val in df4['Tag List'].dropna():
    if isinstance(val, np.ndarray):
        all_tags.update(val.tolist())
    elif isinstance(val, list):
        all_tags.update(val)
for t in sorted(all_tags):
    print(f"  '{t}'")

# ── CLAIM 3: Low-Hanging Fruit ────────────────────────────────────────────
print("\n" + "="*55)
print("CLAIM 3: Low-Hanging Fruit Analysis")
print("="*55)

uncov4 = df4[df4['RPKI Status'] == 'NotFound'].copy()
uncov6 = df6[df6['RPKI Status'] == 'NotFound'].copy()
print(f"\nUncovered IPv4 prefixes: {len(uncov4):,}")
print(f"Uncovered IPv6 prefixes: {len(uncov6):,}")

# Low-Hanging = Certified + Leaf + Same SKI pfx,ASN + No ROA Org
# (org already has RPKI but hasn't issued ROA for this prefix)
lh4 = (
    has_tag(uncov4['Tag List'], 'Certified') &
    has_tag(uncov4['Tag List'], 'Leaf') &
    has_tag(uncov4['Tag List'], 'Same SKI pfx,ASN')
).sum()

lh6 = (
    has_tag(uncov6['Tag List'], 'Certified') &
    has_tag(uncov6['Tag List'], 'Leaf') &
    has_tag(uncov6['Tag List'], 'Same SKI pfx,ASN')
).sum()

lh4_pct = lh4 / len(uncov4) * 100
lh6_pct = lh6 / len(uncov6) * 100

print(f"\nLow-Hanging IPv4: {lh4:,} / {len(uncov4):,} = {lh4_pct:.1f}%")
print(f"Low-Hanging IPv6: {lh6:,} / {len(uncov6):,} = {lh6_pct:.1f}%")
print(f"\nPaper claims: IPv4 = 47%,  IPv6 = 71%")
print(f"My results:   IPv4 = {lh4_pct:.1f}%, IPv6 = {lh6_pct:.1f}%")
print(f"Difference:   IPv4 = {abs(lh4_pct-47):.1f}pp, IPv6 = {abs(lh6_pct-71):.1f}pp")

# ── Also check Certified breakdown ───────────────────────────────────────
cert4   = has_tag(uncov4['Tag List'], 'Certified').sum()
uncert4 = has_tag(uncov4['Tag List'], 'Uncertified').sum()
print(f"\nCertified (uncovered IPv4):   {cert4:,} ({cert4/len(uncov4)*100:.1f}%)")
print(f"Uncertified (uncovered IPv4): {uncert4:,} ({uncert4/len(uncov4)*100:.1f}%)")

# ── FIGURE: Pie charts ────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 6))

for ax, pct, total, label, color in [
    (axes[0], lh4_pct, len(uncov4), 'IPv4', '#2196F3'),
    (axes[1], lh6_pct, len(uncov6), 'IPv6', '#4CAF50'),
]:
    if pct > 0:
        slices = [pct, 100-pct]
        colors = [color, '#E0E0E0']
        wedges, texts, autotexts = ax.pie(
            slices, colors=colors, autopct='%1.1f%%',
            startangle=90, pctdistance=0.75,
            wedgeprops=dict(edgecolor='white', linewidth=2)
        )
        autotexts[0].set_fontsize(13)
        autotexts[0].set_fontweight('bold')
        autotexts[0].set_color('white')
    else:
        ax.pie([100], colors=['#E0E0E0'],
               wedgeprops=dict(edgecolor='white', linewidth=2))
        ax.text(0, 0, '0.0%', ha='center', va='center',
                fontsize=14, fontweight='bold', color='gray')
    ax.set_title(f'{label} Uncovered Prefixes\n(n={total:,})',
                 fontsize=12, fontweight='bold')

axes[0].legend(['Low-Hanging\n(Certified+Leaf+SameSKI)', 'Other (harder to fix)'],
               loc='lower center', bbox_to_anchor=(0.5, -0.15), fontsize=9)

fig.suptitle('Figure 3 Reproduced: Low-Hanging Fruit Analysis\n'
             'Uncovered Prefixes That Could Be Fixed Easily (April 2025)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('../output/figure3_low_hanging.png', dpi=150, bbox_inches='tight')
print("\nSaved: output/figure3_low_hanging.png")
plt.show()

print("\nScript 2 COMPLETE!")
