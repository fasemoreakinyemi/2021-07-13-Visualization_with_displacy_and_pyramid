FROM ubuntu:20.04
RUN apt-get update -y && \
apt-get install -y python3-pip python3-dev && \
pip3 install --upgrade pip setuptools

WORKDIR \livivo_sru
COPY livivo_sru .

RUN pip3 install --upgrade pip && \
    pip3 install -e . && \
    python3 -m spacy download en
#    python3 ./livivo_sru/data/seed_database.py

EXPOSE 6543

CMD ["pserve","development.ini"]

