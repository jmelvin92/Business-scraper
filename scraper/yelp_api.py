import os
import requests
from typing import List, Dict

class YelpSearcher:
    def __init__(self):
        self.api_key = os.environ.get('YELP_API_KEY')
        self.base_url = 'https://api.yelp.com/v3/businesses/search'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def search_businesses(self, location: str, radius: int = 5, category: str = 'all') -> List[Dict]:
        if not self.api_key:
            print("Warning: No Yelp API key found. Using mock data.")
            return self._get_mock_data()
        
        radius_meters = int(radius * 1609.34)
        
        params = {
            'location': location,
            'radius': min(radius_meters, 40000),
            'limit': 50,
            'offset': 0
        }
        
        if category != 'all':
            params['categories'] = category
        
        all_businesses = []
        
        try:
            while len(all_businesses) < 200:
                response = requests.get(self.base_url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    businesses = data.get('businesses', [])
                    
                    if not businesses:
                        break
                    
                    all_businesses.extend(businesses)
                    
                    if len(businesses) < 50:
                        break
                    
                    params['offset'] += 50
                else:
                    print(f"Yelp API error: {response.status_code}")
                    break
            
            return all_businesses
            
        except Exception as e:
            print(f"Error fetching from Yelp: {e}")
            return self._get_mock_data()
    
    def _get_mock_data(self) -> List[Dict]:
        return [
            {
                'name': 'Sample Business 1',
                'url': '',
                'display_phone': '(555) 123-4567',
                'location': {
                    'display_address': ['123 Main St', 'Anytown, ST 12345']
                },
                'categories': [{'title': 'Restaurant'}],
                'rating': 4.5,
                'review_count': 100
            },
            {
                'name': 'Sample Business 2',
                'url': 'https://yelp.com/biz/sample',
                'display_phone': '(555) 987-6543',
                'location': {
                    'display_address': ['456 Oak Ave', 'Anytown, ST 12345']
                },
                'categories': [{'title': 'Plumber'}],
                'rating': 4.2,
                'review_count': 50
            },
            {
                'name': 'Sample Business 3',
                'url': '',
                'display_phone': '(555) 456-7890',
                'location': {
                    'display_address': ['789 Pine Rd', 'Anytown, ST 12345']
                },
                'categories': [{'title': 'Retail'}],
                'rating': 4.8,
                'review_count': 75
            }
        ]