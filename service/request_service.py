import json
from pony.orm import db_session

from entity.schema import define_database
from service.bounce_service import BounceService, BOUNCE
from service.complaint_service import COMPLAINT, ComplaintService
from service.delivery_service import DELIVERY, DeliveryService
from service.datetime import AwsDatetime


@db_session
class AwsRequestService:

    response_notification_type = {
        BOUNCE: BounceService.parse_and_save_bounce_instance,
        COMPLAINT: ComplaintService.parse_and_save_complaint_instance,
        DELIVERY: DeliveryService.parse_and_save_delivery_instance,
    }

    def __init__(self, json_response):
        self.database = define_database()
        self.response = json.loads(json_response)
        self.mail = self.create_mail_instance(self.response['mail'])
        print(self.response['notificationType'])
        self.response_notification_type[self.response['notificationType']](
            self.mail, self.response[self.response['notificationType'].lower()]
        )

    def create_mail_instance(self, mail_r):
        mail = self.database.Mail(timestamp=AwsDatetime.convert_aws_timestamp(mail_r['timestamp']))
        mail.source = mail_r.get('source', '')
        mail.source_arn = mail_r.get('sourceArn', '')
        mail.source_ip = mail_r.get('sourceIp', '')
        mail.sending_account_id = mail_r.get('sendingAccountId', '')
        mail.message_id = mail_r.get('messageId', '')
        mail.headers_truncated = mail_r.get('headersTruncated', '')
        mail.headers = mail_r.get('headers', '')
        return mail
