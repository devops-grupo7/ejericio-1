#Use python 3.9 alpine docker image
FROM python:3.9-alpine

#Create user to avoid running as root user, extend PATH including user directory 
RUN adduser -D devops
USER devops
ENV PATH="/home/devops/.local/bin:${PATH}"

#Create and go to the app directory
WORKDIR app

#Copy and install necessary python packages
COPY --chown=devops:devops requirements.txt .
RUN pip3 install -r requirements.txt

#Copy application content
COPY --chown=devops:devops app/ .

#Expose port 5000, needed by the web server
EXPOSE 5000

#Execute app
ENTRYPOINT ["python3", "app.py"]

