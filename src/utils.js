import axios from "axios";


export const fetchArtists = async () => {
    try {
        return await axios.get(`/get_artists`);
    } catch (e) {
        return [];
    }
};