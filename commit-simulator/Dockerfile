FROM node
RUN npm install -g pm2
COPY . /data
WORKDIR /data
#RUN npm install --silent 
#npm install --silent && npm run-script start-dev
CMD node commitSimulator.js
