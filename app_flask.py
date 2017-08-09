#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from botocore.exceptions import ClientError
from adn_mutante import esMutante, ADNException
from adn_db import ADNDb

app = Flask(__name__)

@app.route('/')
def index():
    return "Test de ADN mutante."

@app.route('/mutant', methods=['POST'])
def post_mutant():
    dna = request.json['dna']
    adn_db = ADNDb()

    try:
        es_mutante = None

        if adn_db.existe_adn(dna):
            es_mutante = bool(adn_db.get_test(dna)['esMutante'])
        else:
            es_mutante = esMutante(dna)
            adn_db.guardar_test(dna, esMutante)

        return jsonify({"esMutante" : es_mutante}), (200 if es_mutante else 403)
    except ADNException as adn_ex:
        return jsonify({"error_text" : str(adn_ex)}), 400
    except ClientError as ce:
        return jsonify({"error_text" : ce.response['Error']['Message']}), 500
    except Exception as ex:
        return jsonify({"error_text" : str(ex)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    adn_db = ADNDb()
    try:
        stats = adn_db.get_stat()
        return jsonify(stats), 200
    except ClientError as ce:
        return jsonify({"error_text" : ce.response['Error']['Message']}), 500
    except Exception as ex:
        return jsonify({"error_text" : str(ex)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)


