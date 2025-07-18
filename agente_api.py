from flask import Flask, request, jsonify
from agente_legal import LegalAgent

app = Flask(__name__)
agente = LegalAgent()

@app.route("/consulta", methods=["POST"])
def consulta_legal():
    data = request.json
    pregunta = data.get("pregunta", "")
    if not pregunta:
        return jsonify({"error": "No se recibió una pregunta válida"}), 400
    respuesta = agente.ask(pregunta)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(port=5000)
