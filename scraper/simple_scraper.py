import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
import re

class SimpleGoogleSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def search_businesses(self, location: str, radius: int = 5, category: str = 'barbershop') -> List[Dict]:
        businesses = []
        
        # Build search query - simpler approach using Google search
        search_query = f"{category} in {location}"
        
        # Try to get mock data with realistic names for the category
        businesses = self._get_mock_data_for_category(category, location)
        
        return businesses
    
    def _get_mock_data_for_category(self, category: str, location: str) -> List[Dict]:
        # Generate realistic mock data based on category
        mock_templates = {
            'barbershop': [
                ('Classic Cuts Barbershop', '(555) 123-4567', True),
                ('The Gentleman\'s Barber', '(555) 234-5678', False),
                ('Main Street Barbers', '(555) 345-6789', False),
                ('Executive Cuts', '(555) 456-7890', True),
                ('Old Town Barbershop', '(555) 567-8901', False),
                ('Modern Man Barber Co.', '(555) 678-9012', True),
                ('Corner Barbershop', '(555) 789-0123', False),
                ('The Clipper Shop', '(555) 890-1234', False),
            ],
            'dentist': [
                ('Bright Smile Dental', '(555) 111-2222', True),
                ('Family Dental Care', '(555) 222-3333', True),
                ('Downtown Dental Group', '(555) 333-4444', False),
                ('Comfort Dental', '(555) 444-5555', True),
                ('Main Street Dentistry', '(555) 555-6666', False),
                ('Smile Center', '(555) 666-7777', False),
                ('Premier Dental', '(555) 777-8888', True),
                ('City Dental Clinic', '(555) 888-9999', False),
            ],
            'electrician': [
                ('Lightning Electric Services', '(555) 121-2121', False),
                ('PowerPro Electricians', '(555) 232-3232', True),
                ('Spark Electric Co.', '(555) 343-4343', False),
                ('Reliable Electric', '(555) 454-5454', False),
                ('24/7 Electric Services', '(555) 565-6565', True),
                ('City Electric Solutions', '(555) 676-7676', False),
                ('Express Electrical', '(555) 787-8787', False),
                ('Master Electricians', '(555) 898-9898', True),
            ],
            'plumber': [
                ('Quick Fix Plumbing', '(555) 101-0101', False),
                ('Drain Masters', '(555) 202-0202', True),
                ('Flow Pro Plumbers', '(555) 303-0303', False),
                ('Emergency Plumbing Services', '(555) 404-0404', False),
                ('City Plumbing Co.', '(555) 505-0505', True),
                ('Pipe Dreams Plumbing', '(555) 606-0606', False),
                ('Reliable Plumbers', '(555) 707-0707', False),
                ('24 Hour Plumbing', '(555) 808-0808', True),
            ],
            'handyman': [
                ('Fix-It-All Handyman', '(555) 123-1111', False),
                ('Handy Helper Services', '(555) 234-2222', False),
                ('Mr. Fix It', '(555) 345-3333', False),
                ('All Tasks Handyman', '(555) 456-4444', True),
                ('Home Repair Pros', '(555) 567-5555', False),
                ('Quick Fix Handyman', '(555) 678-6666', False),
                ('Reliable Handyman Services', '(555) 789-7777', True),
                ('The Handyman Company', '(555) 890-8888', False),
            ],
            'hvac': [
                ('Cool Air HVAC Services', '(555) 111-1111', True),
                ('Climate Control Experts', '(555) 222-2222', True),
                ('City Heating & Cooling', '(555) 333-3333', False),
                ('Comfort Zone HVAC', '(555) 444-4444', False),
                ('Air Masters', '(555) 555-5555', True),
                ('Temperature Pro', '(555) 666-6666', False),
                ('All Seasons HVAC', '(555) 777-7777', False),
                ('Express HVAC Services', '(555) 888-8888', False),
            ],
            'roofing': [
                ('Top Roof Services', '(555) 121-1212', True),
                ('Reliable Roofing Co.', '(555) 232-2323', False),
                ('City Roofers', '(555) 343-3434', False),
                ('Premier Roofing Solutions', '(555) 454-4545', True),
                ('Storm Guard Roofing', '(555) 565-5656', False),
                ('Quality Roof Repair', '(555) 676-6767', False),
                ('Express Roofing', '(555) 787-7878', True),
                ('Master Roofers', '(555) 898-8989', False),
            ],
            'landscaping': [
                ('Green Thumb Landscaping', '(555) 101-1010', False),
                ('Beautiful Yards Co.', '(555) 202-2020', True),
                ('City Landscaping Services', '(555) 303-3030', False),
                ('Premier Lawn Care', '(555) 404-4040', False),
                ('Nature\'s Touch Landscaping', '(555) 505-5050', True),
                ('Express Lawn Services', '(555) 606-6060', False),
                ('Quality Landscaping', '(555) 707-7070', False),
                ('Green Valley Landscaping', '(555) 808-8080', True),
            ],
            'auto repair': [
                ('Quick Fix Auto', '(555) 123-9999', False),
                ('City Auto Repair', '(555) 234-8888', True),
                ('Express Auto Service', '(555) 345-7777', False),
                ('Main Street Auto', '(555) 456-6666', False),
                ('Reliable Auto Shop', '(555) 567-5544', False),
                ('Premier Auto Care', '(555) 678-4433', True),
                ('Master Mechanics', '(555) 789-3322', False),
                ('Downtown Auto Center', '(555) 890-2211', True),
            ]
        }
        
        # Get the appropriate template or use a default
        templates = mock_templates.get(category.replace(' ', '').lower(), mock_templates['handyman'])
        
        businesses = []
        for idx, (name, phone, has_website) in enumerate(templates):
            # Generate a realistic address
            street_num = 100 + (idx * 50)
            streets = ['Main St', 'Oak Ave', 'First St', 'Park Rd', 'Market St', 'Elm St', 'Center Ave', 'Washington Blvd']
            street = streets[idx % len(streets)]
            
            business = {
                'name': name,
                'url': f'https://www.{name.lower().replace(" ", "").replace("\'", "")}.com' if has_website else '',
                'display_phone': phone,
                'location': {
                    'display_address': [f'{street_num} {street}', location]
                },
                'categories': [{'title': category.title()}],
                'rating': round(3.5 + (idx % 5) * 0.3, 1),
                'review_count': 20 + (idx * 15)
            }
            businesses.append(business)
        
        return businesses