# -*- coding:utf-8 -*-
import flask
import socket
import fcntl
import time
import broadcast

# 参考: https://sites.google.com/site/tibracode/python/socket

app = flask.Flask(__name__)


@app.route('/device', methods=['GET'])
def device_search():
  # parameter check
  if ( not flask.request.args["l2id"] ) or ( not flask.request.args["port"] ) : return flask.abort(400)
  l2id = flask.request.args["l2id"]
  port = flask.request.args["port"]
  response = flask.jsonify({'devices': broadcast.main_broadCast(l2id, port).values()})
  response.status_code = 200
  return response



@app.route('/device/<l2id>', methods=['GET'])
def deviceL2id(l2id):
  response = flask.jsonify({'devices': broadcast.main_broadCast(l2id).values()})
  response.status_code = 200
  return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
