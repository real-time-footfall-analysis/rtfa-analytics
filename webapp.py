from flask import Flask

from handler.request_handler import RequestHandler

app = Flask(__name__)


@app.route("/health")
def health():
    return '', 200


@app.route("/compute/<int:freqGroupID>")
def handle_compute(freqGroupID):
    handler = RequestHandler()
    result = handler.execute_tasks(freqGroupID)
    return result, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
