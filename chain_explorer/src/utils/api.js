import axios from 'axios';

// MUDAR IP AQUI
export default axios.create({
    baseURL: `http://localhost:5000/`
});