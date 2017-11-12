import datetime
import json

from pony.orm import db_session

from service.bounce_service import BounceService
from service.request_service import AwsRequestService
from test.common_test_case import CommonTestCase


class AwsRequestServiceBounceTest(CommonTestCase):
    def test_save_request_bounce_to_db(self):
        json_response = '{"notificationType":"Bounce","bounce":{"bounceType":"Permanent","bounceSubType":"General",' \
                        '"bouncedRecipients":[{"emailAddress":"test2@hotmail.com","action":"failed","status":"5.5.0",' \
                        '"diagnosticCode":"smtp;550 Requested action not taken: mailbox unavailable (' \
                        '12354213:4278:-2147467259)"}],"timestamp":"2017-03-11T12:41:17.000Z",' \
                        '"feedbackId":"99999999999999-06c3c06c-0658-11e7-9dc3-2fc31251d7fd-000000",' \
                        '"reportingMTA":"dns;COL004-MC5F23.hotmail.com"},"mail":{' \
                        '"timestamp":"2017-03-11T12:41:12.000Z","source":"testep@test.com",' \
                        '"sourceArn":"arn:aws:ses:eu-west-1:292121581101:identity/test.com","sourceIp":"8.8.8.8",' \
                        '"sendingAccountId":"292121581101",' \
                        '"messageId":"0102015abd631fad-9d31386e-caba-4f09-8b68-4beae4d6769b-000000","destination":[' \
                        '"test2@hotmail.com"],"headersTruncated":false,"headers":[{"name":"Received","value":"from ' \
                        'testep.test.com ([8.8.8.8]) by email-smtp.amazonaws.com with SMTP (' \
                        'SimpleEmailService-1868680137) id mbXpJ9tgkRgJVr9L1G6n for test2@hotmail.com; Sat, ' \
                        '11 Mar 2017 12:41:14 +0000 (UTC)"},{"name":"Message-ID",' \
                        '"value":"<7b046a4f6905c16cf7273154694c15db@www.testep.test.com>"},{"name":"Date",' \
                        '"value":"Sat, 11 Mar 2017 13:41:12 +0100"},{"name":"Subject","value":"[testep] Modificación ' \
                        'de Planning"},{"name":"From","value":"Buzón test testep <testep@test.com>"},{"name":"To",' \
                        '"value":"test2@hotmail.com"},{"name":"MIME-Version","value":"1.0"},{"name":"Content-Type",' \
                        '"value":"text/html; charset=utf-8"},{"name":"Content-Transfer-Encoding",' \
                        '"value":"quoted-printable"}],"commonHeaders":{"from":["Buzón test testep ' \
                        '<testep@test.com>"],"date":"Sat, 11 Mar 2017 13:41:12 +0100","to":["test2@hotmail.com"],' \
                        '"messageId":"<7b046a4f6905c16cf7273154694c15db@www.testep.test.com>","subject":"[testep] ' \
                        'Modificación de Planning"}}}';
        AwsRequestService(json_response)
        with db_session:
            destinations = self.database.Destination.select()
            for destination in destinations:
                self.assertEqual(destination.email, 'test2@hotmail.com')

    def test_generate_bounce_instance(self):
        bounce_service = BounceService()
        bounce_r = json.loads(
            '{ "bounceType":"Permanent", "bounceSubType":"General", "bouncedRecipients":[ { '
            '"emailAddress":"test2@hotmail.com", "action":"failed", "status":"5.5.0", "diagnosticCode":"smtp;550 '
            'Requested action not taken: mailbox unavailable (12354213:4278:-2147467259)" } ], '
            '"timestamp":"2017-03-11T12:41:17.000Z", '
            '"feedbackId":"99999999999999-06c3c06c-0658-11e7-9dc3-2fc31251d7fd-000000", '
            '"reportingMTA":"dns;COL004-MC5F23.hotmail.com" }')
        bounce = bounce_service.generate_bounce_instance(bounce_r)

        self.assertEqual(bounce.bounce_type, 'Permanent')
        self.assertEqual(bounce.bounce_sub_type, 'General')
        self.assertEqual(bounce.feedback_id, '99999999999999-06c3c06c-0658-11e7-9dc3-2fc31251d7fd-000000')
        self.assertEqual(bounce.reporting_mta, 'dns;COL004-MC5F23.hotmail.com')

    def test_save_relationship_with_destination(self):
        with db_session:
            destination = self.database.Destination(email='test@test.com')
            mail = self.database.Mail(timestamp=datetime.datetime.now())
            bounce = self.database.Bounce(timestamp=datetime.datetime.now())

        bounce_service = BounceService()
        bounce_service.save_relationship_with_destination(destination.id, mail.id, bounce.id)

        with db_session:
            destinations = self.database.Destination.select(lambda d: d.email == 'test@test.com')
            for destination in destinations:
                for mail in destination.mails:
                    self.assertEqual(1, mail.id)
                for bounce in destination.bounces:
                    self.assertEqual(1, bounce.id)