import pandas as pd

#  使用陣列建立DataFrame
# grades = [
#     ["Mike", 80, 63],
#     ["Sherry", 75, 90],
#     ["Cindy", 93, 85],
#     ["John", 86, 70]
# ]

# new_df = pd.DataFrame(grades)

# print("使用陣列來建立df：")
# print(new_df)
# print("=====================")


grads = {
    "name": ["Mike", "Sherry", "Cindy", "John"],
    "math": [80, 75, 93, 86],
    "chinese": [63, 90, 85, 70],
}

df = pd.DataFrame(grads)
# df.index = ["s1", "s2", "s3", "s4"]
# df.columns = ["student_name", "math_score", "chinese_sccore"]
# print(df)

print("=============")
# 取得最前兩筆資料
new_pf = df.head(2)
print(new_pf)
print("=============")
# 取得最後三筆資料
new_pf1 = df.tail(3)
print(new_pf1)

print("=============1")
#  取得單一欄位資料(型別為Series)
print(df["name"])
print("=============")
# 取得單一欄位資料(型別為DataFrame)
print(df[["name"]])
print("=============")


df.sort_values
