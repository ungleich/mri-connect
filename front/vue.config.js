const IS_PRODUCTION = process.env.NODE_ENV === 'production'

module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  publicPath: IS_PRODUCTION
    ? 'https://mri.django-hosting.ch/'
    : '/',
  devServer: {
    proxy: {
      '/api*': {
        target: 'http://localhost:8000/'
      }
    }
  }
}
