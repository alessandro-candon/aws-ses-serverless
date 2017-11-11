from pony.orm import db_session

from configuration import ENV
from entity.schema import define_database


class DestinationService:

    def __init__(self):
        self.database = define_database(ENV)

    @db_session
    def get_destination_or_create_if_not_exist(self, email_address):
        destination = self.database.Destination.get(email=email_address)
        if not destination:
            destination = self.database.Destination(email=email_address)
        self.database.commit()
        return destination
