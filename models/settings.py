from pydantic import BaseModel, Field
from typing import Optional

class ScraperSettings(BaseModel):
    pages: Optional[int] = Field(default=None, description="Limit the number of pages to scrape")
    proxy: Optional[str] = Field(default=None, description="Proxy URL to use for requests")
