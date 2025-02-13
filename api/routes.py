from fastapi import APIRouter, Depends
from models.settings import ScraperSettings
from api.auth import verify_token
from scraper.scraper import Scraper

router = APIRouter()

@router.post("/scrape")
async def scrape_endpoint(settings: ScraperSettings, auth: None = Depends(verify_token)):
    scraper = Scraper(pages=settings.pages, proxy=settings.proxy)
    result = scraper.run_scraping()
    return {"message": result}
