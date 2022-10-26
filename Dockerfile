FROM python:3.7
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# steps needed for scipy
RUN apt-get update -y

RUN apt-get install -y python3-pip python3-dev libc-dev build-essential

RUN pip install -U pip

# Install pip requirements
ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "app.py"]