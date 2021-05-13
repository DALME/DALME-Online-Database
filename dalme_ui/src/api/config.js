import Cookies from "js-cookie";

export const apiUrl = "https://data.127.0.0.1.sslip.io:8000";
export const dbUrl = "https://db.127.0.0.1.sslip.io:8000";
export const loginUrl = `${dbUrl}/accounts/login/`;
export const modalLoginUrl = `${apiUrl}/auth/login/`;
export const publicUrl = "https://127.0.0.1.sslip.io:8000";
export const purlUrl = "https://purl.127.0.0.1.sslip.io:8000";

export const fetchApi = (request) => fetch(request, { credentials: "include" });

export let headers = new Headers({ "X-CSRFToken": Cookies.get("csrftoken") });
