import axios from "axios";

const useAxios = () => {
/*    const token = localStorage.getItem("token");*/

    const axiosInstance = axios.create({
        baseURL: 'http://127.0.0.1:8000/',
    });

    // Attach the token to requests
/*    axiosInstance.interceptors.request.use((config) => {
        if (token) {
            config.headers.Authorization = `Bearer `;
        }
        return config;
    });*/

    return axiosInstance;
};

export default useAxios;