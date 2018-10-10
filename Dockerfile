FROM python:3.6.1-alpine
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pytest