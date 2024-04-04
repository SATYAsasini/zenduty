FROM python:3.8
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install requests python-dotenv
ENV zenduty_token=$zenduty_token

CMD ["python", "ruleApplier.py"]
