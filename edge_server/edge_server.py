#!flask/bin/python
from flask import Flask
from flask import request, url_for
from flask import jsonify, abort
from dna import Dna
from werkzeug.utils import secure_filename
from alphabot_exceptions import *
import os
from prometheus_flask_exporter import PrometheusMetrics

DEFAULT_IP_ADDR = '192.168.1.114'
DEFAULT_PORT = 8000

IP_ADDR = os.getenv('EDGE_SERVER_IP_ADDR')
if IP_ADDR is None:
    print ("Environmemnt variable 'EDGE_SERVER_IP_ADDR' is not set, using "
           "default ip: %s" % DEFAULT_IP_ADDR)
    IP_ADDR = DEFAULT_IP_ADDR

PORT = os.getenv('EDGE_SERVER_PORT')
if PORT is None:
    print ("Environmemnt variable 'EDGE_SERVER_PORT' is not set, using "
           "default port: %d" % DEFAULT_PORT)
    PORT = DEFAULT_PORT
else:
    PORT = int(PORT)

D = Dna()
app = Flask(__name__)
PrometheusMetrics(app)


@app.route('/', methods = ['GET', 'POST'])
def post_image():
    if request.method != 'POST':
        return "%s \n" % request.method

    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(filename)
    dirr = os.getcwd()
    osname = os.path.join(dirr, '')
    dest_img = osname + filename
    try:
        results = D.find_distance_and_angle(dest_img)  ### pairnei path
        os.remove(dest_img)
        return jsonify(results)
    except BeaconNotFoundError:
        os.remove(dest_img)
        return abort (404)

def main():
    app.run(host=IP_ADDR, port=PORT, threaded=False)

if __name__ == '__main__':
    main()
