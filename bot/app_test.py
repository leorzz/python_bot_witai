import os, sys
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))