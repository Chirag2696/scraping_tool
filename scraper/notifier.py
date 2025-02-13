class Notifier:
    def notify(self, total: int, updated: int):
        message = f"Scraping completed. Total products scraped: {total}. Updated in DB: {updated}."
        print(message)
