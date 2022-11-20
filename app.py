import datetime
from flask import Flask, jsonify,  render_template, request, redirect
from services.urls import UrlValidators
from services.scrape import DataScrapingService
from services.network import NetworkService

app = Flask(__name__)

url_validator = UrlValidators()
