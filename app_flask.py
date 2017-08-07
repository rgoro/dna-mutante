#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from adn_mutante import esMutante, ADNException

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/mutant', methods=['POST'])
def post_mutant():
    dna = request.json['dna']
    try:
        es_mutante = esMutante(dna)

        return jsonify({"esMutante" : es_mutante}), (200 if es_mutante else 403)
    except ADNException as adn_ex:
        return jsonify({"error_text" : str(adn_ex)}), 400
    except Exception as ex:
        return jsonify({"error_text" : str(ex)}), 500


if __name__ == '__main__':
    app.run(debug=True)


