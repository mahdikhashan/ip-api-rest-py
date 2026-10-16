import os
from dataclasses import dataclass

from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


class UnhandledFormatValue(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return {**(self.payload or {}), "message": self.message}


@app.errorhandler(UnhandledFormatValue)
def unhandled_format_value(e):
    return jsonify(e.to_dict()), e.status_code


@dataclass
class IPDtoResponse:
    ip: str

    def __str__(self):
        return self.ip

    def json(self):
        return jsonify(ip=self.ip, author="mahdikhashan1@gmail.com")


def client_ip() -> str:
    """Return the caller's IP, preferring the first X-Forwarded-For entry."""
    forwarded = request.headers.getlist("X-Forwarded-For")
    return forwarded[0] if forwarded else request.remote_addr


@app.route("/", methods=["GET"])
def get_ip():
    ip = IPDtoResponse(client_ip())
    if request.args.get("format") == "json":
        return make_response(ip.json(), 200)
    return make_response(str(ip), 200)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=os.environ.get("FLASK_DEBUG", "1") == "1",
    )
