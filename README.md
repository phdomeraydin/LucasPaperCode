# OOP Polygon Dissections via Lucas-Inspired Encoding

This folder contains an object-oriented Python implementation of the reduction-based encoding framework described in the manuscript.

## Contents

- `geometry.py`  
  Basic polygon counting utilities:
  - Catalan numbers for triangulation counts
  - Fibonacci numbers for encoding counts

- `lucas_encoding.py`  
  Core object-oriented implementation:
  - `PolygonReductionEncoder`
  - generation of admissible reduction sequences
  - verification helpers
  - summary tables for small `n`

- `experiments.py`  
  Reproduces the computational experiments:
  - Table of admissible sequences
  - line chart for Catalan vs encoding growth
  - bar chart for geometric vs encoding complexity

- `requirements.txt`  
  Minimal dependencies

## Mathematical model

The implementation follows the restricted reduction framework:

- `U` step reduces the polygon size by 1
- `V` step reduces the polygon size by 2
- admissible sequences reduce `P_n` to the base triangle `P_3`

Thus the encoding count satisfies:

`E_n = E_(n-1) + E_(n-2)`, with `E_3 = 1`, `E_4 = 1`

This produces Fibonacci-type growth.

## How to run

Open a terminal in this folder and run:

```bash
python experiments.py
```

This will:

1. print the admissible sequence table for small `n`
2. save `catalan_vs_encoding.png`
3. save `geometric_vs_encoding_bar.png`

## Notes

This code focuses on admissible reduction sequences and the associated counting model.
It does **not** claim to enumerate all triangulations of a convex polygon.
Instead, it studies the smaller encoding space induced by the restricted `U/V` reduction rules.
