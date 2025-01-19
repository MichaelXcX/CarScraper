import requests
from bs4 import BeautifulSoup
from lxml import etree

# https://www.mobile.de/robots.txt

robots_url = 'https://www.mobile.de/robots.txt'

def get_sitemap():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(robots_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract the sitemap URL from txt file
    for line in soup.text.split('\n'):
        if 'Sitemap' in line:
            sitemap = line.split(': ')[1]
            print(f"Found sitemap: {sitemap}")
            break
    return sitemap

# Function to parse the XML file
def get_links(url):
    try:
        # Trick the server into thinking I am a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html'
        }
        response = requests.get(url, headers=headers)

        print(f"Response status: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type', '')}")
        # print(f"Content: {response.text[:500]}...")  # Print first 500 chars  
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            return []
            
        # Register namespaces if needed
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        root = etree.fromstring(response.content)
        # links = root.xpath('//ns:url/ns:loc/text()', namespaces=namespaces) NOT WORKING
        links = [element.text for element in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        print(f"Found {len(links)} links")
        # print(links)
        return links
    except Exception as e:
        print(f"Error processing sitemap: {str(e)}")
        print(f"Response content: {response.text[:500]}...")  # Print first 500 chars
        return []

if __name__ == '__main__':
    sitemap = get_sitemap()
    carspec_xmls = get_links(sitemap)

    carspec_urls = []
    for carspec_xml in carspec_xmls:
        # Exclude the urls that include region
        if 'region' in carspec_xml or 'auto' in carspec_xml or 'magazin' in carspec_xml:
            continue
        carspec_urls.extend(get_links(carspec_xml))
    print(f"Found {len(carspec_urls)} car specification links")

    # Save the links to a file
    with open('carspec_links.txt', 'w') as f:
        for link in carspec_urls:
            f.write(f"{link + '?lang=en'}\n")