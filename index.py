import socket

from flask import Flask, request, jsonify
from flask_cors import CORS

import controllers


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


app = Flask(__name__)
cors = CORS(app)


@app.route('/users/<username>/cases/create/', methods=["POST"])
def create_case(username):
    data = request.get_json(force=True)
    controllers.create_case(username, data)
    return jsonify({})


@app.route('/users/<username>/cases/update/', methods=["PUT"])
def update_case(username):
    data = request.get_json(force=True)
    controllers.update_case(username, data)
    return jsonify({})


@app.route('/users/<username>/cases/', methods=["GET"])
def get_cases(username):
    return jsonify(controllers.get_cases(username))


@app.route('/users/<username>/cases/optimize/', methods=["GET"])
def optimize(username):
    case_name = request.args.get('case_name')
    max_execution_time = float(request.args.get('max_execution_time', default=1))
    strategy = request.args.get('strategy', default='ga')
    solution = controllers.optimize(username, case_name, max_execution_time, strategy)
    return jsonify(solution)


@app.route('/users/create/', methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    success = controllers.create_user(data)
    if not success:
        return jsonify({'error': 'El usuario ya existe!'})
    return jsonify({})


@app.route('/users/<username>/cases/<casename>/delete/', methods=["DELETE"])
def delete_case(username, casename):
    controllers.delete_case(username, casename)
    return jsonify({})


if __name__ == "__main__":
    print("LOCAL IP IS: {}".format(get_local_ip()))
    app.run(host='0.0.0.0', port='5000')
