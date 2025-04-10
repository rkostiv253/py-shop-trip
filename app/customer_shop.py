from dataclasses import dataclass
from typing import Dict


@dataclass
class CustomerShop:
    name: str
    money: int
    product_cart: dict
    price_of_products: Dict[str, Dict[str, float]]
    total_price: Dict[str, float]
    fuel_sum: Dict[str, float]
    total_trip_cost: Dict[str, float]
