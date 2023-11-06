# base image
FROM node:16-alpine

# set working directory
WORKDIR /app

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install --silent
RUN npm install vue@next

# Copy project files into the docker directory
COPY . /app

# build app for production with minification
RUN npm run build

EXPOSE 8080

CMD ["npm", "run", "serve"]
