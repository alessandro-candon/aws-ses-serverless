from pony.orm import db_session

from entity.schema import Destination


class DestinationService:
    @staticmethod
    @db_session
    def get_destination_or_create_if_not_exist(email_address):
        destination = Destination.get(email=email_address)
        if not destination:
            destination = Destination(email=email_address)
        return destination
