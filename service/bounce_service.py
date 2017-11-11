from pony.orm import db_session

from configuration import ENV
from entity.schema import define_database
from service.datetime import AwsDatetime
from service.destination_service import DestinationService

BOUNCE = 'Bounce'


class BounceService:

    def __init__(self):
        self.database = define_database(ENV)

    def parse_and_save_instance(self, mail, bounce_r):
        bounce = self.generate_bounce_instance(bounce_r)
        destination_service = DestinationService()
        for recipient in bounce_r['bouncedRecipients']:
            self.save_destination_data(destination_service, recipient, mail, bounce)

    @db_session
    def generate_bounce_instance(self, bounce_r):
        bounce = self.database.Bounce(timestamp=AwsDatetime.convert_aws_timestamp(bounce_r['timestamp']))
        bounce.bounce_type = bounce_r['bounceType']
        bounce.bounce_sub_type = bounce_r.get('bounceSubType')
        bounce.feedback_id = bounce_r.get('feedbackId')
        bounce.reporting_mta = bounce_r.get('reportingMTA')
        return bounce

    @db_session
    def save_destination_data(self, destination_service, recipient, mail, bounce):
        destination = destination_service.get_destination_or_create_if_not_exist(recipient['emailAddress'])
        # destination.mail.add(mail)
        destination.bounces.add(bounce)
    #
    # def add_destination_shortcut_data(self, subtype):
    #     pass
