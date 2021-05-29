import os # used to import environment variables
from dotenv import load_dotenv
 
import smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
 
import praw
 
load_dotenv()

sender_email = os.environ.get('GMAIL_USER')
password = os.environ.get('GMAIL_PASSWORD')
receiver_email = input("What email would you like your images sent to?")
subreddit = input("What subreddit would you like images from?")

subject = "Your Daily Reddit Images Are Here!" # title/subject of email
 
msg = MIMEMultipart()
msg["From"] = sender_email # set the sender's email
msg["To"] = receiver_email # set the receiver's email
msg["Subject"] = subject # set the subject
 
# Access top 5 "hot" subreddit posts
reddit = praw.Reddit(
client_id=os.environ.get('CLIENT_ID'),
client_secret=os.environ.get('CLIENT_SECRET'),
user_agent="Image collector 1.0 by /u/AshleyHummel"
)

email = "Hello! Your daily reddit images from r/" + subreddit + " are here! "
for submission in reddit.subreddit(subreddit).hot(limit=5):
  # state titles of top 5 "hot" posts and Redditors who posted them in email
  email += submission.title + "by u/" + submission.author.name + "\n"

print(email)
msg.attach(MIMEText(email, "plain"))
text = msg.as_string()

def send_mail(sender_email, password, receiver_email, msg):
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()

send_mail(sender_email, password, receiver_email, msg)
print("Sent to " + receiver_email)