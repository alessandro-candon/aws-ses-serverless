from datetime import datetime


class AwsDatetime:
    @staticmethod
    def convert_aws_timestamp(timestamp_aws):
        return datetime.strptime(timestamp_aws, "%Y-%m-%dT%H:%M:%S.%fZ")
