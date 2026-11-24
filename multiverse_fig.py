import itertools
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle


BLUE = "#4472C4"

decisions = {
    "D1 Goal guessers": ["Keep", "Exclude\n(n = 13)"],
    "D2 Stats grade": ["Keep all", "Exclude < 5.5\n(n = 25)", "Exclude < 6.0\n(n = 54)"],
    "D3 Comprehension": ["Keep all", "Exclude ≤ 7\n(n = 4)", "Exclude ≤ 10\n(n = 37)",
                         "Keep all +\ncovariate"],
    "D4 Covariates": ["None", "ReadNews", "ReadNews\n+ Sexe"],
}
short = [["Keep", "Excl."], ["Keep", "<5.5", "<6.0"],
         ["Keep", "≤7", "≤10", "Cov."], ["None", "RN", "RN+S"]]

# the same options as they are coded in the R results
codes = [["Keep", "Exclude"], ["Keep all", "< 5.5", "< 6.0"],
         ["Keep all", "<= 7", "<= 10", "Covariate"],
         ["None", "ReadNews", "ReadNews + Sexe"]]


def node(ax, x, y, text, w=1.5, h=0.75, fs=9):
    ax.add_patch(Ellipse((x, y), w, h, color=BLUE, zorder=2))
    ax.text(x, y, text, ha="center", va="center", color="white",
            fontsize=fs, fontweight="bold", zorder=3)


def raw_data(ax, y, h=0.7):
    ax.add_patch(Rectangle((-0.65, y - h / 2), 1.3, h, color=BLUE, zorder=2))
    ax.text(0, y, "Raw data\nN = 237", ha="center", va="center",
            color="white", fontsize=10, fontweight="bold", zorder=3)


def lattice(path):
    fig, ax = plt.subplots(figsize=(12, 6))
    prev = [(0, 0)]
    n_paths = 1
    for i, (name, options) in enumerate(decisions.items()):
        x = 2.4 * (i + 1)
        ys = [1.1 * (len(options) - 1) / 2 - 1.1 * j for j in range(len(options))]
        for (px, py), y in itertools.product(prev, ys):
            ax.plot([px, x], [py, y], "k-", lw=0.8, zorder=1)
        for y, text in zip(ys, options):
            node(ax, x, y, text)
        n_paths *= len(options)
        ax.text(x, 2.5, name, ha="center", fontsize=11, fontweight="bold")
        ax.text(x, -2.7, f"× {len(options)} → {n_paths} paths", ha="center")
        prev = [(x, y) for y in ys]
    raw_data(ax, 0)
    ax.text(11, 0, f"{n_paths}\npathways", va="center", fontsize=13, fontweight="bold")
    ax.set_xlim(-1, 12)
    ax.set_ylim(-3, 3)
    ax.axis("off")
    fig.savefig(path, dpi=300, bbox_inches="tight")


def full_tree(path, results_file):
    results = pd.read_csv(results_file, keep_default_na=False)
    results = results.set_index(["goal", "grade", "comp", "covs"])
    leaves = list(itertools.product(*[range(len(o)) for o in decisions.values()]))
    fig, ax = plt.subplots(figsize=(13, 17))

    def y_of(prefix):
        ys = [-i for i, p in enumerate(leaves) if p[:len(prefix)] == prefix]
        return sum(ys) / len(ys)

    xs = [0, 2.2, 4.4, 6.9, 9.4]
    for depth, options in enumerate(decisions.values(), start=1):
        for prefix in sorted({p[:depth] for p in leaves}):
            y, py = y_of(prefix), y_of(prefix[:-1])
            ax.plot([xs[depth - 1], xs[depth]], [py, y], "k-", lw=0.5, zorder=1)
            if depth == 4:
                node(ax, xs[depth], y, short[3][prefix[-1]], w=1.0, h=0.8, fs=6.5)
            else:
                node(ax, xs[depth], y, options[prefix[-1]], w=1.35, h=1.4, fs=7)
    raw_data(ax, y_of(()), h=1.6)

    # right column: sample size and p-value of each pathway (blue if p < .05)
    ax.text(10.05, 0.9, "      N      p", fontsize=7, family="monospace",
            fontweight="bold")
    for i, p in enumerate(leaves):
        row = results.loc[tuple(codes[d][p[d]] for d in range(4))]
        colour = BLUE if row["p"] < .05 else "grey"
        ax.text(10.05, -i, f"{i + 1:>2}.  {int(row['n']):>3}  {row['p']:.3f}",
                va="center", fontsize=7, family="monospace", color=colour)
    for x, name in zip(xs[1:], decisions):
        ax.text(x, 1.5, name, ha="center", fontsize=10, fontweight="bold")
    ax.set_xlim(-1, 12.6)
    ax.set_ylim(-len(leaves), 2.5)
    ax.axis("off")
    fig.savefig(path, dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    lattice("multiverse_lattice.png")
    full_tree("multiverse_full_tree.png", "multiverse_results.csv")
