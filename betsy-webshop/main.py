from models import User, Product, Tag, Tag_Product, Transaction
import peewee
from spellchecker import SpellChecker

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

spell = SpellChecker()


def search(term):
    product_name = Product.name.contains(peewee.fn.LOWER(term))
    product_description = Product.description.contains(peewee.fn.LOWER(term))
    misspelled_word = spell.correction(term)
    misspelled_product_name = Product.name.contains(misspelled_word)
    misspelled_product_description = Product.description.contains(misspelled_word)
    query = Product.select().where(
        product_name |
        product_description |
        misspelled_product_name |
        misspelled_product_description,
        )    
    return [product.name for product in query]


def list_user_products(user_id):
    query = Product.select().join(User).where(Product.user == user_id).order_by(Product.name)
    return [product.name for product in query]


def list_products_per_tag(tag_id):
    query = Product.select().join(Tag_Product).join(Tag).where(Tag.tagname == tag_id).order_by(Product.name)
    return [product.name for product in query]


def add_product_to_catalog(user_id, product):
    new_product = Product.create(
        name=product['name'],
        description=product['description'],
        price=product['price'],
        quantity=product['quantity'],
        user=user_id,
        )
    return new_product


def update_stock(product_id, new_quantity):
    product = Product.get_by_id(product_id)
    product.quantity == new_quantity
    product.save()


def purchase_product(product_id, buyer_id, quantity):
    product = Product.get_by_id(product_id)
    
    bought_product = Transaction.create(
        buyer=buyer_id,
        product=product_id,
        buy_amount=quantity,
    )
    current_quantity = product.quantity
    update_stock(product_id=product_id, quantity=(current_quantity - quantity))
    return bought_product


def remove_product(product_id):
    product = Product.get_by_id(product_id)
    product.delete_instance()


def populate_test_database():
    # Create user
    User.create(
        first_name="Walter",
        last_name="White",
        address="308 Negra Arroya Lane",
        zipcode="87101",
        city="Albuquerque",
        email="heisenberg@email.com",
        username="Heisenberg",
        )
    # Create Products
    Product.create(
        name="Black Sunglasses",
        description="Sunglasses to make you look awesome",
        price=30.00,
        user=1,
        )
    Product.create(
        name="Black Hat",
        description="Stylish hat to give you slick look",
        price=25.00,
        user=1,
    )
    # Create Tags
    Tag.create(tagname="Hat")
    Tag.create(tagname="Glasses")
    # Create Product-Tags
    Tag_Product.create(
        product=1,
        tag=2,
        )
    Tag_Product.create(
        product=2,
        tag=1,
        )


if __name__ == "__main__":
    print(search("glasses"))    # without spelling mistake
    print(search("glsses")) # with spelling mistake
    print(list_user_products(1))
    print(list_products_per_tag('Glasses'))
