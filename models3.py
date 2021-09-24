from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase

# db = SqliteDatabase('dns.db')


db = PostgresqlDatabase('dns_db', user='info_comp', password='123456', host='88.85.89.53', port=5432)


class BaseTable(Model):
    class Meta:
        database = db


class PriceParser(BaseTable):
    name = CharField()
    price_old = CharField()
    price_new = CharField()
    date_recording = DateField()
    display = CharField()


db.create_tables([PriceParser])
