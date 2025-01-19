import requests 
from bs4 import BeautifulSoup
import os
import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
from typing import Dict, List
import time
from pathlib import Path

class CarScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.results = []
        
    def get_headers(self) -> Dict:
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }

    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> Dict:
        try:
            async with session.get(url, headers=self.get_headers()) as response:
                if response.status == 200:
                    html = await response.text()
                    return self.parse_car_details(html, url)
                return None
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def parse_car_details(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, 'html.parser')
        print(f"Processing {url}")
        # Extract article with attribute data-testid="result-list-container"
        article = soup.find('article', {'data-testid': 'result-list-container'})
        if not article:
            return None

        # Extract car details from elements with style="display:contents"
        article_divs = article.find_all('div', {'style': 'display:contents'})        
        if not article_divs:
            return None
        # print(f"Found {len(cars)} car details")
        
        # Extract all the divs with class="mN_WC ctcQH qEvrY" from article_divs
        car_divs = [div for div in article_divs if div.find('div', class_='mN_WC ctcQH qEvrY')]
        cars = []
        for car_div in car_divs:
            # print(car_div)
            # <span class="rqEvz FWtU1 YIC4W" data-testid="result-listing-1"><div class="fEytW"><div class="mZg1N"><div class="zwOmo mIdDf EwKGm" data-testid="listing-image-indicator"><span class="vy2gZ"><svg class="YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M4 5h16a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V7a2 2 0 012-2zm6 10l5-3-5-3v6z" fill="currentColor"></path></svg>Video</span><span class="jaBlJ"><svg class="YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path d="M14.5 8.75c.6904 0 1.25-.55964 1.25-1.25s-.5596-1.25-1.25-1.25-1.25.55964-1.25 1.25.5596 1.25 1.25 1.25Z" fill="currentColor"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M2 5c0-1.65685 1.34315-3 3-3h14c1.6569 0 3 1.34315 3 3v14c0 1.6569-1.3431 3-3 3H5c-1.65685 0-3-1.3431-3-3V5Zm3-1c-.55228 0-1 .44772-1 1v8.4091l3.62328-3.95267c.4431-.48339 1.22373-.41664 1.57833.13496l2.55719 3.97781c.6561 1.0207 2.0627 1.2267 2.9839.437l1.0542-.9035c.3967-.3401.9884-.3174 1.3579.0521L20 16V5c0-.55228-.4477-1-1-1H5Z" fill="currentColor"></path></svg>30</span></div><img alt="BMW Z8 5.0 1. Hand*Zustand 1-*Lückenlos BMW*Sammler" class="Qj_9F" data-testid="result-listing-image-1" loading="eager" sizes="218px" src="https://img.classistatic.de/api/v1/mo-prod/images/c4/c491a73f-582f-464f-ae65-9e5be77e6b72?rule=mo-160.jpg" srcset="https://img.classistatic.de/api/v1/mo-prod/images/c4/c491a73f-582f-464f-ae65-9e5be77e6b72?rule=mo-160.jpg 160w, https://img.classistatic.de/api/v1/mo-prod/images/c4/c491a73f-582f-464f-ae65-9e5be77e6b72?rule=mo-240.jpg 240w, https://img.classistatic.de/api/v1/mo-prod/images/c4/c491a73f-582f-464f-ae65-9e5be77e6b72?rule=mo-360.jpg 360w, https://img.classistatic.de/api/v1/mo-prod/images/c4/c491a73f-582f-464f-ae65-9e5be77e6b72?rule=mo-1024.jpg 1024w" style="width: 218px; height: calc(163.5px);"></div></div><div class="K0qQI"><div class="EflMX"><span class="Q7YSy i7yXy ymhAF Q7YSy" data-testid="sponsored-badge">Gesponsert</span><h2 class="QeGRL">BMW Z8 5.0 1. Hand*Zustand 1-*Lückenlos BMW*Sammler</h2></div><div class="fqe3L" data-testid="online-since">Inserat online seit 17.12.2024, 22:09</div><section data-testid="listing-details"><div class="HaBLt" data-testid="listing-details-attributes"><div class=""><strong>Unfallfrei</strong> • EZ 03/2001 • 48.696&nbsp;km • 294&nbsp;kW&nbsp;(400&nbsp;PS) • Benzin</div></div></section></div><div class="V7THI"><div class=""><div class="" data-testid="main-price-label"><div><span class="fpviJ" data-testid="price-label">239.000&nbsp;€</span></div></div><div><span class="FWtU1 drxl5" data-testid="srp-financing-link" tabindex="0">Finanzierung berechnen</span></div><div class="_rpAd jsOU1 GS9hc"><div class="dyWge"><span></span><span></span><span></span><span></span><span></span></div><div class="_u77E bzOeV">Ohne Bewertung</div></div></div></div><div class="RrMyL"><section class="_t8yX HaBLt"><span class="y2ZHx" data-testid="highlights-item"><svg class="XK6GY YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M9 15.879l-5-5L1.879 13 9 20.121 23.121 6 21 3.879l-12 12z" fill="currentColor"></path></svg> Inzahlungnahme möglich</span><span class="y2ZHx" data-testid="highlights-item"><svg class="XK6GY YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M9 15.879l-5-5L1.879 13 9 20.121 23.121 6 21 3.879l-12 12z" fill="currentColor"></path></svg> Finanzierung möglich</span><span class="y2ZHx" data-testid="highlights-item"><svg class="XK6GY YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M9 15.879l-5-5L1.879 13 9 20.121 23.121 6 21 3.879l-12 12z" fill="currentColor"></path></svg> Weltweite Lieferung</span></section><div class="FPpvB" data-testid="seller-info"><div><div class="v8YU8"><span class="HX987 rjHf7 Ssf9m">CZ-Fahrzeugforum GbR</span><span class="c7aHU"><div class="zRvpd"><span class="CaPWA"><svg class="NDlcw YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17Z" fill="#FFD500"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17ZM12 15.1498L15.9391 17.4218L14.9956 12.9733L18.3736 9.92907L13.8513 9.45177L12 5.29834L10.1486 9.45177L5.62629 9.92907L9.00433 12.9733L8.06081 17.4218L12 15.1498Z" fill="#EBBC00"></path></svg><svg class="NDlcw YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17Z" fill="#FFD500"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17ZM12 15.1498L15.9391 17.4218L14.9956 12.9733L18.3736 9.92907L13.8513 9.45177L12 5.29834L10.1486 9.45177L5.62629 9.92907L9.00433 12.9733L8.06081 17.4218L12 15.1498Z" fill="#EBBC00"></path></svg><svg class="NDlcw YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17Z" fill="#FFD500"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17ZM12 15.1498L15.9391 17.4218L14.9956 12.9733L18.3736 9.92907L13.8513 9.45177L12 5.29834L10.1486 9.45177L5.62629 9.92907L9.00433 12.9733L8.06081 17.4218L12 15.1498Z" fill="#EBBC00"></path></svg><svg class="NDlcw YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17Z" fill="#FFD500"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17ZM12 15.1498L15.9391 17.4218L14.9956 12.9733L18.3736 9.92907L13.8513 9.45177L12 5.29834L10.1486 9.45177L5.62629 9.92907L9.00433 12.9733L8.06081 17.4218L12 15.1498Z" fill="#EBBC00"></path></svg><svg class="NDlcw YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1L15.0388 7.81738L22.4616 8.60081L16.9169 13.5976L18.4656 20.8992L12 17.17Z" fill="currentColor"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M12 1V17.17L5.53431 20.8992L7.08299 13.5976L1.53833 8.60081L8.9611 7.81738L12 1Z" fill="#FFD500"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M12 17.17V1L8.9611 7.81738L1.53833 8.60081L7.08299 13.5976L5.53431 20.8992L12 17.17ZM10.1486 9.45178L10.5 8.66346V16.0149L8.06086 17.4218L9.00438 12.9733L5.62634 9.92908L10.1486 9.45178Z" fill="#EBBC00"></path></svg></span></div><span class="W9v_K">(31)</span></span></div>22547 Hamburg</div></div></div><div class="WRg3T"><div><span class="FWtU1 eW4Ht" data-testid="srp-insurance-link" tabindex="0">Versicherung vergleichen</span></div><div class="Ngy6o WK8AX" data-testid="listing-action-buttons"><button class="FxqoS H2Y6F p7tM_" data-testid="listing-action-email" type="button"><span class="H68e7 TXrbf" tabindex="-1"><svg class="nQao3 hcDLf YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M2 8l10 6 10-6v10a1 1 0 01-1 1H3a1 1 0 01-1-1V8zm0-3a1 1 0 011-1h18a1 1 0 011 1v1l-10 6L2 6V5z" fill="currentColor"></path></svg><span class="fJrrk" tabindex="-1">Kontakt</span></span></button><button class="FxqoS cq2eI p7tM_" data-testid="listing-action-parking-park" aria-label="Parken" type="button"><span class="H68e7 TXrbf" tabindex="-1"><svg class="nQao3 hcDLf YgmFC" width="16" height="16" viewBox="0 0 24 24" focusable="false" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M5 1h14a1 1 0 011 1v20.191a.5.5 0 01-.724.447L12 19l-7.276 3.638A.5.5 0 014 22.191V2a1 1 0 011-1zm4 4v10h2v-3h2c3 0 3-2 3-3.5S16 5 13 5H9zm2 2h2c1 0 1 1 1 1.5s0 1.5-1 1.5h-2V7z" fill="currentColor"></path></svg><span class="fJrrk" tabindex="-1">Parken</span></span></button></div></div></span>
            car = {}
            car['title'] = self.safe_extract(car_div, 'h2', {'class': 'QeGRL'})
            car['price'] = self.safe_extract(car_div, 'span', {'class': 'fpviJ'})
            car['attributes'] = self.safe_extract(car_div, 'div', {'class': ''})

            cars.append(car)
        return cars


    def safe_extract(self, soup: BeautifulSoup, tag: str, attrs: Dict) -> str:
        element = soup.find(tag, attrs)
        return element.text.strip() if element else None

    async def scrape_cars(self, urls: List[str]):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_page(session, url) for url in urls]
            results = await asyncio.gather(*tasks)
            self.results.extend([r for r in results if r])

    def save_results(self, filename: str = 'car_data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

    def append_results(self, filename: str = 'car_data.json'):
        
        # Create file if it doesn't exist
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Read existing data
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
        
        # Append new results
        existing_data.extend(self.results)

        # Write back all data
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        # Clear current results after saving
        self.results = []

def read_urls(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

async def main():
    urls = read_urls('carspec_links.txt')
    scraper = CarScraper()
    
    # Split URLs into batches to avoid overwhelming the server
    batch_size = 10
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        await scraper.scrape_cars(batch)
        print(f"Processed {i + len(batch)}/{len(urls)} URLs")
        scraper.append_results()  # Append after each batch
        time.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())