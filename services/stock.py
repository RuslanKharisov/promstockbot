import json

import aiohttp
from typing import List, Dict, Any
from datetime import datetime


async def get_stocks_by_sku(sku: str, suppliers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []

    async with aiohttp.ClientSession() as session:
        for supplier in suppliers:
            print("supplier", supplier["name"])
            try:
                filters = {"sku": sku, "description": ""}
                filters_json = json.dumps(filters)
                url = f"{supplier['api']['url']}?token={supplier['api']['token']}&page=1&per_page=5&filters={filters_json} "

                async with session.get(url) as response:

                    json_data = await response.json()
                    for item in json_data.get("data", []):
                        results.append({
                            **item,
                            "supplier": supplier["name"],
                            "email": supplier["email"],
                            "siteUrl": supplier.get("siteUrl"),
                            "newDeliveryDate1": parse_date(item.get("newdelivery_date_1")),
                            "newDeliveryDate2": parse_date(item.get("newdelivery_date_2")),
                            "newDeliveryQty1": item.get("newdelivery_qty_1", 0),
                            "newDeliveryQty2": item.get("newdelivery_qty_2", 0),
                        })
            except Exception as e:
                print(f"Ошибка при запросе к {supplier['name']}: {e}")
    print("results", len(results))
    return results


def parse_date(value: str | None):
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except Exception:
        return datetime.now()
