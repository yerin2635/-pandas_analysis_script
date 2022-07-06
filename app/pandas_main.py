from datetime import date
import time
import click
import pandas as pd
from pandas_read import read_intern_billing
from pandas_write import write_file
from pandas_traffic_discount import calculate_cost
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

pd.options.mode.chained_assignment = None


@click.command(help="測試讀寫檔案是否存在")
@click.argument("data_name1", nargs=1)
@click.argument("data_name2", nargs=1)
def copy(data_name1, data_name2):
    # date_set = date_set.date()
    click.echo(f"{data_name1} \t {data_name2} \t ")


@click.command(help="列印所有金額加總")
@click.argument("data_name1", nargs=1)
@click.argument("data_name2", nargs=1)
def cost_sum(data_name1, data_name2):
    df = read_intern_billing(data_name1)
    df2 = read_intern_billing(data_name2)
    cost_totle = df["cost"].sum()
    cost_totle2 = df2["List price ($)"].sum()
    print("檔案一cost加總為:" + str(cost_totle))
    print("檔案二cost加總為:" + str(cost_totle2))
    return print("成功")


@click.command(help="所有服務的cost總和")
@click.argument("data_name")
def service_sum(data_name):
    df = read_intern_billing(data_name)
    service_description_cost = df.groupby(["service.description"])
    print(service_description_cost["cost"].sum())


@click.command(help="所有資料裡cost最高的一筆資料")
@click.argument("data_name")
def max_cost(data_name):
    df = read_intern_billing(data_name)
    ind = df["cost"].idxmax()
    row = df.iloc[ind, :]
    print(row)


@click.command(help="所有公司成本總和")
@click.argument("data_name")
def all_company_cost_sum(data_name):
    df = read_intern_billing(data_name)
    billing_account_id_cost = df.groupby(["billing_account_id"])
    print(billing_account_id_cost["cost"].sum())


@click.command(help="所有billing-account-id的cost總和")
@click.argument("data_name")
def all_company_service_cost_sum(data_name):
    df = read_intern_billing(data_name)
    billing_account_id_services_used_total = df.groupby(
        ["billing_account_id", "service.description"]
    )
    print(billing_account_id_services_used_total["cost"].sum())


@click.command(help="filter練習")
@click.argument("data_name")
def filter_test(data_name):
    df = read_intern_billing(data_name)
    billing_account_id_services_used = df.filter(
        ["billing_account_id", "service.description", "cost"]
    )
    print("印出帳號使用的服務及價格欄位:\n", billing_account_id_services_used)

    fine_word_field = df.filter(regex="[aA]")
    print("找到列裡有A的欄位:", fine_word_field)


@click.command(help="伺服器地點統計")
@click.argument("data_name")
def location_country_count(data_name):
    df = read_intern_billing(data_name)
    location_count = df["location.country"].value_counts()
    print(location_count)


@click.command(help="所有使用服務的cost")
@click.argument("data_name")
def usage_amount_sum(data_name):
    df = read_intern_billing(data_name)
    services_use_data = df.groupby("service.description")
    print(services_use_data["usage.amount"].sum())


@click.command(help="指定一家公司使用的服務流量及cost")
@click.argument("data_name")
@click.argument("company_name")
def choose_one_billing_account_id(data_name, company_name):
    df = read_intern_billing(data_name)
    rows = df.loc[df["billing_account_id"] == company_name].groupby(
        ["service.description", "sku.description", "usage.pricing_unit"]
    )
    rows_df = pd.DataFrame(rows["usage.amount_in_pricing_units", "cost"].sum())
    write_file(rows_df, str(company_name) + "指定公司所有服務的cost加總")


@click.command(help="指定一家公司的當月cost加總")
@click.argument("using_df", nargs=1)
@click.argument("company_name")
def month_statistics(using_df, company_name):
    df = read_intern_billing(using_df)
    df["usage_start_time"] = pd.to_datetime(df["usage_start_time"]).apply(
        lambda x: x.date()
    )
    result = df.loc[df["billing_account_id"] == company_name].groupby(
        [
            "usage_start_time",
            "service.description",
            "sku.id",
            "sku.description",
            "usage.pricing_unit",
        ]
    )
    result_df = pd.DataFrame(result.sum())
    result_df.reset_index(inplace=True)
    write_file(result_df, str(company_name) + "的當月cost加總")


