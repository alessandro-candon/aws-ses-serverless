from entity.schema import Mail, Complaint
from service.datetime import AwsDatetime
from service.destination_service import DestinationService

COMPLAINT = 'Complaint'


class ComplaintService:
    @staticmethod
    def parse_and_save_complaint_instance(mail: Mail, complaint_r):
        bounce = Complaint(timestamp=AwsDatetime.convert_aws_timestamp(complaint_r['timestamp']))
        # bounce.bounce_type = bounce_r['bounceType']
        # bounce.bounce_sub_type = bounce_r.get('bounceSubType')
        # bounce.feedback_id = bounce_r.get('feedbackId')
        # bounce.reporting_mta = bounce_r.get('reportingMTA')
        # for recipient in bounce_r['bouncedRecipients']:
        #     destination = DestinationService.get_destination_or_create_if_not_exist(recipient['emailAddress'])
        #     destination.mail = mail
        #     destination.bounces = bounce

    def add_destination_shortcut_data(self, subtype):
        pass
