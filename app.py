from flask import Flask, render_template, request, session

app = Flask(__name__)

app.secret_key = "python is good"


@app.route('/<name>')
@app.route('/')
def index(name='GUEST'):
    from datetime import datetime
    session['username'] = name

    now = str(datetime.now().strftime('%Y-%m-%d'))
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
    now = str(datetime.now().strftime('%Y-%m-%d'))
    name = request.args.get('name')
    return render_template('./test.html', now=now, name=name)


@app.route('/stock')
def get_stock():
    stocks = [
        {'分類': '日經指數', '指數': '22,920.30'},
        {'分類': '韓國綜合', '指數': '2,304.59'},
        {'分類': '香港恆生', '指數': '25,083.71'},
        {'分類': '上海綜合', '指數': '3,380.68'}
    ]
    name = session['username']
    return render_template('./stock.html', date=get_date(), stocks=stocks, name=name)


if (__name__) == '__main__':
    app.run(debug=True)
