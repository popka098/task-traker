import api from "./index"

export async function getHello() {
    const res = await api.get("");
    return res.data;
}