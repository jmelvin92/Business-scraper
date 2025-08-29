import time
import re
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class GoogleMapsSearcher:
    def __init__(self):
        self.driver = None
        
    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(3)
    
    def _close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def search_businesses(self, location: str, radius: int = 5, category: str = 'barbershop') -> List[Dict]:
        businesses = []
        
        try:
            self._setup_driver()
            
            # Build search query
            search_query = f"{category} near {location}"
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            self.driver.get(url)
            time.sleep(3)
            
            # Wait for results to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[role="article"]'))
                )
            except TimeoutException:
                print("No results found or timeout")
                return businesses
            
            # Scroll to load more results
            results_panel = self.driver.find_element(By.CSS_SELECTOR, '[role="feed"]')
            for _ in range(3):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
                time.sleep(2)
            
            # Get all business cards
            business_elements = self.driver.find_elements(By.CSS_SELECTOR, '[role="article"]')
            
            for element in business_elements[:50]:  # Limit to 50 results
                try:
                    business_data = self._extract_business_info(element)
                    if business_data:
                        businesses.append(business_data)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error during search: {e}")
        finally:
            self._close_driver()
            
        return businesses
    
    def _extract_business_info(self, element) -> Dict:
        try:
            # Get business name
            name = element.find_element(By.CSS_SELECTOR, '.fontHeadlineSmall').text
            
            # Initialize data
            business_data = {
                'name': name,
                'url': '',
                'display_phone': 'N/A',
                'location': {'display_address': []},
                'categories': [],
                'rating': 'N/A',
                'review_count': 0
            }
            
            # Try to get address
            try:
                info_spans = element.find_elements(By.CSS_SELECTOR, '.W4Efsd span')
                for span in info_spans:
                    text = span.text
                    # Check for phone number pattern
                    if re.match(r'[\(\)\d\s\-\+]+', text) and len(text) > 7:
                        business_data['display_phone'] = text
                    # Check for address (contains numbers and letters)
                    elif any(char.isdigit() for char in text) and any(char.isalpha() for char in text):
                        business_data['location']['display_address'] = [text]
                    # Category detection
                    elif '·' in text:
                        parts = text.split('·')
                        if len(parts) > 1:
                            business_data['categories'] = [{'title': parts[1].strip()}]
            except:
                pass
            
            # Try to get rating
            try:
                rating_element = element.find_element(By.CSS_SELECTOR, '.MW4etd')
                business_data['rating'] = float(rating_element.text)
            except:
                pass
            
            # Try to get review count
            try:
                review_element = element.find_element(By.CSS_SELECTOR, '.UY7F9')
                review_text = review_element.text
                if '(' in review_text and ')' in review_text:
                    count = review_text.split('(')[1].split(')')[0].replace(',', '')
                    business_data['review_count'] = int(count)
            except:
                pass
            
            # Try to detect if has website
            try:
                # Click on the business to get more details
                element.click()
                time.sleep(1)
                
                # Look for website button/link
                website_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-value="Website"], [aria-label*="Website"], a[href*="url?q="]')
                for web_elem in website_elements:
                    href = web_elem.get_attribute('href')
                    if href and 'google.com' not in href and 'maps' not in href:
                        business_data['url'] = href
                        break
            except:
                pass
                
            return business_data
            
        except Exception as e:
            return None