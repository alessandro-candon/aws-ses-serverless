from entity.schema import define_database
from service.datetime import AwsDatetime

COMPLAINT = 'Complaint'


class ComplaintService:
    @staticmethod
    def parse_and_save_complaint_instance(mail, complaint_r):
        pass