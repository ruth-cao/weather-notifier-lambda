import os
import logging
from weather import WeatherNotifier

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)

    weatherURL = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&units={units}&appid={apiKey}'.format(lat=os.environ['Latitude'], lon=os.environ['Longtitude'], part=os.environ['Excludes'], units=os.environ['Units'], apiKey=os.environ['WeatherApiKey'])
    notifier = WeatherNotifier(os.environ['NotifyAlexURL'], os.environ['NotifyAlexAccessCode'], os.environ['TopicArn'], weatherURL, os.environ['Atmosphere'], os.environ['Probability'])
    notifier.notify_weather()