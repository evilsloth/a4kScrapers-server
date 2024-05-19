from providers.a4kScrapers import en as scrapers
from flask_restful import Resource, request
from flask import jsonify

class Scrapers(Resource):

    def get(self):
        # filter out glo for now - returns 500 and causes stack overflow
        # return jsonify(scrapers.get_torrent())
        return jsonify(list(filter(lambda s: s != 'glo', scrapers.get_torrent())))
