import urllib
import cgi
import json
import os
from flask import Flask
from flask import request
from flask import make_response
from urllib.request import urlopen
from twilio.rest import Client

app = Flask(__name__)
@app.route("/", methods=['GET'])
def hello():
        return "Hello from Python!"


@app.route('/webhook', methods=['POST'])
def webhook():
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
        text = result.get("queryText")
        parameters = result.get("parameters")
        if "servico" in str(parameters):
            name = parameters.get("servico")
            speech = "Olá, a Porto Faz consegue ajudar com " + name + ",quer mais detalhe que sobre o serviço?"
                
        elif "cep" in str(parameters):
            name = parameters.get("cep")
            cep = buscaCEP(text)
            speech = "para " + cep + "?"
        
        elif ("manha" | "tarde" | "manhã") in str(text):
             
        print ("Response: ")
        print (speech)
        return {
                "fulfillmentText": speech,
                "source": "portofaz"
                }

def buscaCEP(text):
        url = "http://cep.republicavirtual.com.br/web_cep.php?cep=" + str(text) + "&formato=query_string"
        pagina      = urlopen(url).read()  
        conteudo    = pagina.decode('utf-8') #pagina.encode('utf-8')
        resultado   = cgi.parse_qs(conteudo)
        print (resultado)
        if resultado['resultado'][0] == '1':
                endereco = resultado['tipo_logradouro'][0] + " " + resultado['logradouro'][0]

        return endereco #.encode('utf-8')    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
