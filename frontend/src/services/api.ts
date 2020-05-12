import axios from "axios";

const api = axios.create({
    baseURL: 'http://192.168.15.72:8080'
});

export default api;