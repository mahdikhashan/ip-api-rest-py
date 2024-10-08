from dataclasses import dataclass
from flask import Flask, request, jsonify, make_response


app = Flask(__name__)


class UnhandledFormatValue(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(UnhandledFormatValue)
def unhandled_format_value(e):
    return jsonify(e.to_dict()), e.status_code


@dataclass
class IPDtoResponse:
    ip: str

    def __str__(self):
        return self.ip

    def json(self):
        return jsonify(ip=self.ip)


@app.route("/", methods=['GET'])
def get_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = IPDtoResponse(request.headers.getlist("X-Forwarded-For")[0])
    else:
        ip = IPDtoResponse(request.remote_addr)

    query_string_format = request.args.get("format")
    if query_string_format == "json":
        return make_response(ip.json(), 200)
    else:
        pass

    return make_response(str(ip), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
