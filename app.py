
from flask import Flask, render_template, request, session, abort
from pm25 import get_pm25, get_six_pm25, get_countys, get_county_pm25
import json
from stock import get_stocks

app = Flask(__name__)

app.secret_key = "python is good"
sort = False


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


@app.route('/pm25', methods=['GET', 'POST'])
def pm25():
    global sort
    if request.method == 'POST':
        sort = not sort

    date = get_date()
    columns, values = get_pm25(sort)
    return render_template('./pm25.html', **locals())


@app.route('/pm25-charts')
def pm25_charts():

    return render_template('./pm25-charts-bulma.html', countys=get_countys())


@app.route('/pm25-json', methods=['POST'])
def pm25_json():
    columns, values = get_pm25()
    site = [value[1] for value in values]
    pm25 = [value[2] for value in values]
    date = values[0][-1]

    return json.dumps({'date': date, 'site': site, 'pm25': pm25}, ensure_ascii=False)


@app.route('/pm25-six-json', methods=['POST'])
def pm25_six_json():
    values = get_six_pm25()
    site = [value[0] for value in values]
    pm25 = [value[1] for value in values]

    return json.dumps({'site': site, 'pm25': pm25}, ensure_ascii=False)


@app.route('/pm25-county/<county>', methods=['POST'])
def pm25_county_json(county):
    try:
        values = get_county_pm25(county)
        site = [value[0] for value in values]
        pm25 = [value[1] for value in values]

        return json.dumps({'site': site, 'pm25': pm25}, ensure_ascii=False)
    except:
        return '取得資料失敗!'


if __name__ == '__main__':
    pm25_json()
    app.run(debug=True)
