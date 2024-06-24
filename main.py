from dotenv import load_dotenv
from instagrapi import Client
import time
import random
# Load environment variables from the .env file
load_dotenv()
import os
import MySQLdb

# Connect to the database
connection = MySQLdb.connect(
  host=os.getenv("DATABASE_HOST"),
  user=os.getenv("DATABASE_USERNAME"),
  passwd=os.getenv("DATABASE_PASSWORD"),
  db=os.getenv("DATABASE"),
  autocommit=True,
  ssl_mode="VERIFY_IDENTITY",
  ssl={ "ca": "/etc/ssl/certs/ca-certificates.crt" }
)


# Create a cursor to interact with the database
cursor = connection.cursor()

# Execute "SHOW TABLES" query
cursor.execute("SELECT * FROM followersAndBios WHERE bio LIKE '';")

# Fetch all the rows
users = cursor.fetchall()

def put_bio_in_db(username: str, a: Client):
    bio = get_bio(username, a)
    if not bio:
        bio = "NOT_DEFINED"
    q = f"UPDATE followersAndBios SET bio='{bio}' WHERE username='{username}';"
    cursor.execute(q)

def get_bio(username: str, a: Client):
    response = a.user_info_by_username(username).dict()
    return response['biography']

def env_login() -> Client:
    api = Client()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    settings_path = f'settings/{username}.json'
    if os.path.isfile(settings_path):
        api.load_settings(settings_path)
    api.login(username, password)
    api.dump_settings(settings_path)
    return api  

# Print out the tables
print("Tables in the database:")
id = int(os.getenv("ID"))
api = env_login()


for user in users:
    index = user[0]
    username = user[1]
    if index%22 ==  id:
        put_bio_in_db(username, api)
        print(user, index)
        time.sleep(random.uniform(30, 45))
        

cursor.close()
connection.close()
