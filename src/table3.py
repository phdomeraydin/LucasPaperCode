# pip install pandas numpy
import pandas as pd
import numpy as np
from math import comb

# -----------------------------
# Combinatorial functions
# -----------------------------

def fuss_catalan(m: int, n: int) -> int:
    """
    Compute Fuss–Catalan number:
      FC(m, n) = 1/(m*n + 1) * binom((m+1)*n, n)

    This matches the standard count for (m+2)-angulations
    of a polygon with N = m*n + 2 vertices.
    """
    return comb((m + 1) * n, n) // (m * n + 1)

def lucas_upto(N: int):
    """Generate Lucas numbers up to index N (L0=2, L1=1, Ln=Ln-1+Ln-2)."""
    L = [0] * (N + 1)
    if N >= 0:
        L[0] = 2
    if N >= 1:
        L[1] = 1
    for i in range(2, N + 1):
        L[i] = L[i - 1] + L[i - 2]
    return L

# -----------------------------
# m-parameter runtime/memory model (modeled, not measured)
# -----------------------------

def runtime_model_ms(m: int, N: int, enc_count: int, params=None) -> float:
    """
    Modeled runtime (ms) for (m+2)-angulations.

    Default model:
      Runtime ≈ a*(N^3 * log2(enc)) + b*(m * N^2) + c
    """
    log_enc = np.log2(max(enc_count, 2))
    if params is None:
        a, b, c = 2.0e-6, 3.0e-4, 0.0
    else:
        a, b, c = params
    return float(a * (N**3) * log_enc + b * (m * (N**2)) + c)

def memory_model_mb(m: int, N: int, enc_count: int, params=None) -> float:
    """
    Modeled memory (MB) for (m+2)-angulations.

    Default model:
      Memory ≈ d*N + e*log2(enc) + f*m + g
    """
    log_enc = np.log2(max(enc_count, 2))
    if params is None:
        d, e, f, g = 0.06, 0.9, 0.25, 0.0
    else:
        d, e, f, g = params
    return float(d * N + e * log_enc + f * m + g)

# -----------------------------
# Build Table 3 as a DataFrame (no DOCX reading)
# -----------------------------

def build_table3_df(pairs=None, m_values=(2, 3, 4), n_values=(2, 3, 4, 5)):
    """
    Create a Table 3-like DataFrame purely from formulas.

    You can provide either:
      - pairs=[(m,n), (m,n), ...]
    or
      - m_values and n_values (Cartesian product).

    Output columns:
      m, n, Vertices (N), Geometric Count, Enc. Count, Runtime (ms), Memory (MB)
    """
    if pairs is None:
        pairs = [(m, n) for m in m_values for n in n_values]

    # Determine the maximum Lucas index needed: (N - 2)
    max_N = max(m * n + 2 for (m, n) in pairs)
    L = lucas_upto(max_N)

    rows = []
    for m, n in pairs:
        N = m * n + 2
        geo = fuss_catalan(m, n)
        enc = L[N - 2]

        rt = runtime_model_ms(m, N, enc)
        mem = memory_model_mb(m, N, enc)

        rows.append({
            "m": m,
            "n": n,
            "Vertices (N)": N,
            "Geometric Count": geo,
            "Enc. Count": enc,
            "Runtime (ms)": round(rt, 2),
            "Memory (MB)": round(mem, 2),
        })

    df3 = pd.DataFrame(rows).sort_values(["m", "n"]).reset_index(drop=True)
    return df3

if __name__ == "__main__":
    # Option A: specify explicit (m, n) pairs
    # df3 = build_table3_df(pairs=[(2,2), (2,3), (3,2), (3,3)])

    # Option B: generate via ranges (default)
    df3 = build_table3_df(m_values=(2, 3, 4), n_values=(2, 3, 4, 5))

    print("\n=== Table 3  ===")
    print(df3.to_string(index=False))
