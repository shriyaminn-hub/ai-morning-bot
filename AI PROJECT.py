import os

## fetch live weather data 
import requests
from datetime import datetime
### WEATHER API
api_key =os.environ.get('WEATHER_KEY')
## auto detect the city

city = os.environ.get('CITY')
print(f'detected city :{city}')
url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
response = requests.get(url)
data = response.json()
print(data)


temperature = data['main']['temp']
feels_like = data['main']['feels_like']
humidity = data['main']['humidity']
weather= data['weather'][0]['description']

print(f'CITY : {city}' )
print(f'TEMPERATURE : {temperature} C')
print(f'HUMIDITY : {humidity}%')
print(f'todays condition : {weather}')





### TRAFFIC API


##auto detection
city = os.environ.get('CITY')
lat  = float(os.environ.get('LAT'))
lon  = float(os.environ.get('LON'))


hour = datetime.now().hour
if 7 <= hour <= 10:
    status = '🚗 Morning rush hour — allow extra 15 mins!'
elif 17 <= hour <= 20:
    status = '🚗 Evening rush hour — allow extra 15 mins!'
else:
    status = '✅ Roads should be clear right now!'

print(f'traffic:{status}')




from groq import Groq

key = Groq(api_key = os.environ.get('GROQ_KEY'))

response = key.chat.completions.create(model = 'llama-3.3-70b-versatile',
                                       messages = [{'role' : 'user',
                                       'content' : 'Write a unique short motivation quote for Gen-Z with aestheic emojis'}])
print(response.choices[0].message.content)



prompt = f'''
you are a friendly morning assistant.
today in {city},{weather},{temperature}C
Traffic :{status}

Write one short unique intersting motivational quote (1-2 sentences max)for 
gen-z that also references the weather and encourages the person to have a amazing day

format it like that:
start with warm morning message
one line about weather and mention the weather and temperature always
one line about traffic and also tell if there is heavy or moderate or not as well 
one encouraging sentence to get start their day
end with a motivational sign off
and at the end write warm regards shriya sharma
also make all the sentence in cute aesthetic fonts but easy to read

'''

response  = key.chat.completions.create(model = 'llama-3.3-70b-versatile',
                                       messages = [{'role' : 'user',
                                       'content' : prompt}])
ai_message = response.choices[0].message.content
print(ai_message)



## gmail api



import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender   = os.environ.get('EMAIL_SENDER')
receivers = os.environ.get('EMAIL_reciever')
app_pass = os.environ.get('EMAIL_PASS')

msg            = MIMEMultipart()
msg['From']    = sender
msg['To']      = receivers
msg['Subject'] = 'AI Morning BRIEFING!'

msg.attach(MIMEText(ai_message, 'plain'))

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender, app_pass)
    server.send_message(msg)
    print('EMAIL SENT SUCCESSFULLY')






