from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List, Optional


from pydantic import BaseModel

@dataclass
class BookingLink:
    label: str
    url: str
    white_label: bool = False

class HotelQuery(BaseModel):
    city: str
    check_in: str
    check_out: str
    guests: dict
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    amenities: Optional[list] = None
    sort: Optional[str] = None


# ----- Mock + Affiliate (Phase 1) -----
async def _affiliate_link(city: str, check_in: str, check_out: str, adults: int) -> BookingLink:
    base = os.getenv("AFFILIATE_BASE", "https://www.booking.com")
    # For demo, deep-link to a city search. Replace with co-brand/white-label base when approved.
    # Booking.com supports query params like: dest_type=city; checkin, checkout, group_adults, etc.
    url = (
    f"{base}/searchresults.html?ss={city}&checkin={check_in}&checkout={check_out}"
    f"&group_adults={adults}&no_rooms=1&group_children=0"
    )
    return BookingLink(label="Book on Booking.com", url=url, white_label=True)

async def _mock_inventory(city: str) -> List[dict]:
    demo = [
        {
            "id": "demo1",
            "name": "Overgo Collection – Marina View",
            "city": city,
            "rating": 9.2,
            "review_count": 1240,
            "price_total": 320.0,
            "currency": "USD",
            "image_url": "https://images.unsplash.com/photo-1502920917128-1aa500764b8a",
            "summary": "Design-forward boutique with spa & rooftop pool.",
        },
        {
            "id": "demo2",
            "name": "Maison du Parc",
            "city": city,
            "rating": 8.9,
            "review_count": 860,
            "price_total": 240.0,
            "currency": "USD",
            "image_url": "https://images.unsplash.com/photo-1551776235-dde6d4829808",
            "summary": "Quiet luxury near city gardens; perfect for couples.",
        },
    ]
    return demo


async def search_hotels_via_provider(q) -> List[dict]:
    provider = os.getenv("PROVIDER", "affiliate").lower()

    if provider in ("mock", "affiliate"):
        items = await _mock_inventory(q.city)
        book = await _affiliate_link(q.city, str(q.check_in), str(q.check_out), q.guests.adults)
        results = []
        for it in items:
            results.append({
                **it,
                "booking": {"label": book.label, "url": book.url, "white_label": book.white_label},
            })
        return results

    if provider == "hotelbeds":
        # Minimal stub (Phase 2): you will need real keys + signature
        # Signature = SHA256(API_KEY + SECRET + timestamp)
        # See: https://developer.hotelbeds.com/documentation/getting-started/
        raise NotImplementedError("Integrate Hotelbeds shopping/booking once partner keys are available.")

    raise ValueError(f"Unknown provider: {provider}")





