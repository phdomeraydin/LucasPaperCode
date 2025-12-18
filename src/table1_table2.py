# pip install pandas numpy
import pandas as pd
import numpy as np
from math import comb, log2

# -------------------------------------------------
# Core combinatorial sequences
# -------------------------------------------------

def catalan(k: int) -> int:
    """Compute the k-th Catalan number: C_k = binom(2k, k)/(k+1)."""
    return comb(2 * k, k) // (k + 1)

def fuss_catalan(m: int, n: int) -> int:
    """
    Compute the Fuss–Catalan number:
    FC(m, n) = 1 / (m*n + 1) * binom((m+1)*n, n)

    This corresponds to (m+2)-angulations of a polygon
    with N = m*n + 2 vertices.
    """
    return comb((m + 1) * n, n) // (m * n + 1)

def lucas_upto(N: int):
    """Generate Lucas numbers up to index N."""
    L = [0] * (N + 1)
    if N >= 0:
        L[0] = 2
    if N >= 1:
        L[1] = 1
    for i in range(2, N + 1):
        L[i] = L[i - 1] + L[i - 2]
    return L

# -------------------------------------------------
# Table 1: theoretical / structural results
# -------------------------------------------------

def compute_table1(m_values=(1, 2, 3), n_values=(2, 3, 4)):
    """
    Compute Table 1 results:
    - Triangulations (m=1)
    - (m+2)-angulations (m>=2)
    - Geometric counts
    - Lucas-based encoding counts
    """
    rows = []
    L = lucas_upto(50)

    for m in m_values:
        for n in n_values:
            if m == 1:
                # Triangulations of an (n+2)-gon
                N_vertices = n + 2
                geometric_count = catalan(n)
                structure = "Triangulations (m = 1)"
            else:
                # (m+2)-angulations of an (m*n + 2)-gon
                N_vertices = m * n + 2
                geometric_count = fuss_catalan(m, n)
                structure = f"(m+2)-Angulations (m = {m})"

            encoding_count = L[N_vertices - 2]

            rows.append({
                "Structure": structure,
                "m": m,
                "n": n,
                "Vertices (N)": N_vertices,
                "Geometric Count": geometric_count,
                "Encoding Count (Lucas)": encoding_count,
                "Encoding Length": N_vertices - 3,
                "Branching Type": "Binary (U / V)",
                "Reduction Sizes": "{1, 2}"
            })

    return pd.DataFrame(rows)

# -------------------------------------------------
# Table 2: modeled runtime and memory
# -------------------------------------------------

def estimate_runtime_ms(n: int, encoding_count: int):
    """
    Estimate runtime (ms) using:
    - polynomial cost n^3
    - logarithmic dependence on encoding count
    """
    base_cost = n ** 3
    pruning_factor = log2(max(encoding_count, 2))
    scale = 0.002
    return round(scale * base_cost * pruning_factor, 2)

def estimate_memory_mb(n: int, encoding_count: int):
    """
    Estimate memory usage (MB) assuming:
    - linear dependence on n
    - logarithmic dependence on encoding count
    """
    base_memory = 0.5 * n
    encoding_overhead = log2(max(encoding_count, 2))
    return round(base_memory + encoding_overhead, 2)

def compute_table2_full(n_values=(5, 6, 7, 8, 9, 10, 12)):
    """
    Compute a full Table 2 with:
    - Catalan Count
    - Encoding Count (Lucas-type)
    - Estimated Runtime (ms)
    - Estimated Memory (MB)
    """
    L = lucas_upto(max(n_values) + 5)
    rows = []

    for n in n_values:
        catalan_count = catalan(n - 2)
        encoding_count = L[n - 2]

        runtime_ms = estimate_runtime_ms(n, encoding_count)
        memory_mb = estimate_memory_mb(n, encoding_count)

        rows.append({
            "n": n,
            "Catalan Count": catalan_count,
            "Enc. Count": encoding_count,
            "Runtime (ms)": runtime_ms,
            "Memory (MB)": memory_mb
        })

    return pd.DataFrame(rows)

# -------------------------------------------------
# Main execution
# -------------------------------------------------

if __name__ == "__main__":

    df_table1 = compute_table1(
        m_values=(1, 2, 3),
        n_values=(2, 3, 4)
    )

    df_table2 = compute_table2_full(
        n_values=(5, 6, 7, 8, 9, 10, 12)
    )

    print("\n=== Table 1: Structural and Combinatorial Results ===")
    print(df_table1.to_string(index=False))

    print("\n=== Table 2 ===")
    print(df_table2.to_string(index=False))
