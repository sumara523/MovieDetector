from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC00192dda66594328c17c3ea44ff4153b'
auth_token = '827119ae4c807c269e5f24b2c02cdd0e'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Thanks for joining MovieDetector",
                     from_='+18608524749',
                     to='+18605183270'
                 )

print(message.sid)