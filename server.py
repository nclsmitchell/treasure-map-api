#!/usr/bin/env python3
# coding: utf-8

import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from script import treasure_map

# Instantiate Flask app
app = Flask(__name__)
cors = CORS(app)

@app.route('/parse', methods=['POST'])
def parse():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['data']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Parse input value
    def parsing(values):
        output = {
            'C': None,
            'M': [],
            'T': [],
            'A': []
        }
        lines = values.split('\n')

        for line in lines:
            cells = line.split(' - ')
            if cells[0] == 'C':
                output['C'] = [int(cells[1]), int(cells[2])]
            elif cells[0] == 'M':
                output['M'].append([int(cells[1]), int(cells[2])])
            elif cells[0] == 'T':
                output['T'].append([int(cells[1]), int(cells[2]), int(cells[3])])
            elif cells[0] == 'A':
                output['A'].append({
                    'name': cells[1],
                    'position': [int(cells[2]), int(cells[3])],
                    'direction': cells[4],
                    'actions': cells[5],
                })
            else:
                continue

        return output

    response = parsing(values['data'])

    return jsonify(response), 200


@app.route('/map/init', methods=['POST'])
def get_init_state():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['C', 'M', 'T', 'A']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Map
    response = treasure_map.RunTreasureMap(values['C'], values['M'], values['T'], values['A']).get_init_state

    return jsonify(response), 200


@app.route('/map/turn/<path:turn>', methods=['POST'])
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
