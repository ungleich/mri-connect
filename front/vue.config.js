const IS_PRODUCTION = process.env.NODE_ENV === 'production'

module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  baseUrl: IS_PRODUCTION
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
