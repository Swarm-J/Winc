import models
import peewee
from typing import List


__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def cheapest_dish() -> models.Dish:
    """You want to get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    cheapest_dish = models.Dish.select().order_by(models.Dish.price_in_cents).first()
    return cheapest_dish


def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """
    vegetarian_dishes = []
    for dish in models.Dish.select(): 
        if all(ingredient.is_vegetarian for ingredient in dish.ingredients):
                vegetarian_dishes.append(dish)
    return vegetarian_dishes


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """
    highest_rated_restaurant = models.Restaurant.select().join(models.Rating).where(peewee.fn.MAX(models.Rating.rating))
    return highest_rated_restaurant


def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating

    Select the first restaurant in the dataset and add a rating
    """
    first_restaurant = models.Restaurant.select().first()
    models.Rating.create(restaurant=first_restaurant, rating=5, comment="Very Tasty Food")


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    new_dish_name = "The Daily Special"
    new_dished_served = "Franky's Corner"
    new_dish_price = 1000
    ingredients_new_dish = "cheese", "pasta", "salmon", "onions"
    # check if dish is in db
    new_dish = models.Dish.get_or_create(name=new_dish_name,
                                         defaults={
                                         'served_at': new_dished_served,
                                         'price_in_cents': new_dish_price,
                                         'ingredients': ingredients_new_dish})

    # check if ingredients are in db
    for ingredient in ingredients_new_dish:
        models.Ingredient.get_or_create(name=ingredient, defaults={'is_vegetarian': True, 'is_vegan': False, 'is_glutenfree': True})
    
    return new_dish


if __name__ == "__main__":
    # print(cheapest_dish())
    print(vegetarian_dishes())
    # print(best_average_rating())
    # print(dinner_date_possible())
    # print(add_dish_to_menu())