FROM node:latest
MAINTAINER moxin (moxin.chen@sap.com)

RUN npm install webpack -g

WORKDIR /tmp
COPY package.json /tmp/
RUN npm config set registry http://registry.npmjs.org/ && npm install

WORKDIR /usr/src/app
COPY . /usr/src/app
RUN cp -a /tmp/node_modules /usr/src/app/
RUN webpack

EXPOSE 8000

CMD ["npm", "start"]