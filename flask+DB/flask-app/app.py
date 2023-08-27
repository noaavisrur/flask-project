from flask import Flask, render_template, request, jsonify
import os
import random
import mysql.connector
import requests

app = Flask(__name__)

def query_db(query, fetch_all=True):
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'devopsroles'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(query)
    
    if fetch_all:
        results = cursor.fetchall()
    else:
        results = cursor.fetchone()

    cursor.close()
    connection.close()
    return results

def fetch_lyrics_from_external_api(title, artist):
    # Replace this with the real API endpoint and parameters
    api_url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['lyrics']
    else:
        return None

@app.route("/")
def index():
    results = query_db('SELECT url FROM test_table')
    url = random.choice(results)[0]
    return render_template("index.html", url=url)

@app.route("/api/lyrics", methods=['GET'])
def lyrics_api():
    title = request.args.get('title')
    artist = request.args.get('artist')
    
    # Try to fetch lyrics from your own database first
    results = query_db(f"SELECT lyrics FROM lyrics_table WHERE title='{title}' AND artist='{artist}'", fetch_all=False)
    lyrics = results[0] if results else None
    
    # If not found in database, fetch from external API
    if not lyrics:
        lyrics = fetch_lyrics_from_external_api(title, artist)
        if lyrics:
            query_db(f"INSERT INTO lyrics_table (title, artist, lyrics) VALUES ('{title}', '{artist}', '{lyrics}')", fetch_all=False)

    if lyrics:
        return jsonify({"lyrics": lyrics})
    else:
        return jsonify({"message": "Lyrics not found."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
