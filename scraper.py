from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'


def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
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


if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching trending videos')
  videos = get_videos(driver)
  
  print(f'Found {len(videos)} videos')

  print('Parsing videos')
  videos_data = [parse_video(video) for video in videos[:10]]
  print(videos_data)

  print('Saving data to CSV file')
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('trending.csv', index=None)


