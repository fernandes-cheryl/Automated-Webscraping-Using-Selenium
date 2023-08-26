from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'


def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  # chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver


def get_videos(driver):
  driver.get(YOUTUBE_TRENDING_URL)
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
  return videos


def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  
  url = title_tag.get_attribute('href')
  
  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')
  
  channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel_name = channel_div.text
  
  description = video.find_element(By.ID, 'description-text').text
  
  views_and_streamed_div = video.find_elements(By.CLASS_NAME, 'inline-metadata-item')  #span class
  views = views_and_streamed_div[0].text
  
  streamed_ago = views_and_streamed_div[1].text

  return{
    'Title:' : title,
    'URL:' : url,
    'Thumbnail URL:' : thumbnail_url,
    'Channel name:' : channel_name,
    'Description:' : description,
    'Views:' : views,
    'Streamed ago:' : streamed_ago
  }


def send_email(body):
  SENDER_PASSWORD = os.environ['GMAIL_PASSWORD']  
  print('Password:', SENDER_PASSWORD)
  # body = "Thank you"
  
  # create an email message
  msg = MIMEMultipart()
  msg['Subject'] = 'Data'
  msg['From'] = 'cherylsparestorage@gmail.com'
  msg['To'] = 'cherylsparestorage@gmail.com'
  # add in the message body 
  msg.attach(MIMEText(body, 'plain'))
  msg.attach(MIMEText(u'<a href="https://docs.google.com/spreadsheets/d/1O3WNJrJJlozbgK_hZtat8x8xs15Wuk_C5-8TZ9gQi5c/edit#gid=0">Youtube Trending Google Sheet</a>','html'))

  # attach the CSV file to the email
  with open('trending.csv', 'rb') as f:
    attach = MIMEApplication(f.read(), _subtype='csv')
    attach.add_header('Content-Disposition', 'attachment', filename='trending.csv')
    msg.attach(attach)

  # send the email
  with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login('cherylsparestorage@gmail.com', SENDER_PASSWORD)
    smtp.send_message(msg)
  
  # try:
  #   server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
  #   server_ssl.ehlo()

  #   SENDER_EMAIL = 'cherylsparestorage@gmail.com'
  #   RECEIVER_EMAIL = 'cherylsparestorage@gmail.com'
  #   SENDER_PASSWORD = os.environ['GMAIL_PASSWORD']  
  #   print('Password:', SENDER_PASSWORD)
    
  #   subject = 'Youtube Trending Videos'
  #   # body = 'Hey, this is a test from Replit'
  #   message = f'''Subject: {subject}

    
  #   {body}'''

  #   server_ssl.login(SENDER_EMAIL, SENDER_PASSWORD)
  #   server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
  #   server_ssl.close()
  
  # except:
  #   print('Something went wrong!')


if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching trending videos')
  videos = get_videos(driver)
  
  print(f'Found {len(videos)} videos')

  print('Parsing videos')
  videos_data = [parse_video(video) for video in videos[:20]]
  print(videos_data)

  print('Saving data to CSV file')
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('trending.csv', index=None)

  print("Send videos over email")
  body = json.dumps(videos_data, indent=2)
  send_email(body)

  # Define the scope
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']
  
  # Add your service account file
  creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
  
  # Authorize the clientsheet 
  client = gspread.authorize(creds)
  
  # Get the instance of the Spreadsheet
  sheet = client.open('Youtube Trending Videos')
  
  # Get the first sheet of the Spreadsheet
  sheet_instance = sheet.get_worksheet(0)
  
  # Create a Pandas DataFrame
  # data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
  #         'Age': [23, 45, 35, 32],
  #         'Country': ['USA', 'Canada', 'Australia', 'Germany']}
  # df = pd.DataFrame(data)
  
  # Export the DataFrame to Google Sheets
  sheet_instance.insert_rows(videos_df.values.tolist(), 1)

  print('Done')
