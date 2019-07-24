#!/usr/bin/env python
import requests
import json
import os
import sys
import time
import random

IP_ADDR = os.getenv('EDGE_SERVER_IP_ADDR')
if IP_ADDR is None:
    sys.exit("Environmemnt variable 'EDGE_SERVER_IP_ADDR' is not set")

PORT = os.getenv('EDGE_SERVER_PORT')
if PORT is None:
    sys.exit("Environmemnt variable 'EDGE_SERVER_PORT' is not set")

POST_URL = "http://%s:%s/" % (IP_ADDR, PORT)

IMAGES_PATH = os.getenv('IMAGES_PATH', '/tmp/images/')

IMAGES = []
for (dirpath, dirnames, filenames) in os.walk(IMAGES_PATH):
    IMAGES.extend(filenames)
    break
print 'Discovered images: %s' % str(IMAGES)

RUNNING_SECONDS = float(os.getenv('RUNNING_PERIOD', '60'))
RUNNING_INTERVAL = float(os.getenv('RUNNING_INTERVAL', '1'))

def post_once():
    image = os.path.join(IMAGES_PATH, random.choice(IMAGES))
    print 'Using image: %s' % str(image)
    try:
        requests.post(POST_URL, files={"file": open(image, "rb")})
    except requests.exceptions.ConnectionError as e:
        print "Error while trying to post once: %s" % e

def main():
    start_time = time.time()
    while (time.time() - start_time) < RUNNING_SECONDS:
        iteration_start_time = time.time()
        post_once()
        sleep_time = max(0, RUNNING_INTERVAL - (time.time() -
                                                iteration_start_time))
        print 'sleeping for %f' % sleep_time
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
