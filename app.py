from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = "database/legalease.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_type TEXT, name TEXT, details TEXT,
        content TEXT, created_at TEXT
    )""")
    conn.commit()
    conn.close()

def make_document(doc_type, name, details):
    return f"""LEGAL DOCUMENT - {doc_type.upper()}

Name: {name}
Date: {datetime.now().strftime("%d-%m-%Y")}

DETAILS
{details}

DECLARATION
I confirm that the information provided above is true to the best of my knowledge.

IMPORTANT NOTICE
This is an educational document template and should be reviewed by a qualified legal professional before actual use.
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        doc_type = request.form["doc_type"]
        name = request.form["name"]
        details = request.form["details"]
        content = make_document(doc_type, name, details)

        conn = sqlite3.connect(DB)
        conn.execute(
            "INSERT INTO documents (doc_type,name,details,content,created_at) VALUES (?,?,?,?,?)",
            (doc_type, name, details, content,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        conn.close()
        return render_template("result.html", content=content)

    return render_template("index.html")

@app.route("/documents")
def documents():
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT id,doc_type,name,created_at FROM documents ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("documents.html", rows=rows)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
