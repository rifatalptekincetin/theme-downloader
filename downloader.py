from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests,ssl,sys
ssl._create_default_https_context = ssl._create_unverified_context

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

def download(url, save_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('application/zip'):
            print(f"Not zip: {content_type}")
            return

        content_length = response.headers.get('Content-Length')
        if content_length is not None and int(content_length) == 0:
            print("Empty.")
            return

        first_chunk = next(response.iter_content(chunk_size=1024), b'')
        if not first_chunk.startswith(b'PK'):
            print("Not zip.")
            return

        with open(save_path, 'wb') as file:
            file.write(first_chunk)
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                
        print(f"Downloaded: {save_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sys.argv[1]
    text_to_search = '"{}"'.format(sys.argv[2])
    theme = sys.argv[1]
    browser = webdriver.Chrome()
    browser.get('https://www.google.com/search?q='+text_to_search)
    for _ in range(10):
        if "sorry" in browser.current_url:
            input("Rechaptca \a")
            
        links = browser.find_elements("css selector", '#rso a[href]:not([href*="google"])')

        for link in links:
            dom = "/".join(link.get_attribute("href").split("/")[:3])
            dom += "/wp-content/themes/"+theme+".zip"
            if download(dom,theme+".zip"):
                input("Downloaded \a")

        browser.find_element("css selector","#pnnext").click()
