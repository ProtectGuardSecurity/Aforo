from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Función para obtener el número actual de personas
def get_current_count():
    conn = sqlite3.connect("aforo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM contador WHERE id=1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

@app.route("/aforo", methods=["GET"])
def aforo():
    contador = get_current_count()
    return jsonify({"personas": contador})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

