from typing import List, Dict
from flask import Flask, render_template
import os
import random
import mysql.connector

app = Flask(__name__)

def test_table() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'devopsroles'
    }

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT url FROM test_table')
    results = [{'url': url} for (url,) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route("/")
def index():
    results = test_table()
    url = random.choice(results)['url']
    return render_template("index.html", url=url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
