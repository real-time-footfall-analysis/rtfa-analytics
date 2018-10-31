FROM python:3.6.1-alpine
COPY . .
RUN pip install --upgrade pip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt
RUN python3 -m pytest -vv test
ENTRYPOINT ["python"]
CMD ["webapp.py"]
EXPOSE 80