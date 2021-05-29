import os # used to import environment variables
from dotenv import load_dotenv
 
import smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs
 
import praw
 
load_dotenv()
 
port = 465  # standard port
smtp_server = "smtp.gmail.com"
email = os.environ.get('GMAIL_USER')
password = os.environ.get('GMAIL_PASSWORD')
sender_email = os.environ.get('GMAIL_USER')
receiver_email = input("What email would you like your images sent to?") # TODO: use a list here to send to multiple addresses
subject = "TEST MESSAGE" # title of email
 
# initialize message being sent
msg = MIMEMultipart("alternative")
msg["From"] = sender_email # set the sender's email
msg["To"] = receiver_email # set the receiver's email
msg["Subject"] = subject # set the subject
 
# set the body of the email as HTML
html = """
This email is sent using <b>Python </b>!
"""
 
html_part1 = MIMEText(html, 'html')
# attach the email body to the mail message
# attach the plain text version first
msg.attach(html_part1)
 
def send_mail(email, password, sender_email, receiver_email, msg):
   # initialize the SMTP server
   server = smtplib.SMTP("smtp.gmail.com", 587)
   # connect to the SMTP server as TLS mode (secure) and send EHLO
   server.starttls()
   # login to the account using the credentials
   server.login(email, password)
   # send the email
   server.sendmail(sender_email, receiver_email, msg.as_string())
   # terminate the SMTP session
   server.quit()
 
send_mail(email, password, sender_email, receiver_email, msg)
 
# Access top 5 "hot" subreddit posts using Reddit app
reddit = praw.Reddit(
client_id=os.environ.get('CLIENT_ID'),
client_secret=os.environ.get('CLIENT_SECRET'),
user_agent='Image collector 1.0 by /u/AshleyHummel'
)
 
print(reddit.read_only)
 
#TODO: change "Art" to a user-inputted subreddit
for submission in reddit.subreddit("Art").hot(limit=5):
   print(submission.title)