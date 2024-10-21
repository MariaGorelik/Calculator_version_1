from flask import Flask, render_template, request, jsonify
import locale

app = Flask(__name__)

locale.setlocale(locale.LC_NUMERIC, '')

MIN_VALUE = -1000000000000.000000
MAX_VALUE = 1000000000000.000000


def check_overflow(result):
    return result < MIN_VALUE or result > MAX_VALUE


def parse_number(number_str):
    number_str = number_str.replace(',', '.')
    try:
        return float(number_str)
    except ValueError:
        return None


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

    if operation == 'add':
        result = number1 + number2
    elif operation == 'subtract':
        result = number1 - number2
    else:
        return jsonify({'error': 'Unknown operation'})

    if check_overflow(result):
        return jsonify({'error': 'Overflow'})

    return jsonify({'result': f'{result:.6f}'})


if __name__ == '__main__':
    app.run(debug=True)
