const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  transpileDependencies: true,
  // Đặt đường dẫn tương đối cho các tài nguyên tĩnh
  publicPath: process.env.NODE_ENV === 'production' ? '/static/vue/' : '/',

  // Cấu hình output khi build
  outputDir: '../static/vue',

  // Cấu hình proxy cho API
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },

  // Cấu hình để không tạo source map trong production
  productionSourceMap: false,

  // Cấu hình CSS
  css: {
    loaderOptions: {
      sass: {
        additionalData: `
          @import "@/assets/scss/variables.scss";
        `
      }
    }
  },

  // Cấu hình webpack
  configureWebpack: {
    plugins: [
      // Định nghĩa các feature flags
      new webpack.DefinePlugin({
        __VUE_OPTIONS_API__: true,
        __VUE_PROD_DEVTOOLS__: false,
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
      })
    ]
  }
})
