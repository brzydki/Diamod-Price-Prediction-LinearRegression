import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
def plot_1():
    with open('X_data.pkl', 'rb') as f:
        list1 = pickle.load(f)

    # Загрузка result.x
    with open('result_x.pkl', 'rb') as f:
        list2 = pickle.load(f)
    data_before = {
        "Карат": list1[0],
        "Глубина": list1[1],
        "Ширина верхней части": list1[2],
        "Длина в мм": list1[3],
        "Ширина в мм": list1[4],
        "Высота в мм": list1[5],
    }
    data_after = {
        "Карат": list2[0],
        "Глубина": list2[1],
        "Ширина верхней части": list2[2],
        "Длина в мм": list2[3],
        "Ширина в мм": list2[4],
        "Высота в мм": list2[5],
    }


    df = pd.DataFrame({
        "Параметр": ["Карат", "Глубина", "Ширина верхней части", "Длина в мм", "Ширина в мм", "Высота в мм"],
        "До оптимизации": list1,
        "После оптимизации": list2
    })


    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Анализ параметров алмаза", fontsize=16)


    df.set_index("Параметр")[["До оптимизации", "После оптимизации"]].plot(
        kind="bar", ax=axs[0], color=["blue", "green"], edgecolor="black")
    axs[0].set_title("Сравнение параметров до и после оптимизации")
    axs[0].set_ylabel("Значение")
    axs[0].grid(axis="y")


    axs[1].scatter(list1, list2, color="purple", edgecolor="black", s=100)
    for i, param in enumerate(df["Параметр"]):
        axs[1].annotate(param, (list1[i], list2[i]), textcoords="offset points", xytext=(5, -10), ha="center")
    axs[1].plot([min(list1), max(list1)], [min(list1), max(list1)], color="red", linestyle="--", label="Линия равенства")
    axs[1].set_title("Диаграмма рассеяния: До против После")
    axs[1].set_xlabel("До оптимизации")
    axs[1].set_ylabel("После оптимизации")
    axs[1].legend()
    axs[1].grid()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
