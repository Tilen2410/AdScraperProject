#FROM ubuntu:20.04
FROM mcr.microsoft.com/playwright:v1.34.3-jammy

RUN apt-get update

RUN apt-get install -y python3-pip

RUN pip install scrapy scrapy-playwright psycopg2-binary

RUN playwright install

#RUN apt-get update && playwright install-deps

WORKDIR /usr/app/src

COPY ./ ./

CMD ["scrapy", "crawl", "adspider"]