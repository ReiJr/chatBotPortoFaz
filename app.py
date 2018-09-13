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
        print ("ENTROU NA FUNÇÃO PORRA")
        global speech
        speech = "nalds"
        if req.get("queryResult").get("action")!= "portofaz":
                return {}
        result = req.get("queryResult")
        parameters = result.get("parameters")
        print (parameters)
        print ("AQUI!++++++++++ " + str(parameters))
        if "servico" in str(parameters):
            name = parameters.get("servico")
            speech = "Olá, a Porto Faz consegue ajudar com " + name + ",quer mais detalhe que sobre o serviço?"
                
        elif "cep" in str(parameters):
            name = parameters.get("cep")
            speech = "seu cep" + name
        print ("Response: ")
        print (speech)
        return {
                "fulfillmentText": speech,
                "source": "portofaz"
                }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
