from flask import Flask, render_template, request
from datetime import datetime
import pandas as pd
import pymysql
from pm25 import get_pm25_data_from_mysql, update_db
import json

app = Flask(__name__)


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
    columns, datas = get_pm25_data_from_mysql()
    return render_template("index.html", columns=columns, datas=datas)


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
