from flask import Flask, render_template, jsonify
from app.Services.DomainSearchService import GoogleSearch


app = Flask('motor-search-ecommerces', template_folder='resources/views')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search/<terms>')
def search_term(terms):
    found_domains = GoogleSearch().search_for(terms)

    return jsonify({
        'status': True,
        'data': found_domains
    })