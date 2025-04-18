import aiohttp
from typing import List, Dict


API_URL = "http://localhost:5000/apiserv/supplier/list"
# Если потребуется, можно заменить на локальный адрес, например:
# API_URL = "http://localhost:3000/api/supplier"

DEFAULT_PAYLOAD = {
    "page": 1,
    "perPage": 100,
    "filters": {
        "name": ""
    }
}


async def get_suppliers() -> List[Dict]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=DEFAULT_PAYLOAD) as response:
                if response.status != 201:
                    raise Exception(f"Ошибка получения поставщиков: {response.status}")
                json_data = await response.json()
                return json_data.get("data", [])
    except Exception as e:
        print(f"❌ Ошибка при получении поставщиков: {e}")
        return []

