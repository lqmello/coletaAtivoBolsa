FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get update && apt install software-properties-common apt-transport-https ca-certificates curl gpg -y
RUN  curl -fSsL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /usr/share/keyrings/microsoft-edge.gpg > /dev/nul
RUN echo 'deb [signed-by=/usr/share/keyrings/microsoft-edge.gpg] https://packages.microsoft.com/repos/edge stable main'|tee /etc/apt/sources.list.d/microsoft-edge.list
RUN apt-get update && apt install microsoft-edge-stable -y


COPY . .

ENV FLASK_APP main.py

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
