"""
experiments.py
Run computational experiments for Lucas-inspired reduction encoding.
"""

from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np

from geometry import CountingUtils
from lucas_encoding import PolygonReductionEncoder


class ExperimentRunner:
    def __init__(self, n_min: int = 3, n_max: int = 12) -> None:
        self.n_min = n_min
        self.n_max = n_max
        self.encoder = PolygonReductionEncoder()

    def print_sequence_table(self, n_min: int = 3, n_max: int = 8) -> None:
        rows = self.encoder.summary_table(n_min, n_max)
        print(f"{'n':<5}{'E_n':<8}Sequences")
        print("-" * 50)
        for row in rows:
            print(f"{row['n']:<5}{row['E_n']:<8}{row['Sequences']}")

    def line_plot(self) -> None:
        n_values = list(range(max(5, self.n_min), self.n_max + 1))
        catalan_counts = [CountingUtils.triangulation_count(n) for n in n_values]
        encoding_counts = [self.encoder.count_encodings(n) for n in n_values]

        plt.figure(figsize=(8, 5))
        plt.plot(n_values, catalan_counts, marker="o", linestyle="-", label="Catalan count")
        plt.plot(n_values, encoding_counts, marker="s", linestyle="--", label="Encoding count")
        plt.yscale("log")
        plt.xlabel("n (number of vertices)")
        plt.ylabel("Count (log scale)")
        plt.title("Catalan vs Fibonacci-Type Encoding Growth")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig("catalan_vs_encoding.png", dpi=300, bbox_inches="tight")
        plt.close()

    def bar_plot(self) -> None:
        n_values = list(range(max(5, self.n_min), self.n_max + 1))
        catalan_counts = [CountingUtils.triangulation_count(n) for n in n_values]
        encoding_counts = [self.encoder.count_encodings(n) for n in n_values]

        x = np.arange(len(n_values))
        width = 0.38

        plt.figure(figsize=(9, 5))
        plt.bar(x - width / 2, catalan_counts, width, label="Catalan count")
        plt.bar(x + width / 2, encoding_counts, width, label="Encoding count")
        plt.yscale("log")
        plt.xticks(x, n_values)
        plt.xlabel("n (number of vertices)")
        plt.ylabel("Count (log scale)")
        plt.title("Geometric vs Encoding Complexity")
        plt.legend()
        plt.grid(True, axis="y", which="both", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig("geometric_vs_encoding_bar.png", dpi=300, bbox_inches="tight")
        plt.close()

    def verify_model(self) -> None:
        for n in range(max(5, self.n_min), self.n_max + 1):
            ok = self.encoder.verify_recurrence(n)
            print(f"n={n}: recurrence check = {ok}")

    def run_all(self) -> None:
        self.print_sequence_table()
        self.verify_model()
        self.line_plot()
        self.bar_plot()
        print("\nSaved:")
        print("- catalan_vs_encoding.png")
        print("- geometric_vs_encoding_bar.png")


if __name__ == "__main__":
    runner = ExperimentRunner()
    runner.run_all()
