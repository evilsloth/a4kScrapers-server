import importlib
from providers.a4kScrapers import en as scrapers
from flask_restful import Resource, request
from flask import jsonify

class MoviesScraper(Resource):
    scraper_sources_dict = {}
    torrent_scrapers = {}

    def __init__(self):
        for scraper in scrapers.get_torrent():
            self.torrent_scrapers[scraper] = importlib.import_module('providers.a4kScrapers.en.torrent.%s' % scraper)        

    def get_scraper_sources(self, scraper_module, scraper):
        if self.scraper_sources_dict.get(scraper, None) is None:
            self.scraper_sources_dict[scraper] = scraper_module.sources()
        return self.scraper_sources_dict[scraper]

    def get(self):
        selected_scrapers = scrapers.get_torrent()

        if (request.args.get('scraper')):
            selected_scrapers = [request.args.get('scraper')]

        title = request.args.get('title')
        year = request.args.get('year')
        imdb = request.args.get('imdb')
        print('===> Search request for title = [' + title + "] year = [" + str(year) + "] imdb = [" + str(imdb) + "]")
        results = []
        for scraper in selected_scrapers:
            scraper_sources = self.get_scraper_sources(self.torrent_scrapers[scraper], scraper)
            results += scraper_sources.movie(title, year, imdb)
        return jsonify(results)
