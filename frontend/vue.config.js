const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack')

module.exports = defineConfig({
  transpileDependencies: true,

  // Đặt đường dẫn tương đối cho các tài nguyên tĩnh
  publicPath: process.env.NODE_ENV === 'production' ? '/static/vue/' : '/',

  // Cấu hình output khi build
  outputDir: '../static/vue',

  // Tách các chunks
  filenameHashing: true,

  // Cấu hình proxy cho API trong development
  devServer: {
    port: 8083, // Sử dụng port 8083 vì đó là port mà server đang chạy
    // Không sử dụng middleware để xử lý lỗi kết nối
    // Để proxy xử lý tất cả các request
    setupMiddlewares: (middlewares, devServer) => {
      if (!devServer) {
        throw new Error('webpack-dev-server is not defined');
      }

      return middlewares;
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        logLevel: 'debug',
        timeout: 5000, // 5 giây timeout
        onProxyReq(proxyReq, req, res) {
          // Log request
          console.log(`Proxy request: ${req.method} ${req.url}`);
        },
        onError: (err, req, res) => {
          console.log('Proxy error:', err);
          // Lỗi sẽ được xử lý bởi middleware ở trên
          if (!res.headersSent) {
            res.writeHead(500, {
              'Content-Type': 'application/json'
            });
            res.end(JSON.stringify({
              error: 'Không thể kết nối đến máy chủ API. Đang chuyển sang chế độ offline.'
            }));
          }
        }
      },
      '/media': {
        target: 'http://localhost:8001',
        changeOrigin: true
      },
      '/static': {
        target: 'http://localhost:8001',
        changeOrigin: true
      }
    },
    // Cấu hình history mode cho Vue Router
    historyApiFallback: {
      rewrites: [
        { from: /^\/dashboard/, to: '/index.html' },
        { from: /^\/company/, to: '/index.html' },
        { from: /^\/departments/, to: '/index.html' },
        { from: /^\/factories/, to: '/index.html' },
        { from: /^\/employees/, to: '/index.html' },
        { from: /^\/documents/, to: '/index.html' },
        { from: /^\/recruitment/, to: '/index.html' },
        { from: /^\/assets/, to: '/index.html' },
        { from: /^\/notifications/, to: '/index.html' },
        { from: /^\/profile/, to: '/index.html' },
        { from: /^\/settings/, to: '/index.html' },
        { from: /^\/login/, to: '/index.html' },
        { from: /./, to: '/index.html' }
      ]
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
    ],
    // Tối ưu hóa bundle
    optimization: {
      splitChunks: {
        chunks: 'all',
        minSize: 20000,
        maxSize: 250000,
        cacheGroups: {
          vendors: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: -10,
            chunks: 'initial'
          },
          common: {
            name: 'chunk-common',
            minChunks: 2,
            priority: -20,
            chunks: 'initial',
            reuseExistingChunk: true
          }
        }
      }
    }
  }
})
