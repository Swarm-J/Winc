import peewee
import datetime

db = peewee.SqliteDatabase("betsy.db")

# Models go here
class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    first_name = peewee.CharField(max_length=50)
    last_name = peewee.CharField(max_length=50)
    address = peewee.CharField()
    zipcode = peewee.CharField()
    city = peewee.CharField()
    email = peewee.CharField(max_length=50)
    username = peewee.CharField(unique=True, max_length=30)
    password = peewee.CharField(default="0000")
    cardnumber = peewee.IntegerField(default=1337)


class Product(BaseModel):
    name = peewee.CharField()
    description = peewee.CharField(max_length=200)
    price = peewee.DecimalField(constraints=[peewee.Check('price > 0')], decimal_places=2, auto_round=True)
    quantity = peewee.IntegerField(default=1)
    user = peewee.ForeignKeyField(User)


# db['Product'].create_index(['name'], unique=True)
Product.add_index(Product.name, Product.description)


class Tag(BaseModel):
    tagname = peewee.CharField(unique=True)


class Tag_Product(BaseModel):
    product = peewee.ForeignKeyField(Product)
    tag = peewee.ForeignKeyField(Tag)


class Transaction(BaseModel):
    buyer = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)
    buy_amount = peewee.IntegerField()
    buy_date = peewee.DateTimeField(formats="%Y-%m-%d %H:%M:%S", default=datetime.datetime.now)


def create_tables():
    with db:
        db.create_tables([User, Product, Tag, Tag_Product, Transaction])