from flask import Flask

app = Flask(__name__)

@app.route("/")
def main_page():
    sum = 3+4+5+6
    return "<h1>helo</h1>"+ str(sum)

    
@app.route("/about")
def about_page():
    return "<h1>helo this is about</h1>"