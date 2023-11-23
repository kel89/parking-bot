import requests
import json
import os

def lambda_handler(event, context):
    # Your GraphQL API endpoint
    # api_url = "https://your-appsync-api-url/graphql"
    api_url = "https://delnlzxpzbebrlpigize73pqyq.appsync-api.us-east-1.amazonaws.com/graphql"

    # Your GraphQL query
    graphql_query = """
    query MyQuery {
        listToReserves {
            items {
            id
            reserveOn
            reserveTarget
            reserveTime
            resort
            user
            }
        }
    }
    """

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
        print("GraphQL Query Failed. Status Code:", response.status_code)
        print("Response:", response.text)

    # Your Lambda function logic goes here

    return {
        'statusCode': 200,
        'body': json.dumps('GraphQL query executed successfully!')
    }


lambda_handler(None, None)