# scraper/storage.py
import json
import os
from models.product import Product
from typing import List
from config import JSON_DB_FILE

class Storage:
    def __init__(self, db_file: str = JSON_DB_FILE):
        self.db_file = db_file
        # Ensure the storage file exists; create the directory if necessary.
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def load_data(self) -> List[dict]:
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def save_data(self, products: List[dict]):
        with open(self.db_file, 'w') as f:
            json.dump(products, f, indent=4)

    def update_product(self, product: Product) -> bool:
        """
        Update the product in storage. If the product exists and the price is the same,
        do not update. Returns True if updated or if it is a new product; False otherwise.
        """
        data = self.load_data()
        updated = False
        found = False
        for idx, item in enumerate(data):
            if item['product_title'] == product.product_title:
                found = True
                if item['product_price'] != product.product_price:
                    data[idx] = product.dict()
                    updated = True
                break
        if not found:
            data.append(product.dict())
            updated = True
        self.save_data(data)
        return updated
