from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import pymysql
from pm25 import get_pm25_data_from_mysql, update_db
import json

app = Flask(__name__)


@app.route("/filter", methods=["POST"])
def filter_data():
    # args=>form
    county = request.form.get("county")
    columns, datas = get_pm25_data_from_mysql()
    df = pd.DataFrame(datas, columns=columns)
    # 取得特定縣市的資料
    df1 = df.groupby("county").get_group(county).groupby("site")["pm25"].mean()
    print(df1)
    return {"county": county}


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
    # print(counties)

    # columns, datas = get_pm25_data_from_mysql()
    # df = pd.DataFrame(datas, columns=columns)

    # 選取縣市後的資料(預設ALL)
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


@app.route("/books")
def books_page():
    # return f"<h1>Hello World!</h1><br>{datetime.now()}"
    books = [
        {
            "name": "Python book",
            "price": 299,
            "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
        },
        {
            "name": "Java book",
            "price": 399,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
        },
        {
            "name": "C# book",
            "price": 499,
            "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
        },
    ]

    books = []
    if books:
        for book in books:
            print(book["name"])
            print(book["price"])
            print(book["image_url"])
    else:
        print("販售完畢")

    username = "chase"
    nowtime = datetime.now().strftime("%Y-%m-%d")
    print(username, nowtime)
    return render_template("books.html", name=username, now=nowtime, books=books)


@app.route("/bmi")
def get_bmi():
    # args->GET
    height = eval(request.args.get("height"))
    weight = eval(request.args.get("weight"))

    print(height, weight)

    bmi = round(weight / (height / 100) ** 2, 2)

    # return {"height": height, "weight": weight, "bmi": bmi}
    return render_template("bmi.html", **locals())


if __name__ == "__main__":
    app.run(debug=True)
