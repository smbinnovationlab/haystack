FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY uwsgi.ini /app/uwsgi.ini

COPY ./ /src/haystack/app

WORKDIR /src/haystack/app

RUN apt-get update \
&& apt-get install -y apt-utils \
&& apt-get install -y sudo wget \
&& apt-get install -y build-essential chrpath libssl-dev libxft-dev \
&& apt-get install -y libfreetype6 libfreetype6-dev \
&& apt-get install -y libfontconfig1 libfontconfig1-dev \
&& wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 \
&& tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/ \
&& sudo ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin \
&& cd /src/haystack/app \
&& pip install -r requirements.txt
