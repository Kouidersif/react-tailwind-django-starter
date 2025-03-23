import Cookies from "js-cookie"


export const setCookies = (name, value, options) => {
    Cookies.set(name, value, options);
    return;
}

export const getCookies = (name) => {
    return Cookies.get(name);
}