# scraper/scraper.py
import time
import requests
from bs4 import BeautifulSoup
from config import BASE_URL, DEFAULT_RETRIES, RETRY_DELAY
from models.product import Product
from scraper.storage import Storage
from scraper.cache import Cache
from scraper.notifier import Notifier
from typing import Optional
from fake_useragent import UserAgent

class Scraper:
    def __init__(self, pages: Optional[int] = None, proxy: Optional[str] = None):
        """
        :param pages: Optional; limit the number of pages to scrape.
        :param proxy: Optional; proxy string to use (e.g., "http://proxy:port").
        """
        self.pages = pages
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.storage = Storage()
        self.cache = Cache()
        self.notifier = Notifier()
        self.total_scraped = 0
        self.total_updated = 0

    def get_page(self, url: str) -> Optional[str]:
        attempts = 0
        headers = {
            'User-Agent': UserAgent().random,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.google.com'
        }
        while attempts < DEFAULT_RETRIES:
            try:
                response = requests.get(url, proxies=self.proxy, headers=headers, timeout=10)
                if response.status_code == 200:
                    return response.text
                else:
                    print(f"Error: Received status code {response.status_code} for URL: {url}")
            except requests.RequestException as e:
                print(f"Request error: {e} for URL: {url}")
            attempts += 1
            time.sleep(RETRY_DELAY)
        print(f"Failed to fetch URL: {url} after {DEFAULT_RETRIES} attempts.")
        return None

    def parse_products(self, html: str) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        # Adjust the selectors below based on the actual website structure
        # product_elements = soup.find_all('div', class_='product')
        product_elements = soup.find_all('li', class_='product')
        products = []
        for elem in product_elements:
            try:
                title_elem = elem.find('h2', class_='woo-loop-product__title')
                price_elem = elem.find('span', class_='woocommerce-Price-amount')
                image_elem = elem.find('img')
                if title_elem and price_elem and image_elem:
                    product_title = title_elem.get_text(strip=True)
                    # Remove currency symbols and commas
                    price_text = price_elem.get_text(strip=True).replace('$', '').replace('₹', '').replace(',', '')
                    product_price = float(price_text)
                    image_src = image_elem.get('src')
                    # Download the image locally
                    local_image_path = self.download_image(image_src, product_title)
                    product = Product(
                        product_title=product_title,
                        product_price=product_price,
                        path_to_image=local_image_path
                    )
                    products.append(product)
            except Exception as e:
                print(f"Error parsing product element: {e}")
        return products

    def download_image(self, image_url: str, product_title: str) -> str:
        """
        Downloads the image from the URL and saves it locally.
        Returns the local file path.
        """
        try:
            response = requests.get(image_url, proxies=self.proxy, stream=True, timeout=10)
            if response.status_code == 200:
                # Create a safe file name from product title
                filename = "".join([c if c.isalnum() else "_" for c in product_title]) + ".jpg"
                filepath = f"images/{filename}"
                # Ensure the images directory exists
                import os
                os.makedirs("images", exist_ok=True)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return filepath
            else:
                print(f"Failed to download image: {image_url}")
        except Exception as e:
            print(f"Exception downloading image: {e}")
        # Fallback: return the original image URL if download fails
        return image_url

    def run_scraping(self) -> str:
        page_number = 1
        while True:
            if self.pages and page_number > self.pages:
                break
            # Construct URL: first page is BASE_URL; subsequent pages have "page/{page_number}/"
            url = BASE_URL if page_number == 1 else f"{BASE_URL}page/{page_number}/"
            print(f"Scraping URL: {url}")
            html = self.get_page(url)
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(html)
            if not html:
                # Stop if the page cannot be fetched after retries
                break
            products = self.parse_products(html)
            if not products:
                print("No products found on page. Ending scraping.")
                break
            for product in products:
                self.total_scraped += 1
                # Check the cache: if the product price is unchanged, skip updating
                cached_price = self.cache.get(product.product_title)
                if cached_price is None or cached_price != product.product_price:
                    updated = self.storage.update_product(product)
                    if updated:
                        self.total_updated += 1
                    self.cache.set(product.product_title, product.product_price)
            page_number += 1
        self.notifier.notify(self.total_scraped, self.total_updated)
        print("Cache contents:", self.cache.dump())
        return f"Scraping completed. Total products scraped: {self.total_scraped}. Updated: {self.total_updated}"
