import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id_member>', methods=['GET'])
def get_member(id_member):
    member = jackson_family.get_member(id_member)
    if member is None:
        return jsonify({'err': 'member not found'}), 404
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    try:
        new_member = request.json
        jackson_family.add_member(new_member)
        return jsonify(new_member), 200  
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/member/<int:id_member>', methods=['DELETE'])
def delete_member(id_member):
    member = jackson_family.get_member(id_member)
    if member is None:
        return jsonify({'err': 'member not found'}), 404
    jackson_family.delete_member(id_member)
    return jsonify({"done": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
