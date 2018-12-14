import pandas as pd

twitter = pd.read_csv("C:/Users/PhoenixJauregui/Documents/trump/trump/tweets3.csv")

favs = [float(i.replace('K', '')) * 1000 for i in twitter["Comments"]]

print(favs)
