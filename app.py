
from flask import Flask, render_template, request, session
from pm25 import get_pm25
import json
from stock import get_stocks

app = Flask(__name__)

app.secret_key = "python is good"


@app.route('/<name>')
@app.route('/')
def index(name='GUEST'):
    from datetime import datetime
    session['username'] = name
    now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return render_template('./test.html', now=now, name=name)


@app.route('/date')
def get_date():

    from datetime import datetime
    return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@app.route('/book/<id>')
def get_book(id):

    return 'hello'+id


@app.route('/bmi/weight=<weight>&height=<height>')
def get_bmi(weight, height):
    bmi = round(eval(weight)/(eval(height)/100)**2, 4)
    return f'BMI:{bmi}'


@app.route('/hello')
def get_index():
    from datetime import datetime
    now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(now)
    name = request.args.get('name')
    return render_template('./test.html', now=now, name=name)


@app.route('/stock')
def get_stock():
    # stocks = [
    #     {'分類': '日經指數', '指數': '22,920.30'},
    #     {'分類': '韓國綜合', '指數': '2,304.59'},
    #     {'分類': '香港恆生', '指數': '25,083.71'},
    #     {'分類': '上海綜合', '指數': '3,380.68'}
    # ]
    return render_template('./stock.html', date=get_date(), stocks=get_stocks())


sort = False


@app.route('/pm25', methods=['POST', 'GET'])
def pm25():
    global sort
    if request.method == 'POST':
        sort = not sort
    date = get_date()
    columns, values = get_pm25(sort)

    # print(columns, values)
    return render_template('pm25.html', date=date, columns=columns, values=values)


@app.route('/pm25-charts')
def pm25_charts():

    return render_template('pm25_charts.html')


@app.route('/pm25-json')
def pm25_json():
    columns, values = get_pm25()
    site = [value[1] for value in values]
    pm25 = [value[2] for value in values]

    return json.dumps({'site': site, 'pm25': pm25}, ensure_ascii=False)


if __name__ == '__main__':

    app.run(debug=True)
