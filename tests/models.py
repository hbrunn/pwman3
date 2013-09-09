from peewee import *
import peewee as pw

import pwman.util.config as config
filename = config.get_value('Database', 'filename')
# database = SqliteDatabase('test.pwman.db', **{})
database = SqliteDatabase(filename, **{})


class UnknownFieldType(object):
    pass


class BaseModel(pw.Model):
    class Meta:
        database = database


class Dbversion(BaseModel):
    dbversion = pw.TextField(db_column='DBVERSION', primary_key=True)

    class Meta:
        db_table = 'DBVERSION'


class Key(BaseModel):
    thekey = pw.TextField(db_column='THEKEY')

    class Meta:
        db_table = 'KEY'


class Lookup(BaseModel):
    node = pw.PrimaryKeyField(db_column='NODE')
    tag = pw.PrimaryKeyField(db_column='TAG')

    class Meta:
        db_table = 'LOOKUP'


class Nodes(BaseModel):
    data = pw.BlobField(db_column='DATA')
    id = pw.PrimaryKeyField(null=True, db_column='ID')

    class Meta:
        db_table = 'NODES'


class Tags(BaseModel):
    data = pw.BlobField(db_column='DATA')
    id = pw.PrimaryKeyField(null=True, db_column='ID')

    class Meta:
        db_table = 'TAGS'


class Sqlite_Sequence(BaseModel):
    name = UnknownFieldType()
    seq = UnknownFieldType()

    class Meta:
        db_table = 'sqlite_sequence'