@click.command(help="所有公司打95折後的金額")
@click.argument("data_name")
def print_company(data_name):
    df = read_intern_billing(data_name)
    df["usage_start_time"] = pd.to_datetime(df["usage_start_time"]).apply(
        lambda x: x.date()
    )
    for i in df["billing_account_id"].unique():
        result = df.loc[df["billing_account_id"] == i].groupby(
            [
                "usage_start_time",
                "service.description",
                "sku.description",
                "usage.pricing_unit",
            ]
        )
        result_df = pd.DataFrame(result.sum())
        result_df["cost2"] = result_df["cost"].map(lambda x: x * 0.95)
        write_file(result_df, str(i) + "95折後的cost總和")


@click.command(help="使用groups.keys後取得的所有公司打95折")
@click.argument("data_name")
def print_company_groupby(data_name):
    df = read_intern_billing(data_name)
    df["usage_start_time"] = pd.to_datetime(df["usage_start_time"]).apply(
        lambda x: x.date()
    )
    for i in df.groupby(["billing_account_id"]).groups.keys():
        result = df.groupby(
            [
                "usage_start_time",
                "service.description",
                "sku.description",
                "usage.pricing_unit",
            ]
        )
        result_df = pd.DataFrame(result.sum())
        result_df["cost2"] = result_df["cost"].map(lambda x: x * 0.95)
        write_file(result_df, str(i) + "95折後的cost總和(groups.keys)")


@click.command(help="列印則扣後的價格")
@click.argument("using_df", nargs=1)
@click.argument("pricing_df", nargs=1)
@click.option(
    "--date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="填入日期 xxxx-xx-xx",
)
def cost_discount(using_df, pricing_df, date):
    using_df = read_intern_billing(using_df)
    pricing_df = read_intern_billing(pricing_df)
    pricing_df = pricing_df.dropna(
        axis="index", how="any", subset=["Contract price ($)", "Effective discount"]
    )

    pricing_df["Effective discount"] = (
        1
        - pricing_df["Effective discount"]
        .str.rstrip("%")
        .replace(",", "", regex=True)
        .astype("float")
        / 100.0
    )

    pricing_df["price after discount"] = pricing_df[
        ["Contract price ($)", "Effective discount"]
    ].apply(lambda x: x["Contract price ($)"] * x["Effective discount"], axis=1)

    write_file(pricing_df, "刪除金額及折扣空值")


@click.command(help="測試合併則扣")
@click.argument("using_df", nargs=1)
@click.argument("pricing_df", nargs=1)
@click.option(
    "--date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="填入日期 xxxx-xx-xx",
)
def cost_discount_test(using_df, pricing_df, date):
    using_df = read_intern_billing(using_df)
    pricing_df = read_intern_billing(pricing_df)
    pricing_df.dropna(
        axis="index", how="any", subset=["Contract price ($)", "Effective discount"]
    )

    pricing_df["Effective discount"] = (
        1
        - pricing_df["Effective discount"]
        .str.rstrip("%")
        .replace(",", "", regex=True)
        .astype("float")
        / 100.0
    )

    new_pricing_df = pricing_df[
        ["SKU ID", "Discount", "Contract price ($)", "Effective discount"]
    ]

    result = using_df.join(new_pricing_df.set_index("SKU ID"), on="sku.id")
    result["cost2"] = result["cost"] * result["Effective discount"]

    for billing_account_id in using_df.groupby(["billing_account_id"]).groups.keys():
        result_df = result.loc[result["billing_account_id"] == billing_account_id]

        write_file(result_df, str(billing_account_id))


