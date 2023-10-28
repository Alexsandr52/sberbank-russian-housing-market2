FROM python:3.10.9

WORKDIR /app
COPY . /app

# RUN apk update && apk add python3-dev \
#                           gcc \
#                           libc-dev \
#                           libffi-dev
# RUN python3.12 -m ensurepip --upgrade
# RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "/app/app/run_server.py"]