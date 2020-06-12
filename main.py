# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from celeryTasks import run_all_scripts
app = Flask(__name__)


@app.route('/servicebrute', methods=['POST','GET'])
def route():
    try:
        host = request.form['host']
        port = request.form['port']
        asset_id = request.form['asset_id']
        is_https = request.form['is_https']
        run_all_scripts.delay(host, port, asset_id, is_https)
        return jsonify(code=1, message=u'already get task', error='')
    except Exception as error:
        return jsonify(code=0, message='', error=str(error))


if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8082",debug=True)
