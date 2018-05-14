![The SAP Product Haystack](https://raw.githubusercontent.com/smbinnovationlab/haystack/master/resource/The%20SAP%20Product%20Haystack.png)

***

**Your products are like a needle in the great big world-wide-web haystack.**

Keeping up to date is almost impossible. There are a whole host of sites which all have their own opinion on how your products should look and what the price should be. The more successful your products are, the more places will be selling them. It just gets harder.

With **Product Haystack**, see in real-time where your products are making an online impression. The haystack uses AI image recognition to identify products without relying on keywords and language translations. At the core of the Haystack is a complex web-crawler to continuously sense the sites and pages where your products feature.



## Introduction

- **haystack-api**: The core of the Product Haystack. An image-based web crawler and machine
  learning analyzing engine to extract the product information, such as price, currency, etc.
- **haystack**: A Website for tracking your products based on the haystack api.
- **haystack-webui**: UI.




## Setup

### Environment

**Frontend**: React, Ant Design

**Backend**: Python3, MySQL

**Backend Dependencies**: 

```
Flask						   # server
beautifulsoup4, pyquery          # parse the HTML source code
SQLAlchemy                       # SQL ORM toolkit
scikit-learn                     # machine learning toolkit
selenium                         # simulate browser for headless OS, for screenshots
pika                             # connect to RabbitMQ
```

For all of the dependencies, please refer to ` XXX/app/requirements `.

**Deploy**: Flask + uWSGI + Nginx, Docker



### haystack-api

**Demo**:

![haystack-api demo](https://raw.githubusercontent.com/smbinnovationlab/haystack/master/resource/haystack-api_demo.gif)

**Steps**:

1. Install Docker and Docker Compose.

2. Apply for an [Google Vision API](https://cloud.google.com/vision/) in Google Cloud Platform for image searching.

3. Build and start the docker containers

   ```sh
   sudo KEY="YOUR_GOOGLE_API_KEY" docker-compose up -d
   ```
   
   
   Haystack: http://localhost:8001
   API: http://localhost:8002
   
   change timestamp of data:
   under: copy script/update_event_date.py to app/script/u.py
   goto docker:  docker exec -it haystack_server  /bin/bash 
   run script in docker: python u.py db test
   
   
   
   

**Notes:**

- Replace the string "YOUR_GOOGLE_API_KEY" in step 2 with your Google API key applied in step 1.

- The default password for root in MySQL is "test", you can modify it in ` docker-compose.yml - services - db - environment - MYSQL_ROOT_PASSWORD ` and ` app\db\mysql_conf.conf `.

- TThe image searching engine and the product analyzing engine which is composed of multiple layers ("microdata_analyzer", "url_pattern_analyzer", "multi_pattern_analyzer") can be easily scaled to improve the performance by using the ` scale ` command of Docker Compose.

  ```bash
  sudo KEY="YOUR_GOOGLE_API_KEY" docker-compose up -d --scale image_searching_engine=3 --scale microdata_analyzer=6 --scale url_pattern_analyzer=3 --scale multi_pattern_analyzer=3
  ```

Architecture (Haystack-API)

upload image from web or SDK => RabbitMQ => image_searching_engine -> RabbitMQ -> microdata_analyzer -> RabbitMQ -> url_pattern_analyzer -> multi_pattern_analyzer


### haystack

Please follow the instruction for setting up the **haystack-api**.

```bash
sudo KEY="YOUR_GOOGLE_API_KEY" docker-compose up -d
```



### haystack-webui

1. Install packages

   ``````
   npm install
   ``````

2. Run webpack-dev-server for development

   ```
   npm start
   ```

3. Build

   ```
   webpack
   ```

   ​After build, move the file ` xxx\build\bundle.js ` to ` xxx\static\build\ ` .



## Credits

Collaborators: ***@Ma, Ziyin***, ***@Ding, Morning Ding***.
