The way I currently have the .env file setup locally I need
to run `source .env`.

This is probably fine, need to think about how I want to load
those into the lambda enviornment (AWS Secrets?)

to build container for AWS need this: `Building on an M mac, need to use the following to build: docker buildx build --platform linux/amd64 -t parking-notifier .`
