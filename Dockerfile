FROM python:3.6.1-alpine
COPY . .
RUN pytest