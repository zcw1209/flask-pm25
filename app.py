from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
from pm25 import (
    get_pm25_data_from_mysql,
    update_db,
    get_pm25_data_by_site,
    get_all_counties,
    get_site_by_county,
)
import json

app = Flask(__name__)


@app.route("/pm25-county-site")
def pm25_county_site():
    county = request.args.get("county")
    sites = get_site_by_county(county)
    result = json.dumps(sites, ensure_ascii=False)

    return result


@app.route("/pm25-site")
def pm25_site():
    counties = get_all_counties()
    return render_template("pm25-site.html", counties=counties)


@app.route("/pm25-data-site")
def pm25_data_by_site():
    county = request.args.get("county")
    site = request.args.get("site")

    if not county or not site:
        result = json.dumps({"error": "縣市跟站點名稱不能為空!"}, ensure_ascii=False)
    else:
        columns, datas = get_pm25_data_by_site(county, site)
        df = pd.DataFrame(datas, columns=columns)
        data = df["datacreationdate"].apply(lambda x: x.strftime("%Y-%m-%d %H"))

        data = {
            "county": county,
            "site": site,
            "x_data": data.tolist(),
            "y_data": df["pm25"].tolist(),
        }

        result = json.dumps(data, ensure_ascii=False)

    return result


# 更新資料庫
@app.route("/update-db")
def update_pm25_db():
    count, message = update_db()
    nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = json.dumps(
        {"時間": nowtime, "更新比數": count, "結果": message}, ensure_ascii=False
    )
    return result


@app.route("/")
def index():
    # 取得資料庫最新資料
    columns, datas = get_pm25_data_from_mysql()
    # 取出不同縣市
    df = pd.DataFrame(datas, columns=columns)
    # 排序縣市
    counties = sorted(df["county"].unique().tolist())

    county = request.args.get("county", "ALL")
    if county == "ALL":
        df1 = df.groupby("county")["pm25"].mean().reset_index()
        x_data = df1["county"].tolist()

    else:
        # 取得特定縣市的資料
        df = df.groupby("county").get_group(county)
        # 繪製所需資料
        x_data = df["site"].tolist()

    # 7:11優化這個東西
    y_data = df["pm25"].tolist()
    columns = df.columns.tolist()
    datas = df.values.tolist()

    return render_template(
        "index.html",
        columns=columns,
        datas=datas,
        counties=counties,
        selected_county=county,
        x_data=x_data,
        y_data=y_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
