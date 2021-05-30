# used to import environment variables
import os
from dotenv import load_dotenv
 
import smtplib # Simple Mail Transfer Protocol (Python module)
import ssl # module to access TLS (Transport Layer Security) --> makes transfer secure
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
 
import praw
 
load_dotenv(".env") # private environment variables are located in a local .env file

sender_email = os.environ.get('GMAIL_USER') # access email and password from .env file
password = os.environ.get('GMAIL_PASSWORD')
receiver_email = input("What email would you like your images sent to? ")
subreddit = input("What subreddit would you like images from? ")

subject = "Your Daily Reddit Images Are Here!" # title/subject of email
 
msg = MIMEMultipart()
msg["From"] = sender_email # set the sender's email
msg["To"] = receiver_email # set the receiver's email
msg["Subject"] = subject # set the subject
 
# Access reddit app using PRAW
reddit = praw.Reddit(
client_id=os.environ.get('CLIENT_ID'),
client_secret=os.environ.get('CLIENT_SECRET'),
user_agent="Image collector 1.0 by /u/AshleyHummel"
)

posts = 1
image_count = 0
email = "Hello! Your daily reddit images from r/" + subreddit + " are here!\n"
msg.attach(MIMEText(email, "plain"))
for submission in reddit.subreddit(subreddit).hot(limit=None):
  # state titles of top 5 "hot" posts and Redditors who posted them in email
  email = "\n" + str(posts) + ") " + submission.title + " by u/" + submission.author.name
  posts += 1
  msg.attach(MIMEText(email, "plain"))

  # save images to workspace file and TODO: Embed image in email
  if "jpg" in submission.url or "png" in submission.url:
    path = os.environ.get('PATH_NAME') # access path name from .env file
    # define image path and give it a name, which contains the subreddit and post ID
    output = open(path + f"{subreddit}-{submission.id}.png", "wb")
    output.write(requests.get(submission.url).content)
    output.close()
    image_count += 1
    if image_count > 5: # break loop when 5 images are found
      break

# use SMTP to access server and send email
def send_mail(sender_email, password, receiver_email, msg):
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# send email to user
send_mail(sender_email, password, receiver_email, msg)
print("Sent to " + receiver_email)