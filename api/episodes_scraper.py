import importlib
from providers.a4kScrapers import en as scrapers
from flask_restful import Resource, request
from flask import jsonify

class EpisodesScraper(Resource):
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

        simple_info = {}
        simple_info['show_title'] = request.args.get('show_title')
        simple_info['episode_title'] = request.args.get('episode_title') or ''
        simple_info['year'] = request.args.get('year')
        simple_info['season_number'] = request.args.get('season')
        simple_info['episode_number'] = request.args.get('episode')
        simple_info['show_aliases'] = request.args.get('show_aliases') or []
        simple_info['country'] = request.args.get('country') or ''
        simple_info['no_seasons'] = request.args.get('seasons') or request.args.get('season')

        all_info = {}
        all_info['showInfo'] = {}
        all_info['showInfo']['ids'] = {}
        all_info['showInfo']['ids']['imdb'] = request.args.get('imdb')
        print('===> Search request for show = ', simple_info)
        results = []
        for scraper in selected_scrapers:
            scraper_sources = self.get_scraper_sources(self.torrent_scrapers[scraper], scraper)
            results += scraper_sources.episode(simple_info, all_info)
        return jsonify(results)
