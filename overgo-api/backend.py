from __future__ import annotations
import os
from datetime import date
from typing import List, Optional


import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


from providers import search_hotels_via_provider, BookingLink


app = FastAPI(title="Overgo MVP Backend", version="0.1.0")

class GuestCounts(BaseModel):
    adults: int = Field(ge=1, default=2)
    children: int = 0


class HotelQuery(BaseModel):
    city: str
    check_in: date
    check_out: date
    guests: GuestCounts = GuestCounts()
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    amenities: Optional[List[str]] = None # ["pool", "spa", "oceanfront", "wifi"]
    sort: Optional[str] = "recommended" # or "price", "distance"

class HotelCard(BaseModel):
    id: str
    name: str
    city: str
    rating: Optional[float] = None
    review_count: Optional[int] = None
    price_total: Optional[float] = None
    currency: Optional[str] = "USD"
    image_url: Optional[str] = None
    summary: Optional[str] = None
    booking: BookingLink


class SearchResponse(BaseModel):
    results: List[HotelCard]

@app.get("/health")
def health():
    return {"ok": True}


@app.post("/search", response_model=SearchResponse)
async def search_hotels(q: HotelQuery):
    try:
        results = await search_hotels_via_provider(q)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Minimal chat router (LLM stub) to extract intent -> HotelQuery.
# In Phase 1 we keep it simple; you can swap in an LLM later.
class ChatTurn(BaseModel):
    role: str
    content: str

class ChatToQueryRequest(BaseModel):
    history: List[ChatTurn]

@app.post("/chat-to-query", response_model=HotelQuery)
async def chat_to_query(req: ChatToQueryRequest):
# SUPER simple heuristic: look for patterns. Replace with an LLM function call later.
# Defaults: 2 adults, next Fri->Sun in city mentioned.
    import re
    from datetime import datetime, timedelta

    text = " ".join(t.content for t in req.history if t.role == "user")
    city_match = re.search(r"in\s+([A-Z][a-zA-Z\s]+)$|to\s+([A-Z][a-zA-Z\s]+)", text)
    city = (city_match.group(1) or city_match.group(2)).strip() if city_match else "Lagos"

    today = datetime.utcnow().date()
    days_until_fri = (4 - today.weekday()) % 7
    check_in = today + timedelta(days=days_until_fri or 7)
    check_out = check_in + timedelta(days=2)

    budget_match = re.search(r"under\s*(\d+)|max\s*(\d+)", text)
    budget_max = int(budget_match.group(1) or budget_match.group(2)) if budget_match else None
    
    return HotelQuery(city=city, check_in=check_in, check_out=check_out, guests=GuestCounts(), budget_max=budget_max)