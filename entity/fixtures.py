from pony.orm import db_session

from entity.schema import define_entities


@db_session
def populate_db(database):
    destination = database.Destination(
        email='email@email.com'
    )
