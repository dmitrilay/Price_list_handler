from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase

db = SqliteDatabase('parser.db')


# db = PostgresqlDatabase('parser', user='info_comp', password='123456', host='88.85.89.53', port=5432)


class BaseTable(Model):
    class Meta:
        database = db


class Dns(BaseTable):
    name = CharField()
    price_old = CharField()
    price_new = CharField()
    date_recording = DateField()
    display = CharField()


class Mvm(BaseTable):
    name = CharField()
    price_old = CharField()
    price_new = CharField()
    date_recording = DateField()
    display = CharField()


class Eld(BaseTable):
    name = CharField()
    price_old = CharField()
    price_new = CharField()
    date_recording = DateField()
    display = CharField()


class Mts(BaseTable):
    name = CharField()
    price_old = CharField()
    price_new = CharField()
    date_recording = DateField()
    display = CharField()


db.create_tables([Dns, Mvm, Mts, Eld])
