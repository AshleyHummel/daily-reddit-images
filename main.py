# used to import environment variables
import os
from dotenv import load_dotenv
 
import smtplib # Simple Mail Transfer Protocol (Python module)
import ssl # module to access TLS (Transport Layer Security) --> makes transfer secure
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
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

# declare variables for email and saving images
posts = 1
image_count = 0
gif_found = False # triggered if gif is found... reduces number of posts sent in order to limit email size
path = os.environ.get('PATH_NAME') # access image path name from .env file
email = "Hello! Your daily reddit images from r/" + subreddit + " are here!"
msg.attach(MIMEText(email, "plain"))

print("Preparing email...")
print("Saving images...")
for submission in reddit.subreddit(subreddit).hot(limit=None):
  if "jpg" in submission.url or "png" in submission.url or "gif" in submission.url:
    # state titles of top 5 "hot" posts and Redditors who posted them in email
    email = "\n\n" + str(posts) + ") \"" + submission.title + "\" by u/" + submission.author.name + "\n"
    posts += 1
    msg.attach(MIMEText(email, "plain"))

    # define image path and give it a name, which contains the subreddit and post ID
    full_path_name = "blank"
    subtype = "blank"
    if "jpg" in submission.url :
      full_path_name = path + f"{subreddit}-{submission.id}.jpg"
      subtype = "jpeg"
      print("jpeg was found!")
    elif "png" in submission.url :
      full_path_name = path + f"{subreddit}-{submission.id}.png"
      subtype = "png"
      print("png was found!")
    elif "gif" in submission.url :
      full_path_name = path + f"{subreddit}-{submission.id}.gif"
      subtype = "gif"
      print("gif was found!")
      gif_found = True
    else :
      print("Image path was not able to be created.")

    # save images to workspace folder and embed image in email
    output = open(full_path_name, "wb")
    output.write(requests.get(submission.url).content) # save image to folder
    msg_image = MIMEImage(open(full_path_name, 'rb').read(), _subtype=subtype)
    msg.attach(msg_image) # attach image to email
    output.close()
    
    email = "\nImage link: " + submission.url
    msg.attach(MIMEText(email, "plain"))
    image_count += 1
    if image_count >= 5 or gif_found == True: # break loop when 5 images or 1 gif found
      break

# if gif was found, user is alerted that post number was limited (to reduce size of email)
if gif_found == True:
  email = "\n\nA gif was found and saved from r/" + subreddit + ". Only 1 post was sent to reduce email size. Sorry for the inconvenience!"
  msg.attach(MIMEText(email, "plain"))

email = "\n\nYour images have been saved to " + os.environ.get('PATH_NAME') + ". Enjoy!"
msg.attach(MIMEText(email, "plain"))

# use SMTP to access server and send email
def send_mail(sender_email, password, receiver_email, msg):
  print("Sending email...")
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print("Closing server...")
    server.quit()

# send email to user
send_mail(sender_email, password, receiver_email, msg)
print("Sent to " + receiver_email)