from flask import Flask,request
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    print(request.form['password'])
    return {"password":request.form['password']}