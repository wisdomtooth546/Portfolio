FROM python:3.8
WORKDIR /WebApp
COPY . . 
RUN pip3 install -r requirements.txt
RUN apt-get update -y
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0
CMD python ./WebApp/app.py