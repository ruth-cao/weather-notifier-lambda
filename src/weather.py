import boto3
import logging
import requests
import json

from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class WeatherNotifier:
    def __init__(self, notifyAlexa, accessCode, topicArn, weatherURL, atmosphere, probability):
        self.notifyAlexa = notifyAlexa
        self.accessCode = accessCode
        self.topicArn = topicArn
        self.weatherURL = weatherURL
        self.ATMOSPHERE = atmosphere
        self.PROBAILITY = probability
    
    def notify_weather(self):
        weatherResponse=requests.post(url=self.weatherURL)
        weather_dict = weatherResponse.json()

        current_weather=weather_dict['current']['weather']
        realCondition = next(filter(lambda weather: weather['id'] <= self.ATMOSPHERE, current_weather), None)

        if 'hourly' in weather_dict:
            sorted_hour=sorted(weather_dict['hourly'], key=lambda hour: hour['dt'])
            mean_probability = (sorted_hour[0]['pop'] + sorted_hour[1]['pop']) / 2
            # if current weather is not good or probability in the next two hours is higher than threshold
            if realCondition or mean_probability >= self.PROBABILITY:
                logger.info('mean probability is %s', mean_probability)
                msg = ''
                if (realCondition):
                    msg = 'Weather is {0}. '.format(realCondition['main'])
                else:
                    msg = 'The probability of rainining is {0}. '.format(mean_probability)
                msg += 'Consider bringing an umbrella.'
                logger.info(msg)
                req = json.dumps({
                    "notification": msg,
                    "accessCode": self.accessCode
                })
                response = requests.post(url = self.notifyAlexa, data = req)
                status_code = response.status_code
                
                # if failed to publish to Alexa, send an email 
                if status_code != 202:
                    sns = boto3.client('sns')
                    response = sns.publish(
                        TopicArn=self.topicArn,
                        Message='the response code is {0}'.format(200),
                        Subject='Fail to notify Alexa')
            else:
                logger.warning('weather is clear. no notification sent.')

