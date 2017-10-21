import json
from datetime import datetime

from pony.orm import db_session

from entity.schema import Mail, Bounce, Destination
from service.bounce_service import BounceService, BOUNCE


@db_session
class AwsRequestService:
    def __init__(self, json_response):
        self.response = json.loads(json_response)
        self.mail = self.create_mail_instance(self.response['mail'])
        if self.response['notificationType'] == BOUNCE:
            BounceService.parse_and_save_bounce_instance(self.response['bounce'])

    def create_mail_instance(self, mail_r):
        mail = Mail(timestamp=self.convert_aws_timestamp(mail_r['timestamp']))
        mail.source = mail_r.get('source', '')
        mail.source_arn = mail_r.get('sourceArn', '')
        mail.source_ip = mail_r.get('sourceIp', '')
        mail.sending_account_id = mail_r.get('sendingAccountId', '')
        mail.message_id = mail_r.get('messageId', '')
        mail.headers_truncated = mail_r.get('headersTruncated', '')
        mail.headers = mail_r.get('headers', '')
        return mail
