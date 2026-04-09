

## fetch live weather data 



pip install requests

import requests



### WEATHER API
api_key =os.environ.get('WEATHER_KEY')
## auto detect the city
geo = requests.get('https://freeipapi.com/api/json')
city = geo.json()['cityName']
print(f'detected city :{city}')
url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
response = requests.get(url)
data = response.json()
print(data)

print(geo.json())

temperature = data['main']['temp']
feels_like = data['main']['feels_like']
humidity = data['main']['humidity']
weather= data['weather'][0]['description']

print(f'CITY : {city}' )
print(f'TEMPERATURE : {temperature} C')
print(f'HUMIDITY : {humidity}%')
print(f'todays condition : {weather}')





### TRAFFIC API





traffic_key = os.environ.get('tomtom_key')
##auto detection
lon = geo.json()['longitude']
lat = geo.json()['latitude']
traffic_url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json'
params = {'point':f'{lat},{lon}','key':traffic_key}

traffic_response = requests.get(traffic_url,params=params)
traffic_data = traffic_response.json()
print(traffic_data)








flow = traffic_data['flowSegmentData']
current_speed = traffic_data['flowSegmentData']['currentSpeed']
free_speed = traffic_data['flowSegmentData']['freeFlowSpeed']## when roads are like empty then free flow
conf = traffic_data['flowSegmentData']['confidence']

percentage = (current_speed / free_speed)*100

if percentage >80:
    status = 'CLEAR ROADS - 🌷 YOU CAN HEAD OUT AND HAVE A SMOOTH DRIVE YAYYYYY!!!'
elif percentage >50:
    status = 'MODERATE TRAFFIC - ⚠️ TRY LEAVING 10 MINS BEFORE'
else:
    status = 'HEAVY TRAFFIC - ‼️ TRY LEAVE EARLY OR MAYBE WORK FROM HOME TODAYYYYY OR MAYBE STAY SLEEP'

MESSAGE =(f'TRAFFIC : {status} (SPEED :{current_speed}km/h)')
print(MESSAGE)





##gemini AI INTEGRATION




pip install groq


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
receivers = os.environ.get('EMAIL_SENDER')
app_pass = os.environ.get('EMAIL_reciever')

msg            = MIMEMultipart()
msg['From']    = sender
msg['To']      = ','.join(receivers)
msg['Subject'] = 'AI Morning BRIEFING!'

msg.attach(MIMEText(ai_message, 'plain'))

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender, app_pass)
    server.send_message(msg)
    print('EMAIL SENT SUCCESSFULLY')






