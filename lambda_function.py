import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import boto3
import time

### Set up ChromeDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1280x1696')
chrome_options.add_argument('--user-data-dir=/tmp/user-data')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-level=0')
chrome_options.add_argument('--v=99')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--data-path=/tmp/data-path')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--homedir=/tmp')
chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
driver = webdriver.Chrome(chrome_options=chrome_options)

### Lambda Handler
def lambda_handler(event, context):
    ### Boto configuration
    boto = boto3.client('s3', region_name='us-west-1')
    url = event['url']

    if '://' in url:
        url = url.split('://')[1]

    ### Try HTTPS
    try:
        url = ('https://' + url)
        driver.get(url)

        ### Take screenshot and upload it to S3
        driver.save_screenshot('/tmp/screenshot.png')
        screen = url.split('://')[1] + '/' + time.strftime("%m-%d-%Y") + '/screenshot.png'
        if 'recordedfuture' in event:
            print(event)
            boto.upload_file('/tmp/screenshot.png', 'bucketname', str(screen))
        else:
            print(event)
            boto.upload_file('/tmp/screenshot.png', 'bucketname', str(screen))


        ### Save DOM as .txt file and upload it to s3
        dom = driver.page_source
        with open('/tmp/DOM.txt', 'w+') as f:
            f.write(dom)
            domfile = url.split('://')[1] + '/' + time.strftime("%m-%d-%Y") +'/DOM.txt'
            if 'recordedfuture' in event:
                boto.upload_file('/tmp/DOM.txt', 'bucketname', str(domfile))
                return
            else:
                boto.upload_file('/tmp/DOM.txt', 'bucketname', str(domfile))
                return

    ### Without HTTPS
    except:
        url = ('http://' + url)
        driver.get(url)

        ### Take screenshot and upload it to S3
        driver.save_screenshot('/tmp/screenshot.png')
        screen = url.split('://')[1] + '/' + time.strftime("%m-%d-%Y") + '/screenshot.png'
        if 'recordedfuture' in event:
            print(event)
            boto.upload_file('/tmp/screenshot.png', 'bucketname', str(screen))

        else:
            print(event)
            boto.upload_file('/tmp/screenshot.png', 'bucketname', str(screen))
            

        ### Save DOM as .txt file and upload it to s3
        dom = driver.page_source
        with open('/tmp/DOM.txt', 'w+') as f:
            f.write(dom)
            domfile = url.split('://')[1] + '/' + time.strftime("%m-%d-%Y") + '/DOM.txt'
            if 'recordedfuture' in event:
                boto.upload_file('/tmp/DOM.txt', 'bucketname', str(domfile))
                return
            else:
                boto.upload_file('/tmp/DOM.txt', 'bucketname', str(domfile))
                return
