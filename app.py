import datetime
from flask import Flask, jsonify,  render_template, request, redirect
from services.urls import UrlValidators
from services.scrape import DataScrapingService
from services.network import NetworkService

app = Flask(__name__)

url_validator = UrlValidators()

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method != 'POST':
        return render_template('index.html')
    url = url_validator.clean_url(request.form.get('url'))
    return redirect(f'/v1/scrape?url={url}') if url_validator.validate_url(url) else render_template('index.html', error='Invalid URL!')

@app.route("/v1/scrape", methods=['GET'])
def scrape_data():
    url = url_validator.clean_url(request.args.get('url'))
    if not (url_validator.validate_url(url)):
        return jsonify({'error': 'Invalid URL!'}), 400

    data_scraping_service = DataScrapingService()
    data = data_scraping_service.get_data(url)

    network_service = NetworkService()
    data["network"] = network_service.get_data(url)

    data["data_scraped_at"] = datetime.datetime.now()

    return jsonify(data), 200
