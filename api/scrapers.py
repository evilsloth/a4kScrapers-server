from providers.a4kScrapers import en as scrapers
from flask_restful import Resource, request
from flask import jsonify

class Scrapers(Resource):

    def get(self):
        return jsonify(scrapers.get_torrent())
