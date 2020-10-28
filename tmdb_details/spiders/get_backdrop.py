import scrapy
import csv
import json
from dateutil.parser import parse


class GetBackdropSpider(scrapy.Spider):
    name = 'get_backdrop'
    count = 0
    allowed_domains = ['themoviedb.org']
    BASE_IMAGE_URL = 'https://image.tmdb.org/t/p/original'
    GET_MOVIE = 'https://api.themoviedb.org/3/search/movie?api_key=8a026a6164781758d7295d0a434718dc&query={}&page=1'
    GET_BACKDROP = 'https://api.themoviedb.org/3/movie/{}/images?api_key=8a026a6164781758d7295d0a434718dc'

    def start_requests(self):
        with open('tmdb_details/m_v1_movies_for_backdrop.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.count += 1
                yield scrapy.Request(self.GET_MOVIE.format(row['movie_title']), callback=self.parse, meta={'dict': row})

    def parse(self, response):
        response_dict =  response.json()
        movie_dict = response.meta.get('dict')
        if 'results' in response_dict.keys():
            for result in response_dict['results']:
                if 'release_date' in result.keys() and result['release_date']:
                    release_year = parse(result['release_date']).year
                    if str(release_year) == movie_dict['release_year']:
                        return scrapy.Request(self.GET_BACKDROP.format(result['id']), callback=self.parse_backdrop, meta={'dict': movie_dict})
    
    def parse_backdrop(self, resp):
        image_dict = resp.json()
        movie_row = resp.meta.get('dict')
        movie_row['posters'] = json.dumps([self.BASE_IMAGE_URL + poster['file_path'] for poster in image_dict['posters'] if 'posters' in image_dict.keys()])
        movie_row['backdrops'] = json.dumps([self.BASE_IMAGE_URL + backdrop['file_path'] for backdrop in image_dict['backdrops'] if 'backdrops' in image_dict.keys()])
        print(self.count)
        return movie_row
    

