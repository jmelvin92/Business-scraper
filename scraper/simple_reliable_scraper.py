import random
from typing import List, Dict

class SimpleReliableScraper:
    def __init__(self):
        pass
    
    def search_businesses(self, location: str, radius: int = 5, category: str = 'barbershop') -> List[Dict]:
        """
        For now, return realistic mock data that will definitely work.
        This ensures the UI works while we can work on real scraping later.
        """
        
        # Get city from location
        city = location.split(',')[0].strip()
        
        # Category-specific business templates
        templates = {
            'barbershop': [
                'Classic Cuts', 'The Gentleman\'s Barber', 'Main Street Barbers', 
                'Executive Cuts', 'Old Town Barbershop', 'Modern Man Barber Co.',
                'Corner Barbershop', 'The Clipper Shop', 'Fresh Cuts', 'Uptown Barbers'
            ],
            'dentist': [
                'Bright Smile Dental', 'Family Dental Care', 'Downtown Dental Group',
                'Comfort Dental', 'Main Street Dentistry', 'Smile Center',
                'Premier Dental', 'City Dental Clinic', 'Perfect Smile Dentistry', 'Gentle Dental'
            ],
            'electrician': [
                'Lightning Electric', 'PowerPro Electricians', 'Spark Electric Co.',
                'Reliable Electric', '24/7 Electric Services', 'City Electric Solutions',
                'Express Electrical', 'Master Electricians', 'Bright Electric', 'Voltage Pros'
            ],
            'plumber': [
                'Quick Fix Plumbing', 'Drain Masters', 'Flow Pro Plumbers',
                'Emergency Plumbing', 'City Plumbing Co.', 'Pipe Dreams Plumbing',
                'Reliable Plumbers', '24 Hour Plumbing', 'Water Works Plumbing', 'Fix-It Plumbing'
            ],
            'handyman': [
                'Fix-It-All Services', 'Handy Helper', 'Mr. Fix It',
                'All Tasks Handyman', 'Home Repair Pros', 'Quick Fix Services',
                'Reliable Handyman', 'The Handyman Co.', 'Home Solutions', 'Fix & Go'
            ],
            'hvac': [
                'Cool Air HVAC', 'Climate Control Experts', 'City Heating & Cooling',
                'Comfort Zone HVAC', 'Air Masters', 'Temperature Pro',
                'All Seasons HVAC', 'Express HVAC', 'Climate Solutions', 'Air Comfort'
            ],
            'roofing': [
                'Top Roof Services', 'Reliable Roofing', 'City Roofers',
                'Premier Roofing', 'Storm Guard Roofing', 'Quality Roof Repair',
                'Express Roofing', 'Master Roofers', 'Summit Roofing', 'Apex Roofing'
            ],
            'landscaping': [
                'Green Thumb Landscaping', 'Beautiful Yards', 'City Landscaping',
                'Premier Lawn Care', 'Nature\'s Touch', 'Express Lawn Services',
                'Quality Landscaping', 'Green Valley', 'Bloom Landscaping', 'Yard Pros'
            ],
            'auto repair': [
                'Quick Fix Auto', 'City Auto Repair', 'Express Auto Service',
                'Main Street Auto', 'Reliable Auto Shop', 'Premier Auto Care',
                'Master Mechanics', 'Downtown Auto', 'Fast Lane Auto', 'Pro Auto Service'
            ]
        }
        
        # Get business names for the category
        business_names = templates.get(category.lower().replace(' ', ''), templates['handyman'])
        
        businesses = []
        
        # Generate realistic business data
        for i, name in enumerate(business_names):
            # Generate realistic phone numbers
            area_codes = ['555', '702', '415', '213', '619', '408']
            phone = f"({random.choice(area_codes)}) {random.randint(100,999)}-{random.randint(1000,9999)}"
            
            # Generate realistic addresses
            street_numbers = [100 + (i * 25), 250 + (i * 33), 500 + (i * 17)]
            street_names = ['Main St', 'Oak Ave', 'First St', 'Park Rd', 'Market St', 'Center Ave', 'Washington Blvd', 'Broadway', 'Pine St', 'Elm Ave']
            address = f"{random.choice(street_numbers)} {random.choice(street_names)}"
            
            # Realistic ratings and reviews
            rating = round(random.uniform(3.2, 4.8), 1)
            reviews = random.randint(15, 150)
            
            # 60% chance of NO website (these are the leads we want!)
            has_website = random.random() < 0.4  # 40% have websites, 60% don't
            
            business = {
                'name': f"{name} - {city}",
                'url': f'https://www.{name.lower().replace(" ", "").replace("\'", "")}.com' if has_website else '',
                'display_phone': phone,
                'location': {
                    'display_address': [address, location]
                },
                'categories': [{'title': category.title()}],
                'rating': rating,
                'review_count': reviews
            }
            
            businesses.append(business)
            
        # Shuffle to make it seem more realistic
        random.shuffle(businesses)
        
        print(f"Generated {len(businesses)} {category} businesses for {location}")
        
        return businesses[:8]  # Return 8 businesses for speed