import json
from appsync import get_credentials

from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
import datetime as dt

from BrightonParking import BrightonParking
from SolitudeParking import SolitudeParking


def lambda_handler(event, context):
    # Parse the triggering message
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # Extract the key info
    resort = message['resort']
    reserve_target = message['reserveTarget']
    reserve_target_date = dt.datetime.strptime( reserve_target, "%Y-%m-%d")
    user_id = message['user']
    
    # Get the passwords
    creds = get_credentials(user_id, resort)
    
    # Make the reservation------
    # startup chrome
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    chrome = webdriver.Chrome(options=options, service=service)


    # For testing locally, not in container, use this webdriver setup --------
    # options = webdriver.ChromeOptions()
    # options.add_argument("--window-size=1280,1696")
    # chrome = webdriver.Chrome(options=options)
    # ---------------------------------------------------------------------



    if resort == "SOLITUDE":
        sp = SolitudeParking(chrome, creds)
        sp.make_reservation(reserve_target_date)
    elif resort == "BRIGHTON":
        bp = BrightonParking(chrome, creds)
        bp.make_reservation(reserve_target_date)
    elif resort == "ALTA":
        pass
    else:
        pass

test_data = {
    "Records": [
        {
            'Sns': {
                'Message': """{
                    "resort": "SOLITUDE",
                    "reserveTarget": "2023-12-30",
                    "user": "e39fdf08-ee98-4c66-864a-90a6cf3543b1"

                }"""
            }
        }
    ]
}

if __name__ == "__main__":
    lambda_handler(test_data, None)
