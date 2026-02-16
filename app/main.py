from flask import Flask

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "hello proj"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

