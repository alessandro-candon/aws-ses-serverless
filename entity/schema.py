from pony.orm import Required, Database, Set, Optional, Json
from datetime import datetime

from configuration import App


def define_entities(database):
    class Destination(database.Entity):
        email = Required(str, unique=True)
        bounces = Set('Bounce')
        details = Set('Details')
        delivery = Set('Delivery')
        complaint = Set('Complaint')
        mail = Set('Mail')
        bounce_Undetermined = Optional(int)
        bounce_permanent_general = Optional(int)
        bounce_permanent_noEmail = Optional(int)
        bounce_permanent_suppressed = Optional(int)
        bounce_transient_general = Optional(int)
        bounce_transient_mail_box_full = Optional(int)
        bounce_transient_message_too_large = Optional(int)
        bounce_transient_content_rejected = Optional(int)
        bounce_transient_attachment_rejected = Optional(int)
        complaint_abuse = Optional(int)
        complaint_auth_failure = Optional(int)
        complaint_fraud = Optional(int)
        complaint_not_spam = Optional(int)
        complaint_other = Optional(int)
        complaint_virus = Optional(int)

    class Mail(database.Entity):
        destinations = Set(Destination)
        timestamp = Required(datetime)
        source = Optional(str)
        source_arn = Optional(str)
        source_ip = Optional(str)
        sending_account_id = Optional(str)
        message_id = Optional(str)
        headers_truncated = Optional(bool)
        headers = Optional(Json)

    class Bounce(database.Entity):
        destinations = Set(Destination)
        timestamp = Required(datetime)
        bounce_type = Optional(str)
        bounce_sub_type = Optional(str)
        feedback_id = Optional(str)
        reporting_mta = Optional(str)

    class Details(database.Entity):
        destinations = Set(Destination)
        timestamp = Required(datetime)
        source = Optional(str)
        source_arn = Optional(str)
        source_ip = Optional(str)
        sending_account_id = Optional(str)
        message_id = Optional(str)
        headers_truncated = Optional(str)
        destination = Optional(str)

    class Delivery(database.Entity):
        destinations = Set(Destination)
        timestamp = Required(datetime)
        processing_time_millis = Optional(int)
        smtp_response = Optional(str)
        reporting_mta = Optional(str)
        remote_mta_ip = Optional(str)

    class Complaint(database.Entity):
        destinations = Set(Destination)
        timestamp = Required(datetime)
        user_agent = Optional(str)
        complaint_feedback_type = Optional(str)
        arrival_date = Optional(str)
        feedback_id = Optional(str)


def define_database(env):
    db_params = App.get_db_configuration(env)
    db = Database(**db_params)
    define_entities(db)
    return db


def mapping_database(env):
    db_params = App.get_db_configuration(env)
    db = Database()
    db.bind(**db_params)
    define_entities(db)
    db.generate_mapping(create_tables=True)
