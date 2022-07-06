import pandas as pd


def write_file(result_df, file_name):
    datatoexce2 = pd.ExcelWriter(
        "output/" + file_name + ".xlsx", datetime_format="YYYY-MM-DD"
    )
    result_df.to_excel(datatoexce2)
    datatoexce2.save()
    print("完成!")


# result.sum()
