FROM node:lts-alpine

WORKDIR /app

# Install Vue CLI globally
RUN npm install -g @vue/cli@5.0.8

# Add Vue CLI to PATH
ENV PATH /usr/local/share/.config/yarn/global/node_modules/.bin:$PATH

# Copy package.json and package-lock.json
COPY package.json .
COPY package-lock.json .

# Install dependencies
RUN npm install

CMD ["npm", "run", "serve"]