#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "user.id":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    id1 = parameters.get("user-id")
    pass1 = parameters.get("password")
    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    if(str(cost[id1])==pass1):
        speech = "The cost of shipping to " + id1 + " is " + str(cost[id1]) + " euros."
    else:
        speech = "error"
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