@click.command(help="測試時間+cost2")
@click.argument("using_df", nargs=1)
@click.argument("pricing_df", nargs=1)
@click.option(
    "--date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="填入日期 xxxx-xx-xx",
)
def time_test(using_df, pricing_df, date):
    start = time.time()
    using_df = read_intern_billing(using_df)
    pricing_df = read_intern_billing(pricing_df)
    using_df["usage_start_time"] = pd.to_datetime(using_df["usage_start_time"]).apply(
        lambda x: x.date()
    )

    pricing_df.dropna(
        axis="index", how="any", subset=["Contract price ($)", "Effective discount"]
    )

    pricing_df["Effective discount"] = (
        1
        - pricing_df["Effective discount"]
        .str.rstrip("%")
        .replace(",", "", regex=True)
        .astype("float")
        / 100.0
    )

    new_pricing_df = pricing_df[
        [
            "SKU ID",
            "Discount",
            "Tiered usage start",
            "List price ($)",
            "Contract price ($)",
            "Effective discount",
        ]
    ]

    for billing_account_id in using_df.groupby(["billing_account_id"]).groups.keys():
        result_df = using_df.loc[
            using_df["billing_account_id"] == billing_account_id
        ].groupby(
            [
                "usage_start_time",
                "service.description",
                "sku.id",
                "sku.description",
                "usage.pricing_unit",
            ]
        )

        result_df = pd.DataFrame(result_df.sum())

        new_usging = result_df.join(new_pricing_df.set_index("SKU ID"), on="sku.id")
        new_usging["cost2"] = new_usging["cost"] * new_usging["Effective discount"]
        new_usging = pd.DataFrame(new_usging)
        new_usging.reset_index(inplace=True)
        write_file(new_usging, str(billing_account_id))
    end = time.time()
    print("用時" + str(end - start) + "秒")


@click.command(help="時間先groupby")
@click.argument("using_df", nargs=1)
@click.argument("pricing_df", nargs=1)
@click.option(
    "--date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="填入日期 xxxx-xx-xx",
)
def groupby_time_test(using_df, pricing_df, date):
    using_df = read_intern_billing(using_df)
    pricing_df = read_intern_billing(pricing_df)

    using_df["usage_start_time"] = pd.to_datetime(using_df["usage_start_time"]).apply(
        lambda x: x.date()
    )

    pricing_df.dropna(
        axis="index", how="any", subset=["Contract price ($)", "Effective discount"]
    )

    pricing_df["Effective discount"] = (
        1
        - pricing_df["Effective discount"]
        .str.rstrip("%")
        .replace(",", "", regex=True)
        .astype("float")
        / 100.0
    )

    new_pricing_df = pricing_df[
        [
            "SKU ID",
            "Discount",
            "Tiered usage start",
            "List price ($)",
            "Contract price ($)",
            "Effective discount",
        ]
    ]

    using_df = using_df.groupby(
        [
            "billing_account_id",
            "usage_start_time",
            "service.description",
            "sku.id",
            "sku.description",
            "usage.pricing_unit",
        ]
    )
    using_df = pd.DataFrame(using_df.sum())
    using_df.reset_index(inplace=True)

    new_usging = using_df.join(new_pricing_df.set_index("SKU ID"), on="sku.id")
    new_usging["cost2"] = new_usging["cost"] * new_usging["Effective discount"]
    new_usging = pd.DataFrame(new_usging)
    new_usging.reset_index(inplace=True)

    for billing_account in using_df.groupby(["billing_account_id"]).groups.keys():
        result_df = new_usging.loc[new_usging["billing_account_id"] == billing_account]
        write_file(result_df, str(billing_account))


