from time import sleep

from flask import Flask, jsonify, render_template
from flask_executor import Executor
import requests


app = Flask(__name__)
executor = Executor(app)

# runs in exponential time!
def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)

@app.route('/start-task')
def start_task():
    executor.submit_stored('fib', fib, 37)
    return render_template('t.html')

@app.route('/get-result')
def get_result():
    if not executor.futures.done('fib'):
        return jsonify({'status': executor.futures._state('fib')})
    future = executor.futures.pop('fib')
    return jsonify({'status': 'done', 'result': future.result()})

if __name__ == '__main__':
    app.run(debug=True)

