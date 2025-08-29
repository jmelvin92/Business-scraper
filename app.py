from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from scraper.yelp_api import YelpSearcher
from scraper.google_scraper import GoogleMapsSearcher
from scraper.simple_scraper import SimpleGoogleSearcher
from scraper.yellowpages_scraper import YellowPagesSearcher
from scraper.working_scraper import WorkingGoogleScraper
from scraper.simple_reliable_scraper import SimpleReliableScraper
from scraper.validator import WebsiteValidator
from scraper.exporter import CSVExporter

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        city = data.get('city')
        state = data.get('state')
        radius = data.get('radius', 5)
        category = data.get('category', 'all')
        
        if not city or not state:
            return jsonify({'error': 'City and state are required'}), 400
        
        location = f"{city}, {state}"
        
        # Use simple reliable scraper for consistent results
        scraper = SimpleReliableScraper()
        businesses = scraper.search_businesses(location, radius, category)
        
        # If no results, provide feedback
        if not businesses:
            return jsonify({
                'success': True,
                'total_found': 0,
                'without_websites': 0,
                'businesses': [],
                'message': f'No {category} businesses found in {location}. Try a different category or location.'
            })
        
        print(f"Processing {len(businesses)} businesses...")
        
        validator = WebsiteValidator()
        processed_businesses = []
        without_website_count = 0
        
        for i, business in enumerate(businesses):
            print(f"Business {i+1}: {business.get('name', 'Unknown')} - URL: {business.get('url', 'No URL')}")
            has_website = validator.has_website(business)
            print(f"  Has website: {has_website}")
            
            if not has_website:
                without_website_count += 1
                
            processed_businesses.append({
                'name': business.get('name'),
                'phone': business.get('display_phone', 'N/A'),
                'address': ', '.join(business.get('location', {}).get('display_address', [])),
                'categories': ', '.join([c['title'] for c in business.get('categories', [])]),
                'rating': business.get('rating', 'N/A'),
                'review_count': business.get('review_count', 0),
                'has_website': has_website,
                'website_url': business.get('url', '')
            })
        
        result = {
            'success': True,
            'total_found': len(businesses),
            'without_websites': without_website_count,
            'businesses': processed_businesses
        }
        
        print(f"Returning {len(processed_businesses)} processed businesses to client")
        print(f"Sample business data: {processed_businesses[0] if processed_businesses else 'None'}")
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['POST'])
def export():
    try:
        data = request.json
        businesses = data.get('businesses', [])
        
        if not businesses:
            return jsonify({'error': 'No businesses to export'}), 400
        
        exporter = CSVExporter()
        filename = exporter.export(businesses)
        
        return send_file(filename, as_attachment=True, download_name=f'businesses_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)