from flask import Flask
from flask_restful import Api
from api.episodes_scraper import EpisodesScraper
from api.movies_scraper import MoviesScraper
from api.scrapers import Scrapers
from waitress import serve
import logging

app = Flask(__name__)
api = Api(app)

logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

api.add_resource(Scrapers, '/scrapers')
api.add_resource(EpisodesScraper, '/episodes')
api.add_resource(MoviesScraper, '/movies')

if __name__ == '__main__':
     serve(app, port='8091')