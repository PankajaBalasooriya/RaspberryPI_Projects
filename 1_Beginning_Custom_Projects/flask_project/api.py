from flask import Flask

app = Flask(__name__)

@app.route("/led/on")
def led_on():
    # return "Turing on the LED"
    return {'status': True}