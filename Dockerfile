FROM python:3

WORKDIR /usr/src/app

ENV AUTH_URL 'https://login.salesforce.com/services/oauth2/token'
ENV QUERY_URL 'https://na59.salesforce.com/services/data/v39.0/query'
ENV OBJECT_FIELDS_URL  'https://na59.salesforce.com/services/data/v20.0/sobjects/Lead/describe'
ENV CLIET_ID '3MVG9zlTNB8o8BA2cQ0oXGFzLbo54UdVYwhqLthwmtQXfuIwl5d0gK9x8Yaw373.bwYs0r1Mvktzw6fZ4Us5Y'
ENV CLIENT_SECRET 'B994580C536D24DB0BD58E5E84038CD1F933CA9834DB17A992A408ACB41BB8CC'
ENV PASSWORD  'bmasters2020'
ENV USERNAME  'md02-ach@basementremodeling.com'

ENV DB_NAME = "scheduler",
ENV DB_USER = "postgres", 
ENV DB_PASSWORD = "postgres", 
ENV DB_HOST = "127.0.0.1", 
ENV BD_PORT = "5432")

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

#COPY . .

#CMD [ "python", "./your-daemon-or-script.py" ]