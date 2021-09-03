from find_subscribers import filter_raw_detection
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.DataFrame([1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1], columns=["state"])
    df_old = df.copy()
    df = filter_raw_detection(df)
    df["stats_old"] = df_old["state"]
    df.plot.bar()
    plt.show()
