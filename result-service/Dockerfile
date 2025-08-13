# ./result-service/Dockerfile
## Using an official Node.js 18 image on Alpine Linux

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 80

CMD ["node", "server.js"]
