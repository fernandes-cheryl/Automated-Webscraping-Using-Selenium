# Automated-Webscraping-Using-Selenium
Automate webscraping for top 10 trending videos on Youtube using Selenium and set up a recurring job to send data via email using python on AWS Lambda.

## Objective:
  1. Scrape top 10 trending videos on YouTube using Selenium.
  2. Set up a recurring job on AWS Lambda to scrape every 30 minutes.
  3. Send the results as a CSV attachment over email and to a spreadsheet.

## Tools and services used:
  * Replit     
    For the development stage (code is developed here)
    
  * Selenium  
    Used to scrape the youtube website for trending video details
    
  * AWS Lambda  
    The python code developed on replit is deployed on lambda and is triggered every 30 minutes to scrape the site
    
  * SMTP and MIME  
    These libraries are used for sending csv files and details over email

  ## Process:
  1. Create and launch a repository on Replit  
    * Connect Replit with your GitHub account  
    * Launch the repository as a Replit project  
    * Set up the language and run command  
    * Create and execute a Python script  
      
  2. Extract information using Selenium  
    * Install selenium and create a browser driver  
    * Load the page and extract information  
    * Create a CSV of results using Pandas  
      
  3. Set up a recurring job on AWS Lambda  
    * Create an AWS Lambda Python function   
    * Deploy the python script created on replit  
    * Add layers for Selenium and Chromium and additional modules used  
    * Set up recurring job using AWS CloudWatch  
      
  4. Send results over email using SMTP and MIME  
    * Create email client using smtplib  
    * Set up SSL, TLS and authenticate with password  
    * Send an email with text and attachment (csv file)  

  ## References:
  For updating the gpead sheet: 
  https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/
  
  To send DataFrame as a CSV file
  https://saturncloud.io/blog/how-to-send-pandas-dataframe-using-python/

  To export DataFrame to Google sheets
  https://saturncloud.io/blog/how-to-export-pandas-dataframe-to-google-sheets-using-python/
  https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/

  To Deploy Python Selenium Script in AWS Lambda
  https://www.youtube.com/watch?v=b49Y3NGJX68

  To Install Pandas on AWS Lambda Function
  https://www.youtube.com/watch?v=1UDEp90S9h8
