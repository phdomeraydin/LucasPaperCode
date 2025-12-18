# pip install matplotlib numpy
import matplotlib.pyplot as plt
from math import comb

# -----------------------------
# Helper functions
# -----------------------------

def catalan(k: int) -> int:
    """Catalan number: C_k = binom(2k, k) / (k+1)."""
    return comb(2 * k, k) // (k + 1)

def lucas_upto(n: int):
    """Lucas numbers up to n: L0=2, L1=1, Ln=Ln-1+Ln-2."""
    L = [0] * (n + 1)
    if n >= 0:
        L[0] = 2
    if n >= 1:
        L[1] = 1
    for i in range(2, n + 1):
        L[i] = L[i - 1] + L[i - 2]
    return L

# -----------------------------
# Data used in the figure
# -----------------------------

# x-axis values
n_vals = [5, 6, 7, 8, 9, 10, 12]

# Catalan triangulation counts: C_{n-2}
catalan_counts = [catalan(n - 2) for n in n_vals]

# Encoding counts (Lucas-based): L_{n-2}
L = lucas_upto(max(n_vals))
encoding_counts = [L[n - 2] for n in n_vals]

# -----------------------------
# Plot
# -----------------------------

plt.figure(figsize=(9.2, 4.8))

# Catalan count — orange
plt.plot(
    n_vals,
    catalan_counts,
    color="orange",
    marker="o",
    linewidth=2,
    label="Catalan count"
)

# Encoding count — blue
plt.plot(
    n_vals,
    encoding_counts,
    color="dodgerblue",
    marker="s",
    linestyle="--",
    linewidth=2,
    label="Encoding count"
)

plt.yscale("log")
plt.xlabel("n (number of vertices)")
plt.ylabel("Count (log scale)")
plt.grid(True, which="both", linestyle=":", linewidth=0.8)
plt.legend(loc="upper left")

plt.tight_layout()
plt.savefig("figure2.png", dpi=300, bbox_inches="tight")
plt.show()
