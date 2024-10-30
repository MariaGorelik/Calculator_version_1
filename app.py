from flask import Flask, render_template, request, jsonify
import locale
import re

app = Flask(__name__)

locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

MIN_VALUE = -1000000000000.000000
MAX_VALUE = 1000000000000.000000


def check_overflow(number):
    return number < MIN_VALUE or number > MAX_VALUE


def parse_number(number_str):
    number_str = number_str.replace(',', '.')
    if not re.match(r'^-?\d+(\.\d+)?$', number_str):
        return None
    try:
        return float(number_str)
    except ValueError:
        return None


def arithmetic_round(number, decimals=0):
    factor = 10 ** decimals
    return int(number * factor + 0.5) / factor if number >= 0 else int(number * factor - 0.5) / factor


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    number1_str = request.form.get('number1')
    number2_str = request.form.get('number2')
    operation = request.form.get('operation')

    number1 = parse_number(number1_str)
    number2 = parse_number(number2_str)

    if number1 is None or number2 is None:
        return jsonify({'error': 'Invalid input'})

    if check_overflow(number1) or check_overflow(number2):
        return jsonify({'error': 'Overflow'})

    if operation == 'add':
        result = number1 + number2
    elif operation == 'subtract':
        result = number1 - number2
    else:
        return jsonify({'error': 'Unknown operation'})

    if check_overflow(result):
        return jsonify({'error': 'Overflow'})

    return jsonify({'result': f'{arithmetic_round(result, 6)}'})


if __name__ == '__main__':
    app.run(debug=True)
