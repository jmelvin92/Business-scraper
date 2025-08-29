import csv
import os
from typing import List, Dict
from datetime import datetime

class CSVExporter:
    def __init__(self):
        self.export_dir = 'exports'
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export(self, businesses: List[Dict]) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.export_dir, f'businesses_{timestamp}.csv')
        
        if not businesses:
            return None
        
        fieldnames = ['name', 'phone', 'address', 'categories', 'rating', 'review_count', 'has_website', 'website_url', 'lead_priority']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for business in businesses:
                has_website = business.get('has_website', True)
                writer.writerow({
                    'name': business.get('name', ''),
                    'phone': business.get('phone', ''),
                    'address': business.get('address', ''),
                    'categories': business.get('categories', ''),
                    'rating': business.get('rating', ''),
                    'review_count': business.get('review_count', 0),
                    'has_website': 'Yes' if has_website else 'No',
                    'website_url': business.get('website_url', ''),
                    'lead_priority': 'HIGH' if not has_website else 'LOW'
                })
        
        return filename