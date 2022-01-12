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
        title = request.args.get('title')
        year = request.args.get('year')
        imdb = request.args.get('imdb')
        print('===> Search request for title = [' + title + "] year = [" + year + "] imdb = [" + imdb + "]")
        results = []
        for scraper in scrapers.get_torrent():
            try:
                scraper_sources = self.get_scraper_sources(self.torrent_scrapers[scraper], scraper)
                results += scraper_sources.movie(title, year, imdb)
            except Exception as e:
                print('Scraper {scraper} error', e)
        return jsonify(results)
