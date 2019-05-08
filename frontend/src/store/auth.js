import { 
    AUTH_REQUEST,
    AUTH_TOKEN,
    USER_REQUEST,
    AUTH_LOGOUT,
    AUTH_SIGNUP,
} from './mutation-types'
// import apiCall from '../api/common'
import axios from 'axios'

const state = {
    token: localStorage.getItem('user-token') || '',
}

const getters = {
    token: state => state.token,
    isAuthenticated: state => !!state.token,
}

const actions = {
    [AUTH_SIGNUP]: ({commit, dispatch}, user) => {
        return new Promise((resolve, reject) => {
            console.log(user);
            axios
            .post('http://127.0.0.1:8000/api/send_invite/', {
                "email": user.email,
            })
            .then(resp => {
                console.log(resp)
                axios
                .post('http://127.0.0.1:8000/api/users', {
                    "email": user.email,
                    "password": resp.data.password,
                    "profile": {}
                })
                .then(response => {
                    console.log(response)
                    resolve(resp.data.password)
                })
                .catch(err => {
                    reject(err)
                    console.log(err);
                })
            })
            .catch(err => {
                reject(err)
                console.log(err);
            })
        })
    },
    [AUTH_REQUEST]: ({commit, dispatch, state}, user) => {
        return new Promise((resolve, reject) => {
            axios
            .post('http://127.0.0.1:8000/api/get_auth_token/', {
                "email": user.email,
                "password": user.password
            })
            .then(response => {
                const token = response.data.token
                commit(AUTH_TOKEN, response.data)
                localStorage.setItem('user-token', token)
                axios.defaults.headers.common['Authorization'] = token
                resolve(response)
            })
            .catch(err => {
                localStorage.removeItem('user-token')
                reject(err)
                console.log(err);
            })
        })
    },
    [AUTH_LOGOUT]: ({commit, dispatch}) => {
        return new Promise((resolve, reject) => {
            commit(AUTH_LOGOUT)
            localStorage.removeItem('user-token')
            delete axios.defaults.headers.common['Authorization']
            resolve()
        })
    }
}

const mutations = {
    [AUTH_TOKEN]: (state, resp) => {
        state.token = resp.token
    },
    [AUTH_LOGOUT]: (state) => {
        state.token = ''
        state.profile = {}
    },
}

export default {
    state,
    getters,
    actions,
    mutations,
}