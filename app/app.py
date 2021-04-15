from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'winnersData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Winners Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarWinners')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, winners=result)


@app.route('/view/<int:name_index>', methods=['GET'])
def record_view(name_index):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarWinners WHERE index=%s', name_index)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', name=result[0])


@app.route('/edit/<int:name_index>', methods=['GET'])
def form_edit_get(name_index):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarWinners WHERE index=%s', name_index)
    return render_template('edit.html', title='Edit Form', name=result[0])


@app.route('/edit/<int:name_index>', methods=['POST'])
def form_update_post(name_index):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Year'), request.form.get('Age'),
                 request.form.get('Name'), request.form.get('Movie'),
                 request.form.get('Extra'), name_index)
    sql_update_query = """UPDATE tblOscarWinners t SET t.Year = %s, t.Age = %s, t.Name = %s, t.Movie = 
    %s, t.Extra = %s WHERE t.index = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/winners/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Winner Form')


@app.route('/winners/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Year'), request.form.get('Age'), request.form.get('Name'),
                 request.form.get('Movie'), request.form.get('Extra'))
    sql_insert_query = """INSERT INTO tblOscarWinners (Year,Age,Name,Movie,Extra) VALUES (%s, %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:name_index>', methods=['POST'])
def form_delete_post(name_index):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblOscarWinners WHERE index = %s """
    cursor.execute(sql_delete_query, name_index)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/winners', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarWinners')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/winners/<int:name_index>', methods=['GET'])
def api_retrieve(name_index) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblOscarWinners WHERE index=%s', name_index)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/winners/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/winners/<int:name_index>', methods=['PUT'])
def api_edit(name_index) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/winners/<int:name_index>', methods=['DELETE'])
def api_delete(name_index) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)