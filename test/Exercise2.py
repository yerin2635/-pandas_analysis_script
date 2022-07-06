import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

df = pd.read_csv("data/歷年國內主要觀光遊憩據點遊客人數月別統計.csv", encoding="utf-8")

# 尋找2019年的台北市123月遊客人數
rows = (df["年別"] == 2019) & (df["縣市別"] == "臺北市")
columns = ["細分", "1月", "2月", "3月"]
result = df.loc[rows, columns].head(10)
result.set_index("細分", inplace=True)

# chart = result.plot(
#     kind='bar',  # 圖表類型
#     title='2019台北市各景點旅客人數',  # 圖表標題
#     xlabel='細分',  # x軸說明文字
#     ylabel='人數',  # y軸說明文字
#     legend=True,  # 是否顯示圖例
#     figsize=(10, 5),  # 圖表大小
# )

chart = result.plot(figsize=(10, 5))  # 圖表大小
font = FontProperties(fname=r"font/NotoSansTC-Black.otf")

for label in chart.get_xticklabels():
    label.set_fontproperties(font)  # 設定x軸每一個細分

plt.title("2019年臺北市各景點旅客人數", fontproperties=font)  # 圖表標題
plt.xlabel("景點名稱", fontproperties=font)  # x軸說明文字
plt.ylabel("人數", fontproperties=font)  # y軸說明文字
plt.legend(prop=font)  # 圖例


plt.show()
