FROM node:lts-alpine

WORKDIR /app

# Install Vue CLI globally
RUN npm install -g @vue/cli@5.0.8
# Install the vue cli-service
RUN npm install -g @vue/cli-service@5.0.8

# Add Vue CLI to PATH
ENV PATH /usr/local/share/.config/yarn/global/node_modules/.bin:$PATH

# Copy package.json and package-lock.json
COPY package.json .

# Install dependencies
RUN rm -rf node_modules package-lock.json && npm install

CMD ["npm", "run", "serve"]