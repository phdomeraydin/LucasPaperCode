"""
geometry.py
Basic counting utilities for polygon triangulations and admissible encodings.
"""

from __future__ import annotations
import math


class CountingUtils:
    """Utility class for Catalan and Fibonacci-type counts."""

    @staticmethod
    def catalan(k: int) -> int:
        if k < 0:
            raise ValueError("Catalan index must be non-negative.")
        return math.comb(2 * k, k) // (k + 1)

    @staticmethod
    def triangulation_count(n_vertices: int) -> int:
        if n_vertices < 3:
            raise ValueError("A polygon must have at least 3 vertices.")
        return CountingUtils.catalan(n_vertices - 2)

    @staticmethod
    def fibonacci(k: int) -> int:
        if k <= 0:
            return 0
        if k in (1, 2):
            return 1
        a, b = 1, 1
        for _ in range(3, k + 1):
            a, b = b, a + b
        return b

    @staticmethod
    def encoding_count(n_vertices: int) -> int:
        if n_vertices < 3:
            raise ValueError("A polygon must have at least 3 vertices.")
        if n_vertices == 3:
            return 1
        return CountingUtils.fibonacci(n_vertices - 2)
