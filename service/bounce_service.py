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
            destination = destination_service.get_destination_or_create_if_not_exist(recipient['emailAddress'])
            self.save_relationship_with_destination(destination.id, mail.id, bounce.id)

    @db_session
    def generate_bounce_instance(self, bounce_r):
        bounce = self.database.Bounce(timestamp=AwsDatetime.convert_aws_timestamp(bounce_r['timestamp']))
        bounce.bounce_type = bounce_r['bounceType']
        bounce.bounce_sub_type = bounce_r.get('bounceSubType')
        bounce.feedback_id = bounce_r.get('feedbackId')
        bounce.reporting_mta = bounce_r.get('reportingMTA')
        return bounce

    @db_session
    def save_relationship_with_destination(self, destination_id: int, mail_id: int, bounce_id: int):
        destination = self.database.Destination[destination_id]
        mail = self.database.Mail[mail_id]
        destination.mails.add(mail)
        bounce = self.database.Bounce[bounce_id]
        destination.bounces.add(bounce)
