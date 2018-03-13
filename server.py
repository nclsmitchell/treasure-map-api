#!/usr/bin/env python3
# coding: utf-8

import os

from flask import Flask, jsonify, request
from script import treasure_map

# Instantiate Flask app
app = Flask(__name__)

@app.route('/map/new', methods=['POST'])
def new_map():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['C', 'M', 'T', 'A']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Map
    Treasure_map = treasure_map.TreasureMap(values['C'], values['M'], values['T'], values['A'])
    response = Treasure_map.get_treasure_map()

    return jsonify(response), 201

@app.route('/map/run', methods=['POST'])
def get_turns():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['C', 'M', 'T', 'A']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Run treasure map
    response = treasure_map.RunTreasureMap(values['C'], values['M'], values['T'], values['A']).get_turns

    return jsonify(response), 200

@app.route('/map/run/<path:turn>', methods=['POST'])
def get_turn(turn):
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['C', 'M', 'T', 'A']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Get treasure map at step `turn`
    response = treasure_map.RunTreasureMap(values['C'], values['M'], values['T'], values['A']).get_turn(turn)

    return jsonify(response), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
