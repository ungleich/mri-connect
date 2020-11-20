import axios from 'axios'
const Qs = require('qs');

let $axios = axios.create({
  baseURL: '/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token'
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {
  getExpertiseTopics () {
    return $axios.get(
      `topics/`
    )
      .then(response => response.data)
  },
  getPeopleSearch (query) {
    let params = { search: query }
    if (query === 'latest') {
      params = {}
    }
    return $axios.get(
      `search/`,
      { params: params }
    )
      .then(response => response.data)
  },
  getExpertiseSearch (query) {
    return $axios.get(
      `expertise/`, {
        params: { expertise: query },
        paramsSerializer: function(params) {
          return Qs.stringify(params, {arrayFormat: 'repeat'})
        }
      }
    )
      .then(response => response.data)
  },
  getAdvancedSearch (query) {
    return $axios.get(
      `advanced/`, {
        params: query
      }
    )
      .then(response => response.data)
  },
  getPeopleData (id) {
    return $axios.get(
      `people/` + id.toString() + `/`
    )
      .then(response => response.data)
  }
}
