FROM python:3

WORKDIR /usr/src/app

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip";\ 
         unzip awscliv2.zip; ./aws/install

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
#COPY . . remove that 
# RUN chmod +x ./entrypoint.sh and that
# ENTRYPOINT [ "./entrypoint.sh" ] and that
#CMD [ "python", "./runner.py" ]