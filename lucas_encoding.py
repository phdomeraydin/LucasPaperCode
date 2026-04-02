"""
lucas_encoding.py
Object-oriented implementation of Lucas-inspired reduction encoding.
"""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Dict


@dataclass(frozen=True)
class ReductionSequence:
    word: str

    @property
    def reduction_amount(self) -> int:
        return self.word.count("U") + 2 * self.word.count("V")

    def is_admissible_for(self, n_vertices: int) -> bool:
        return self.reduction_amount == n_vertices - 3


class PolygonReductionEncoder:
    """
    Generate admissible reduction sequences under the restricted U/V framework.
    """

    def __init__(self) -> None:
        pass

    @lru_cache(maxsize=None)
    def generate_encodings(self, n_vertices: int) -> tuple[str, ...]:
        if n_vertices < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        if n_vertices == 3:
            return ("ε",)

        if n_vertices == 4:
            return ("U",)

        u_branch = tuple(
            "U" + word if word != "ε" else "U"
            for word in self.generate_encodings(n_vertices - 1)
        )
        v_branch = tuple(
            "V" + word if word != "ε" else "V"
            for word in self.generate_encodings(n_vertices - 2)
        )
        return u_branch + v_branch

    def count_encodings(self, n_vertices: int) -> int:
        return len(self.generate_encodings(n_vertices))

    def verify_recurrence(self, n_vertices: int) -> bool:
        if n_vertices < 5:
            return True
        return self.count_encodings(n_vertices) == (
            self.count_encodings(n_vertices - 1) +
            self.count_encodings(n_vertices - 2)
        )

    def summary_row(self, n_vertices: int) -> Dict[str, str]:
        words = list(self.generate_encodings(n_vertices))
        joined = ", ".join(words[:10])
        if len(words) > 10:
            joined += ", ..."
        return {
            "n": str(n_vertices),
            "E_n": str(len(words)),
            "Sequences": joined,
        }

    def summary_table(self, n_min: int = 3, n_max: int = 8) -> List[Dict[str, str]]:
        if n_min > n_max:
            raise ValueError("n_min must be <= n_max.")
        return [self.summary_row(n) for n in range(n_min, n_max + 1)]
