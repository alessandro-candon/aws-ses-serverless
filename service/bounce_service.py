from service.datetime import AwsDatetime
from service.destination_service import DestinationService

BOUNCE = 'Bounce'


class BounceService:
    @staticmethod
    def parse_and_save_bounce_instance(mail, bounce_r, database):
        bounce = database.Bounce(timestamp=AwsDatetime.convert_aws_timestamp(bounce_r['timestamp']))
        bounce.bounce_type = bounce_r['bounceType']
        bounce.bounce_sub_type = bounce_r.get('bounceSubType')
        bounce.feedback_id = bounce_r.get('feedbackId')
        bounce.reporting_mta = bounce_r.get('reportingMTA')
        for recipient in bounce_r['bouncedRecipients']:
            destination = DestinationService.get_destination_or_create_if_not_exist(recipient['emailAddress'])
            destination.mail = mail
            destination.bounces = bounce

    def add_destination_shortcut_data(self, subtype):
        pass
