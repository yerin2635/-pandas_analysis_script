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
all-company-cost-sum                      所有公司成本總和
all-company-service-cost-sum              所有公司服務費用總和
choose-one-billing-account-id             指定一家公司使用的服務流量及cost
choose-one-billing-account-id-use-time    查看一個公司的服務使用時間
copy                                      測試
cost-discount                             列印則扣後的價格
cost-discount-test                        測試合併則扣
cost-sum                                  列印所有金額
filter-test                               filter練習
groupby-time-test                         時間先groupby
location-country-count                    伺服器地點統計
max-cost                                  cost最高的一筆資料
month-statistics                          指定一家公司的當月cost
print-company                             所有公司打95折
print-company-groupby                     所有公司打95折
service-sum                               服務的cost總和
time-test                                 測試時間+cost2
usage-amount-sum                          所有服務的的cost
traffic-discount                          計算所有公司使用的流量及價格
generate-image                            製作圖表
```