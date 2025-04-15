import os
from dotenv import load_dotenv

load_dotenv()  # Load the environment variables from the .env file

# Print the values of your API keys and tokens
print(f"API Key: {os.getenv('TWITTER_API_KEY')}")
print(f"API Secret Key: {os.getenv('TWITTER_API_SECRET_KEY')}")
print(f"Access Token: {os.getenv('TWITTER_ACCESS_TOKEN')}")
print(f"Access Token Secret: {os.getenv('TWITTER_ACCESS_TOKEN_SECRET')}")
print(f"Bearer Token: {os.getenv('TWITTER_BEARER_TOKEN')}")
