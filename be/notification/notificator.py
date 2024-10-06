import os
from twilio.rest import Client
from datetime import timedelta

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
ui_url = os.environ["UI_URL"]

# client = Client(account_sid, auth_token)

def notify_user_about_landsat(email, phone, hit, lead):
    pass
    # message = client.messages.create(
    #     body="LANDSAT will be passing over you in '{}' minutes".format(lead),
    #     messaging_service_sid="MG00f377b04816be8046507469725770f5",
    #     to=phone,
    #     send_at=hit - timedelta(lead),
    #     schedule_type="fixed",
    # )

    # Email integration TBD

def notify_user_about_data(email, phone, folder_name, lat, lon):
    pass
    # message = client.messages.create(
    #     body="LANDSAT data is available for you at '{}'/take/'{}'?lat='{}'&lon='{}'".format(ui_url, folder_name, lat, lon),
    #     messaging_service_sid="MG00f377b04816be8046507469725770f5",
    #     to=phone
    # )

    # Email integration TBD