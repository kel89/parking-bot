import smtplib
import sys

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}


class SMSHelper:
    def __init__(self, config):
        self.email = config.smsEmail
        self.password = config.smsEmailPassword
        self.alert_number = config.alertNumber
        self.alert_carrier = config.alertCarrier

    def send_message(self, message):
        recipient = self.alert_number + CARRIERS[self.alert_carrier]
        auth = (self.email, self.password)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(auth[0], auth[1])

        server.sendmail(auth[0], recipient, message)

    @staticmethod
    def is_valid_config(config):
        if (config.smsEmail and config.smsEmailPassword and config.alertNumber and config.alertCarrier):
            return True
        else:
            return False
