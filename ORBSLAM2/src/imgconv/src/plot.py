import pandas as pd
import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt

# Read the data from the CSV file.
df = pd.read_csv("deep_04.csv")
print(df.head())
plt.plot(df["x_x"], df["y_y"])
plt.show()

