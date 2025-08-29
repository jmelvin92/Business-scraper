import requests
from typing import Dict
import re

class WebsiteValidator:
    def __init__(self):
        self.timeout = 5
    
    def has_website(self, business: Dict) -> bool:
        url = business.get('url', '')
        
        if not url:
            return False
        
        if 'yelp.com' in url:
            return False
        
        if self._extract_website_from_yelp_data(business):
            return True
        
        return False
    
    def _extract_website_from_yelp_data(self, business: Dict) -> str:
        return None
    
    def validate_url(self, url: str) -> bool:
        if not url:
            return False
        
        if not url.startswith(('http://', 'https://')):
            url = f'http://{url}'
        
        try:
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            return response.status_code < 400
        except:
            return False