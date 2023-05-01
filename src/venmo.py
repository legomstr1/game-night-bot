from venmo_api import Client
import config

# Get your access token. You will need to complete the 2FA process
access_token = Client.get_access_token(username = config.venmo_email,
                                       password = config.venmo_password)
print("My token:", access_token)

venmo = Client(access_token = access_token)

venmo.payment.request_money(0.01, "test request", "disker")