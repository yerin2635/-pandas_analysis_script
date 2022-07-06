# Pandas Analysis Script
使用Pandas作數據分析


## Environment

```
Python 3.9.12
```

## Local development

1. 建立Python虛擬環境

```shell
$ pip install virtualenv 
$ virtualenv venv     
```

2. 啟動虛擬環境
  
```shell
$ venv\Scripts\activate
```

3. 安裝套件

```shell
$ pip install -r requirements.txt
```

4.  終端機提供的服務

```shell
$ python app <option>
copy                                      測試讀寫檔案是否存在
cost-sum                                  列印所有金額加總
service-sum                               所有服務的cost總和
max-cost                                  所有資料裡cost最高的一筆資料
all-company-cost-sum                      所有公司成本總和
all-company-service-cost-sum              所有billing-account-id的cost總和
filter-test                               filter練習
location-country-count                    伺服器地點統計
usage-amount-sum                          所有使用服務的cost
choose-one-billing-account-id             指定一家公司使用的服務流量及cost
month-statistics                          指定一家公司的當月cost
print-company                             所有公司打95折後的金額
print-company-groupby                     使用groups.keys後取得的所有公司打95折
cost-discount                             列印則扣後的價格
cost-discount-test                        測試合併則扣
time-test                                 測試時間+cost2
groupby-time-test                         時間先groupby
traffic-discount                          計算所有公司使用的流量及價格
generate-image                            選擇要查看的服務並製作成圖表
```