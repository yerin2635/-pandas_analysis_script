import pandas as pd

testcsv = pd.read_csv("data/air_quality.csv")

print(testcsv)
testcsv.head(10)
print(testcsv.dtypes)

# 找出最大值並印出那一列
ind = testcsv["AQI"].idxmax()
row = testcsv.iloc[ind, :]
print(row)


# 找出AQI大於50的
above_50 = testcsv[testcsv["AQI"] > 50]
print(above_50.head(30))
