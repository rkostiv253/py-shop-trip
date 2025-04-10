import json

from app.car import Car
from app.customer import Customer
from app.customer_shop import CustomerShop
from app.shop import Shop
from app.Calculate_modules.calculate_distance import calculate_distance
from decimal import Decimal
from datetime import datetime


def shop_trip() -> None:
    with open("config.json", "r") as file:
        dict1 = json.load(file)

    customers = []
    for customer in dict1["customers"]:
        customer["car"] = Car(**customer["car"])
        customers.append(Customer(**customer))

    shops = [Shop(**shop) for shop in dict1["shops"]]

    fuel_price = dict1["FUEL_PRICE"]

    result = []

    for customer in customers:
        price_of_products = {
            shop.name: {
                item: Decimal(customer.product_cart.get(item, 0))
                * Decimal(shop.products.get(item, 0))
                for item in customer.product_cart
            }
            for shop in shops
        }

        total_price = {
            shop.name: sum(
                Decimal(customer.product_cart.get(item, 0))
                * Decimal(shop.products.get(item, 0))
                for item in customer.product_cart
            )
            for shop in shops
        }

        fuel_dict1 = {}
        for shop in shops:
            distance = calculate_distance(customer.location,
                                          shop.location)

            fuel_used = (Decimal(distance)
                         * Decimal(customer.car.fuel_consumption / 100))
            fuel_cost = (Decimal(fuel_used)
                         * Decimal(fuel_price))
            fuel_dict1[shop.name] = float(round(fuel_cost, 2)) * 2

        total_trip_cost = {
            shop_name: Decimal(total_price[shop_name])
            + Decimal(fuel_dict1[shop_name])
            for shop_name in total_price
        }

        result.append({
            "name": customer.name,
            "money": customer.money,
            "product_cart": customer.product_cart,
            "price_of_products": price_of_products,
            "total_price": total_price,
            "fuel_sum": fuel_dict1,
            "total_trip_cost": total_trip_cost
        })

    customers_shops = [CustomerShop(**r) for r in result]

    for cm in customers_shops:
        print(f"\n{cm.name} has {cm.money} dollars")
        cheapest_shop = min(cm.total_trip_cost, key=cm.total_trip_cost.get)
        cheapest_cost = cm.total_trip_cost[cheapest_shop]
        for key, value in cm.total_trip_cost.items():
            print(f"{cm.name}'s trip to the {key} "
                  f"costs {round(float(value), 2)}")
        if cheapest_cost < cm.money:
            print(f"{cm.name} rides to {cheapest_shop}")
            print(f"\nDate: {datetime.now().replace(microsecond=0)}")
            print(f"Thanks, {cm.name}, for your purchase!")
            print("You have bought: ")
            for shop_name, products in cm.price_of_products.items():
                if shop_name == cheapest_shop:
                    for prod, price in products.items():
                        for prod2, number in cm.product_cart.items():
                            if prod == prod2:
                                print(f"{number} {prod2}(s) for "
                                      f"{round(float(price), 2)}")
            for key, value in cm.total_price.items():
                if key == cheapest_shop:
                    print(f"Total cost is {round(float(value), 2)} dollars")
            print("See you again!")
            print(f"\n{cm.name} rides home")
            print(f"{cm.name} now has "
                  f"{round((float(cm.money) - float(cheapest_cost)), 2)}"
                  f"dollars")
        else:
            print(f"{cm.name} doesn't have enough money "
                  f"to make a purchase in any shop")


print(shop_trip())
