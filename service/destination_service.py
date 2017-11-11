from pony.orm import db_session

from entity.schema import define_database


class DestinationService:
    @staticmethod
    @db_session
    def get_destination_or_create_if_not_exist(email_address):
        database = define_database()
        destination = database.Destination.get(email=email_address)
        if not destination:
            destination = database.Destination(email=email_address)
        return destination
