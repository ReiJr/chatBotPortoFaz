import urllib
import json
import os
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)
@app.route("/", methods=['GET'])
def hello():
        return "Hello from Python!"


@app.route('/webhook', methods=['POST'])
def webhook():
#        speech = "nalds"
        global speech
        req = request.get_json(silent=True, force=True)
        print ("Request:")
        print (json.dumps(req, indent=4))
        res = makeWebhookResult(req)
        res = json.dumps(res, indent=4)
        print (res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r
def makeWebhookResult(req):
        global speech
        speech = "nalds"
        if req.get("queryResult").get("action")!= "portofaz":
                return {}
        result = req.get("queryResult")
        parameters = result.get("parameters")
        print ("Parametro: " + str(parameters))
        if (parameters == "servico"):
#            global speech
            name = parameters.get("servico")
        #bank = {'Federal Bank':'6.7%', 'Andhra Bank':'6.85%', 'Bandhan Bank':'7.15%'}
            speech = "Olá, a Porto Faz consegue ajudar com " + name + ",quer mais detalhe que sobre o serviço?"
            print ("Speech: " + speech)
        #global speech
        print ("Response: ")
        print (speech)
        return {
                "fulfillmentText": speech,
                "source": "portofaz"
                }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
