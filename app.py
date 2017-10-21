from chalice import Chalice
from pony.orm import db_session

app = Chalice(app_name='aws-ses-api')
app.debug = True


@app.route('/aws/ses/response', methods=['POST'])
@db_session
def save_aws_notification():
    return "hola"