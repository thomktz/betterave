const Dotenv = require('dotenv-webpack');

// Check if VUE_APP_LOCAL_IP is set
if (!process.env.VUE_APP_LOCAL_IP) {
    throw new Error("VUE_APP_LOCAL_IP not set in .env file");
}

console.log(`Starting server on ${process.env.VUE_APP_LOCAL_IP}:8080`);

const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: process.env.VUE_APP_LOCAL_IP, 
  },
  configureWebpack: {
    plugins: [
      new Dotenv()
    ]
  },
  pluginOptions: {
    vuetify: {
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    }
  }
});
