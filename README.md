The way I currently have the .env file setup locally I need
to run `source .env`.

This is probably fine, need to think about how I want to load
those into the lambda enviornment (AWS Secrets?)

to build container for AWS need this: `Building on an M mac, need to use the following to build: docker buildx build --platform linux/amd64 -t parking-notifier .`

# Polling script use

To reserve a spot:
1. Create a config JSON file (see [pollingConfig.py](pollingConfig.py) for an example file), containing login info, resort, and target date.
2. Run `python3 webdriverPoller.py  --config nameOfYourConfig.json`

This will open a browser, navigate to the target date, and reserve; if the date is not available, we will "refresh" (click on the next date and then back to the target date) until it is 

## Notes
- Only one date in the config file is supported at the time. To reserve multiple dates, current workaround is to have multiple scripts running
- Previous version of this script relied on calling API points directly in order to check availabiility. We can no longer do this since it seems Cloudflare's [I'm Under Attack Mode](https://blog.cloudflare.com/introducing-im-under-attack-mode) is being used to block non-browser traffic. [This commit](https://github.com/kel89/parking-bot/commit/effd1dbc60ef0e99422cd406d7eb29b8f05f679b) shows the latest status of the repo when API calling was being used. 

# Adding resorts

Add an enum class in [resorts.py](resorts.py) and update [pollingConfig.py](pollingConfig.py) to read a config file with that resort

# SMS Config
Using a free hack sending from a gmail account. Need to configure an "application password" to use
instructions can be found [here](https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637700239874464736-1954441174&rd=1)

Include the following in the config json:
```
{
    ...
    "alertNumber": "1234567890",
    "alertCarrier": "verizon", // see sms file for available carriers
    "smsEmail": "youemail@gmail.com",
    "smsEmailPassword": "yourApplicationPassword"
}
```