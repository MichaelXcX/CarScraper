from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


import random
import time
from typing import Optional
import os
import json

class SeleniumScraper:
    def __init__(self):
        self.driver = None
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        ]
        self.links = self.get_car_links()
        
    # Initialize the browser
    def init_browser(self):
        try:
            options = Options()
            options.binary_location = './chrome-win64/chrome-win64/chrome.exe'
            options.add_argument('--enable-unsafe-swiftshader')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument(f'user-agent={random.choice(self.user_agents)}')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            
            # # Execute CDP commands for stealth
            # self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            #     "userAgent": random.choice(self.user_agents)
            # })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return self.driver
            
        except Exception as e:
            print(f"Error initializing browser: {e}")
            return None

    # Close the browser
    def close(self):
        if self.driver:
            self.driver.quit()

    # Accept cookies
    def accept_cookies(self):
        try:
            # Wait up to 10 seconds for button to be clickable
            consent_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mde-consent-accept-btn"))
            )
            consent_button.click()
            print("Cookie consent accepted")
            return True
        except TimeoutException:
            print("Cookie consent button not found")
            return False

    # Get the links from carspec_links.txt
    def get_car_links(self):
        links = []
        with open('carspec_links.txt', 'r') as f:
            links = f.readlines()
        return links

    # Collect car elements from a page
    def collect_cars(self, url):
        try:
            self.current_url = url
            self.driver.get(url)
            time.sleep(2)
            print(f"Loading page: {url}")

            self.accept_cookies()
            return self.get_car_elements()
        except Exception as e:
            print(f"Error scraping page: {e}")
        return []

    def get_car_elements(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".mN_WC.ctcQH.qEvrY"))
            )
            return self.driver.find_elements(By.CSS_SELECTOR, ".mN_WC.ctcQH.qEvrY")
        except Exception as e:
            print(f"Error getting elements: {e}")
            return []

    # Collect info from car page after click
    def scrape_car(self, index):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Refresh elements list
                elements = self.get_car_elements()
                if index >= len(elements):
                    print(f"Index {index} out of range")
                    return None
                    
                # Click element
                elements[index].click()
                time.sleep(4)
                self.driver.switch_to.window(self.driver.window_handles[1])
                
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".XY6XP.FWtU1.drxl5"))
                )
                
                ### Extracting car tehnical data ###
                show_more_btns = self.driver.find_elements(By.CSS_SELECTOR, ".XY6XP.FWtU1.drxl5")
                show_more_btn = show_more_btns[0] if show_more_btns else None

                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", show_more_btn)
                time.sleep(1)
                
                # Try JavaScript click
                self.driver.execute_script("arguments[0].click();", show_more_btn)
                time.sleep(1)
                # <dl class="XCaEv"><dt class="NcUki epo9w nI7AA" data-testid="damageCondition-item">Vehicle condition<span class="aVYhD" data-testid="damageCondition"><button aria-label="Info" type="button" class="MefuX gsbIM"><svg class="YgmFC rQe2M d8LC4" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.5 12.005C1.5 6.201 6.199 1.5 12 1.5s10.5 4.701 10.5 10.505C22.5 17.812 17.801 22.5 12 22.5S1.5 17.812 1.5 12.005zM11.975 9c.864 0 1.5-.686 1.5-1.475C13.475 6.661 12.839 6 12 6a1.53 1.53 0 00-1.525 1.525c0 .789.711 1.475 1.5 1.475zM15 18v-1c-1.311-.161-1.5-.276-1.5-1.702V10.5l-4 .5v1c1.15.184 1 .519 1 1.876v1.422c0 1.449-.758 1.541-2 1.702v1H15z" fill="currentColor"></path></svg></button></span></dt><dd class="nI7AA">Used vehicle, Accident-free</dd><dt class="NcUki epo9w nI7AA" data-testid="category-item">Category</dt><dd class="nI7AA">Small Car, Demonstration Vehicle</dd><dt class="NcUki epo9w nI7AA" data-testid="sku-item">Vehicle Number</dt><dd class="nI7AA">70810888</dd><dt class="NcUki epo9w nI7AA" data-testid="availability-item">Availability</dt><dd class="nI7AA">Now</dd><dt class="NcUki epo9w nI7AA" data-testid="countryVersion-item">Origin</dt><dd class="nI7AA">German edition</dd><dt class="NcUki epo9w nI7AA" data-testid="mileage-item">Mileage</dt><dd class="nI7AA">3,900&nbsp;km</dd><dt class="NcUki epo9w nI7AA" data-testid="power-item">Power</dt><dd class="nI7AA">80&nbsp;kW&nbsp;(109&nbsp;hp)</dd><dt class="NcUki epo9w nI7AA" data-testid="envkv.engineType-item">Drive type</dt><dd class="nI7AA">Electric motor</dd><dt class="NcUki epo9w nI7AA" data-testid="envkv.otherEnergySource-item">Other energy source</dt><dd class="nI7AA">Electricity</dd><dt class="NcUki epo9w nI7AA" data-testid="battery-item">Battery</dt><dd class="nI7AA">included</dd><dt class="NcUki epo9w nI7AA" data-testid="batteryCapacity-item">Battery capacity (in kWh)</dt><dd class="nI7AA">52&nbsp;kWh</dd><dt class="NcUki epo9w nI7AA" data-testid="plugTypes-item">Plug types</dt><dd class="nI7AA">Type 2 plug</dd><dt class="NcUki epo9w nI7AA" data-testid="envkv.energyConsumption-item">Energy consumption (comb.)<sup>2</sup></dt><dd class="nI7AA">19.4 kWh/100km</dd><dt class="NcUki epo9w nI7AA" data-testid="envkv.co2Emissions-item">CO₂ emissions (comb.)<sup>2</sup><span class="aVYhD" data-testid="envkv.co2Emissions"><button aria-label="Info" type="button" class="MefuX gsbIM"><svg class="YgmFC rQe2M d8LC4" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.5 12.005C1.5 6.201 6.199 1.5 12 1.5s10.5 4.701 10.5 10.505C22.5 17.812 17.801 22.5 12 22.5S1.5 17.812 1.5 12.005zM11.975 9c.864 0 1.5-.686 1.5-1.475C13.475 6.661 12.839 6 12 6a1.53 1.53 0 00-1.525 1.525c0 .789.711 1.475 1.5 1.475zM15 18v-1c-1.311-.161-1.5-.276-1.5-1.702V10.5l-4 .5v1c1.15.184 1 .519 1 1.876v1.422c0 1.449-.758 1.541-2 1.702v1H15z" fill="currentColor"></path></svg></button></span></dt><dd class="nI7AA">0&nbsp;g/km</dd><dt class="NcUki epo9w nI7AA" data-testid="envkv.co2Class-item">CO₂ class</dt><dd class="nI7AA"><div>Based on CO₂ emissions (combined)</div><img alt="" class="ouvhd" data-testid="envkv.co2Class-image" src="https://img.classistatic.de/api/v1/mo-prod/images/co2class-A?rule=mo-1024.jpg"></dd><dt class="NcUki epo9w nI7AA" data-testid="envkv.consumptionDetails.power-item">Power consumption<sup>2</sup></dt><dd class="nI7AA"><div class="Js08r">19.4 kWh/100km (combined)</div></dd><dt class="NcUki epo9w nI7AA" data-testid="numSeats-item">Number of Seats</dt><dd class="nI7AA">5</dd><dt class="NcUki epo9w nI7AA" data-testid="doorCount-item">Door Count</dt><dd class="nI7AA">4/5</dd><dt class="NcUki epo9w nI7AA" data-testid="transmission-item">Transmission</dt><dd class="nI7AA">Automatic</dd><dt class="NcUki epo9w nI7AA" data-testid="emissionClass-item">Emission Class<div class="VdRnH" data-testid="emissionClass"><button aria-label="Info" type="button" class="MefuX gsbIM"><svg class="YgmFC rQe2M d8LC4" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.5 12.005C1.5 6.201 6.199 1.5 12 1.5s10.5 4.701 10.5 10.505C22.5 17.812 17.801 22.5 12 22.5S1.5 17.812 1.5 12.005zM11.975 9c.864 0 1.5-.686 1.5-1.475C13.475 6.661 12.839 6 12 6a1.53 1.53 0 00-1.525 1.525c0 .789.711 1.475 1.5 1.475zM15 18v-1c-1.311-.161-1.5-.276-1.5-1.702V10.5l-4 .5v1c1.15.184 1 .519 1 1.876v1.422c0 1.449-.758 1.541-2 1.702v1H15z" fill="currentColor"></path></svg></button></div></dt><dd class="nI7AA">Euro6d</dd><dt class="NcUki epo9w nI7AA" data-testid="emissionsSticker-item">Emissions Sticker<div class="VdRnH" data-testid="emissionsSticker"><button aria-label="Info" type="button" class="MefuX gsbIM"><svg class="YgmFC rQe2M d8LC4" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.5 12.005C1.5 6.201 6.199 1.5 12 1.5s10.5 4.701 10.5 10.505C22.5 17.812 17.801 22.5 12 22.5S1.5 17.812 1.5 12.005zM11.975 9c.864 0 1.5-.686 1.5-1.475C13.475 6.661 12.839 6 12 6a1.53 1.53 0 00-1.525 1.525c0 .789.711 1.475 1.5 1.475zM15 18v-1c-1.311-.161-1.5-.276-1.5-1.702V10.5l-4 .5v1c1.15.184 1 .519 1 1.876v1.422c0 1.449-.758 1.541-2 1.702v1H15z" fill="currentColor"></path></svg></button></div></dt><dd class="nI7AA">4 (Green)</dd><dt class="NcUki epo9w nI7AA" data-testid="firstRegistration-item">First Registration</dt><dd class="nI7AA">04/2024</dd><dt class="NcUki epo9w nI7AA" data-testid="numberOfPreviousOwners-item">Number of Vehicle Owners</dt><dd class="nI7AA">1</dd><dt class="NcUki epo9w nI7AA" data-testid="hu-item">HU</dt><dd class="nI7AA">04/2027</dd><dt class="NcUki epo9w nI7AA" data-testid="climatisation-item">Climatisation</dt><dd class="nI7AA">Automatic air conditioning</dd><dt class="NcUki epo9w nI7AA" data-testid="parkAssists-item">Parking sensors</dt><dd class="nI7AA">Rear</dd><dt class="NcUki epo9w nI7AA" data-testid="airbag-item">Airbags</dt><dd class="nI7AA">Front and Side and More Airbags</dd><dt class="NcUki epo9w nI7AA" data-testid="manufacturerColorName-item">Colour (Manufacturer)</dt><dd class="nI7AA">FEUERROT</dd><dt class="NcUki epo9w nI7AA" data-testid="color-item">Colour</dt><dd class="nI7AA">Red Metallic</dd><dt class="NcUki epo9w nI7AA" data-testid="interior-item">Interior Design</dt><dd class="nI7AA">Cloth, Grey</dd></dl>

                technical_data_first_col = self.driver.find_elements(By.CSS_SELECTOR, ".NcUki.epo9w.nI7AA")
                technical_data_second_col = self.driver.find_elements(By.CSS_SELECTOR, ".nI7AA")
                technical_data_second_col = technical_data_second_col[1::2]

                technical_data = {}
                for i in range(len(technical_data_first_col)):
                    key = technical_data_first_col[i].text
                    value = technical_data_second_col[i].text
                    technical_data[key] = value
                print(f"Technical data: {technical_data}")
                ### Extracting car features ###
                show_more_btn = show_more_btns[1] if show_more_btns else None

                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", show_more_btn)
                time.sleep(1)
                
                # Try JavaScript click
                self.driver.execute_script("arguments[0].click();", show_more_btn)
                time.sleep(1)
                # Process car details here
                features = self.driver.find_elements(By.CSS_SELECTOR, ".FtSYW")
                features = [feature.text for feature in features]
                print(f"Features: {features}")

                # Car name 
                car_name = self.driver.find_elements(By.CSS_SELECTOR, ".dNpqi")[1]
                
                # Car type 
                car_type = self.driver.find_element(By.CSS_SELECTOR, ".GOIOV.fqe3L.EevEz").get_attribute('innerHTML')

                #Car price
                car_price = self.driver.find_element(By.CSS_SELECTOR, ".zgAoK.jjvdJ.dNpqi")

                car_details = {
                    'car': car_name.text + ' ' + car_type,
                    'car_price': car_price.text,
                    'technical_data': technical_data,
                    'features': features
                }
                self.save_car_data(car_details)

                time.sleep(1)

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.get(self.current_url)
                time.sleep(1)

                return True
                
            except StaleElementReferenceException:
                if attempt == max_attempts - 1:
                    print(f"Failed to process car {index} after {max_attempts} attempts")
                    return None
                print(f"Retrying car {index}")
                time.sleep(2)
                continue
            except Exception as e:
                print(f"Error processing car {index}: {e}")
                return None
            
    def save_car_data(self, car_data):
        filename = 'cars_data.json'
        try:
            # Load existing data if file exists
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []
            
            # Append new car data
            existing_data.append({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'url': self.driver.current_url,
                'details': car_data
            })
            
            # Save back to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
                
            print(f"Saved car data to {filename}")
            
        except Exception as e:
            print(f"Error saving car data: {e}")

def main(): 

    scraper = SeleniumScraper()
    results = []

    try:
        driver = scraper.init_browser()
        if not driver:
            print("Error initializing browser")
            return
        
        for link in scraper.links:
            # curr_link = scraper.links[0]
            car_elements = scraper.collect_cars(link)
            print(f"Found {len(car_elements)} cars")

            # Process each car
            for index in range(len(car_elements)):
                try:
                    car_data = scraper.scrape_car(index)
                    if car_data:
                        results.append(car_data)
                    time.sleep(2)
                except Exception as e:
                    print(f"Error processing car {index}: {e}")
                    continue

    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        # Cleanup
        scraper.close()
        print(f"Processed {len(results)} cars")


if __name__ == "__main__":
    main()