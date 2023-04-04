FROM python:3.8-slim-buster
WORKDIR /
RUN pip3 install -r requirements.txt

CMD [ "python", "code_issues.py"]