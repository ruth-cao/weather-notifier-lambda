import os
import logging
import boto3

from weather import WeatherNotifier

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)

    latitude = get_parameter('latitude')
    longtitude = get_parameter('longtitude')
    units = get_parameter('units')
    apiKey = get_parameter('weatherapikey')
    weatherURL = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units={units}&appid={apiKey}'.format(lat=latitude, lon=longtitude, units=units, apiKey=apiKey)

    notifyMeURL = get_parameter('notifyMeURL')
    notifyMeAccessCode = get_parameter('notifyMeAccessCode')
    topicArn = get_parameter('topicArn')
    atmosphere = get_parameter('atmosphere')
    probability = get_parameter('probability')    
    notifier = WeatherNotifier(notifyMeURL, notifyMeAccessCode, topicArn, weatherURL, atmosphere, probability)
    notifier.notify_weather()

def get_parameter(name):
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name=name, WithDecryption=True)
    return parameter['Parameter']['Value']