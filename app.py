import urllib
import json
import os
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route("/")
def hello():
        return "Hello from Python!"

@app.route('/webhook', methods=['POST'])
def webhook():
        req = request.get_json(silent=True, force=True)
        print ("Request:")
        print (json.dumps(req, indent=4))
        res = makeWehookResult(req)
        res = json.dumps(res, indent=4)
        print (res)
        r = make_response(res)
        r.header['Content-Type'] = 'application/json'
        return r

def makeWebhookResult(req):
        if req.get("result").get("action")!= "portofaz":
                return {}
        result = req.get("queryResult")
        parameters = result.get("parameters")
        name = parameters.get("servico")
        #bank = {'Federal Bank':'6.7%', 'Andhra Bank':'6.85%', 'Bandhan Bank':'7.15%'}
        speech = "Olá, a Porto Faz consegue ajudar com " + name + ",quer mais detalhe que sobre o serviço?"
        print ("Response: ")
        print (speech)
        return {
                "fulfillmentText": speech,
                "source": "portofaz"
                }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
