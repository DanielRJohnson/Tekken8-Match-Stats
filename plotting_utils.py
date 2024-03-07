import os
import matplotlib.pyplot as plt
import seaborn as sns


def plot_categorical_histogram(df, x: str, xlabels: list[str], colors: list[str], title: str, annot_format=".1f", **kwargs):
    hist = sns.countplot(df, x=x, hue=x, palette=colors, stat="percent", **kwargs)
    for i, p in enumerate(sorted([p for p in hist.patches if p.get_height() > 0], key=lambda p: p.get_height())):
        if "order" in kwargs:
            p.set_color(colors[i])
        hist.annotate(f"{p.get_height():{annot_format}}%\n", 
                      (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="center")

    plt.xticks(ticks=range(len(xlabels)), labels=xlabels, rotation=90)
    plt.xlabel("")
    plt.gca().set_yticks([])
    plt.ylabel("")

    plt.title(title, weight="bold")
    plt.tight_layout()
    dirname = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(dirname, exist_ok=True)
    plt.savefig(os.path.join(dirname, f"{title}.png"))
    plt.show()


def plot_bar(df, x: str, y: str, xlabels: list[str], colors: list[str], title: str, ylim=None, annot=True, annot_format=".2f", **kwargs):
    bar = sns.barplot(df, x=x, y=y, hue=x, palette=colors, legend=False, edgecolor="black", **kwargs)
    for i, p in enumerate(sorted([p for p in bar.patches if p.get_height() > 0], key=lambda p: p.get_height())):
        if "order" in kwargs:
            p.set_color(colors[i])
        if annot:
            bar.annotate(f"{p.get_height():{annot_format}}%\n", (p.get_x() + p.get_width() / 2, p.get_height()), ha="center", va="center")

    plt.xticks(ticks=range(len(xlabels)), labels=xlabels, rotation=90)
    plt.xlabel("")
    plt.ylabel("")
    plt.ylim(ylim)

    plt.title(title, weight="bold")
    plt.tight_layout()
    dirname = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(dirname, exist_ok=True)
    plt.savefig(os.path.join(dirname, f"{title}.png"))
    plt.show()


def plot_heatmap(df, xlabel: str, ylabel: str, xticklabels: list[str], yticklabels: list[str], title: str, **kwargs):
    sns.heatmap(df, xticklabels=xticklabels, yticklabels=yticklabels, cmap="magma", annot=True, cbar=False, **kwargs)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title, weight="bold")
    plt.tight_layout()
    dirname = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(dirname, exist_ok=True)
    plt.savefig(os.path.join(dirname, f"{title}.png"))
    plt.show()