@click.command(help="計算所有公司使用的流量及價格")
@click.argument("using_df", nargs=1)
@click.argument("pricing_df", nargs=1)
@click.option(
    "--date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="填入日期 xxxx-xx-xx",
)
def traffic_discount(using_df, pricing_df, date):
    start = time.time()
    using_df = read_intern_billing(using_df)
    pricing_df = read_intern_billing(pricing_df)
    using_df["usage_start_time"] = pd.to_datetime(using_df["usage_start_time"]).apply(
        lambda x: x.date()
    )

    pricing_df.dropna(
        axis="index", how="any", subset=["Contract price ($)", "Effective discount"]
    )

    pricing_df["Effective discount"] = (
        1
        - pricing_df["Effective discount"]
        .str.rstrip("%")
        .replace(",", "", regex=True)
        .astype("float")
        / 100.0
    )

    new_pricing_df = pricing_df[
        [
            "SKU ID",
            "Discount",
            "Tiered usage start",
            "List price ($)",
            "Contract price ($)",
            "Effective discount",
        ]
    ]

    count_skuid = new_pricing_df["SKU ID"].value_counts().to_dict()
    count_two_skuid = {key: values for key, values in count_skuid.items() if values > 1}
    using_df = using_df.groupby(
        [
            "billing_account_id",
            "usage_start_time",
            "service.description",
            "sku.id",
            "sku.description",
            "usage.pricing_unit",
        ]
    )
    using_df = pd.DataFrame(using_df.sum())
    using_df.reset_index(inplace=True)

    # 需要額外計算的
    usage_df = using_df.loc[using_df["sku.id"].isin(count_two_skuid.keys())]

    usage_two_df = []
    for skuid in usage_df.groupby(["sku.id"]).groups.keys():
        result = new_pricing_df.loc[new_pricing_df["SKU ID"] == skuid]
        Tiered_usage = result["Tiered usage start"].to_list()
        Contract_price = result["Contract price ($)"].to_list()

        new_usage = usage_df.loc[usage_df["sku.id"] == skuid]
        new_usage["cost2"] = new_usage["usage.amount_in_pricing_units"].apply(
            calculate_cost, metrics=Tiered_usage, pricings=Contract_price
        )
        usage_two_df.append(new_usage)
    usage_two_df = pd.concat(usage_two_df)

    usage_two_df = usage_two_df.groupby(
        [
            "billing_account_id",
            "usage_start_time",
            "service.description",
            "sku.id",
            "sku.description",
            "usage.pricing_unit",
        ]
    )
    usage_two_df = pd.DataFrame(usage_two_df.sum())
    usage_two_df.reset_index(inplace=True)

    # 只需要相乘的
    one_using_df = using_df.loc[~using_df["sku.id"].isin(count_two_skuid.keys())]

    new_usging = one_using_df.join(new_pricing_df.set_index("SKU ID"), on="sku.id")
    new_usging["cost2"] = new_usging["cost"] * new_usging["Effective discount"]
    new_usging = pd.DataFrame(new_usging.sum())
    new_usging.reset_index(inplace=True)

    # 將兩張表合併
    total = pd.concat([usage_two_df, new_usging], axis=0)
    for billing_account in using_df.groupby(["billing_account_id"]).groups.keys():
        result_df = total.loc[total["billing_account_id"] == billing_account]
        write_file(result_df, str(billing_account))


@click.command(help="選擇要查看的服務並製作成圖表")
@click.argument("csv_path", nargs=1)
@click.option("--service", type=str, help="請填入要查詢的服務")
@click.option("--show", type=bool, is_flag=True, help="查看圖表")
def generate_image(csv_path, service, show):
    using_df = read_intern_billing(csv_path)

    if using_df is None:
        exit()

    font = FontProperties(fname=r"font/NotoSansTC-Black.otf")
    if service == None:
        title = using_df.iat[0, 1] + "所有服務費用加總"
    else:
        using_df = using_df.loc[using_df["service.description"] == service]
        title = using_df.iat[0, 1] + "的" + service + "費用"
        if using_df.empty == True:
            print("服務輸入錯誤")
            exit()

    using_df = using_df.groupby(["usage_start_time"])
    using_df = pd.DataFrame(using_df.sum())
    using_df.reset_index(inplace=True)

    using_df[
        [
            "usage_start_time",
            "cost",
        ]
    ].plot(x="usage_start_time", y="cost", kind="bar")

    plt.title(title, fontproperties=font)
    plt.xlabel("時間", fontproperties=font)
    plt.ylabel("價格", fontproperties=font)
    plt.savefig("output/" + title + ".jpg", dpi=200)
    print(title + ".jpg" + "儲存成功")

    if show == True:
        plt.show()
