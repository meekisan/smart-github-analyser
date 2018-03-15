FROM node
COPY . /data
WORKDIR /data
#RUN npm install -g pm2
RUN npm install --silent
#RUN npm run-script start-dev
CMD node commitSimulator.js
