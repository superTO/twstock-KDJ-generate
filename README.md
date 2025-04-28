# twstock-KDJ-generate

[requires]
python_version = "3.9"


## 注意事項
1. 請確保虛擬環境 .venv 是乾淨的, 只有此專案使用, 不要安裝其他 package
2. OS: windows 10, terminal: powershell

## 使用 conda 建立 虛擬環境 流程
1. conda create python=3.9 --prefix .venv
    - 將虛擬環境建立在指定路徑
    - 或是使用 conda create -n kickstarter-PassiveGuidance python=3.9 定義環境名稱
    - 備註: -n 和 --prefix 不可同時使用
2. conda activate .\.venv\
    - windows 環境的關係會有\ , 請盡量用 tab autocomplement
3. pip install -r requirements.txt

## 請注意
- PowerShell exports files in UTF-16 LE by default, which may not display correctly on GitHub; you need to convert them to UTF-8.


## keepalive.yml

原因: Scheduled workflows are disabled automatically after 60 days of repository inactivity.
解決辦法: 固定每個月1號, 在 keepalive 分支建立空的 commit 並 push, 以此來規避60天程式碼沒有更新的問題.
