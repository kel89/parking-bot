import requests
import json
import os


def get_credentials(user_id, resort):
    api_url = "https://delnlzxpzbebrlpigize73pqyq.appsync-api.us-east-1.amazonaws.com/graphql"

    graphql_query = """
    query MyQuery {
        listCredentials(filter: {user: {eq: "%s"}, resort: {eq: %s}}) {
            items {
            password
            username
            }
        }
    }
    """ % (user_id, resort)
    print(graphql_query)
    # return
    # AWS AppSync requires a specific header for authorization
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.environ['appsync_api_key']  # Replace with your API key or other authentication headers
    }

    # Make the GraphQL request
    response = requests.post(api_url, headers=headers, data=json.dumps({"query": graphql_query}))

    # Check for success
    if response.status_code == 200:
        result = response.json()
        # Process the result as needed
        print("GraphQL Query Result:", result)
    else:
        # hope we don't get here because I'm not going to handle it
        print("GraphQL Query Failed. Status Code:", response.status_code)
        print("Response:", response.text)

    # Parse out the items and we just want the first
    items = result.get('data', {}).get('listCredentials', {}).get('items', [])
    return items[0]