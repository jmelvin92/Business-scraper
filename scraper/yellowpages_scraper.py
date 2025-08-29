import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
import re

class YellowPagesSearcher:
    def __init__(self):
        self.base_url = "https://www.yellowpages.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def search_businesses(self, location: str, radius: int = 5, category: str = 'barbershop') -> List[Dict]:
        businesses = []
        
        # Format location (city, state)
        location_formatted = location.replace(', ', '-').replace(' ', '-').lower()
        
        # Map our categories to Yellow Pages search terms
        category_map = {
            'barbershop': 'barber-shops',
            'dentist': 'dentists',
            'electrician': 'electricians',
            'plumber': 'plumbers', 
            'handyman': 'handyman-services',
            'hvac': 'heating-and-air-conditioning',
            'roofing': 'roofing-contractors',
            'landscaping': 'landscaping',
            'auto repair': 'auto-repair'
        }
        
        search_term = category_map.get(category.lower().replace(' ', ''), 'businesses')
        
        # Construct URL
        url = f"{self.base_url}/search?search_terms={search_term}&geo_location_terms={location_formatted}"
        
        try:
            # Make request
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find business listings
            listings = soup.find_all('div', class_='result')
            
            for listing in listings[:30]:  # Limit to 30 results
                business = self._extract_business_info(listing, category)
                if business:
                    businesses.append(business)
            
            # If no results from scraping, return empty list (app will handle)
            if not businesses:
                print(f"No results found for {category} in {location}")
                
        except Exception as e:
            print(f"Error scraping Yellow Pages: {e}")
        
        return businesses
    
    def _extract_business_info(self, listing, category: str) -> Dict:
        try:
            business = {
                'name': '',
                'url': '',
                'display_phone': 'N/A',
                'location': {'display_address': []},
                'categories': [{'title': category.title()}],
                'rating': 'N/A',
                'review_count': 0
            }
            
            # Get business name
            name_elem = listing.find('a', class_='business-name')
            if name_elem:
                business['name'] = name_elem.get_text(strip=True)
            else:
                return None
            
            # Get phone number
            phone_elem = listing.find('div', class_='phones')
            if phone_elem:
                phone_text = phone_elem.get_text(strip=True)
                business['display_phone'] = phone_text
            
            # Get address
            address_elem = listing.find('div', class_='street-address')
            locality_elem = listing.find('div', class_='locality')
            
            address_parts = []
            if address_elem:
                address_parts.append(address_elem.get_text(strip=True))
            if locality_elem:
                address_parts.append(locality_elem.get_text(strip=True))
            
            if address_parts:
                business['location']['display_address'] = address_parts
            
            # Check for website
            links = listing.find_all('a', class_='track-visit-website')
            if links:
                for link in links:
                    href = link.get('href', '')
                    if href and 'yellowpages.com' not in href:
                        business['url'] = href
                        break
            
            # Get rating if available
            rating_elem = listing.find('div', class_='ratings')
            if rating_elem:
                rating_match = re.search(r'([\d.]+)', rating_elem.get('data-rating', ''))
                if rating_match:
                    business['rating'] = float(rating_match.group(1))
                
                # Get review count
                count_elem = rating_elem.find('span', class_='count')
                if count_elem:
                    count_text = count_elem.get_text(strip=True)
                    count_match = re.search(r'(\d+)', count_text)
                    if count_match:
                        business['review_count'] = int(count_match.group(1))
            
            return business
            
        except Exception as e:
            print(f"Error extracting business info: {e}")
            return None