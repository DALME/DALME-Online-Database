import Cookies from "js-cookie";

const urlPatterns = {
  development: "127.0.0.1.sslip.io:8000",
  // beta: "beta.dalme.org",
  beta: "127.0.0.1.sslip.io:8000",
  production: "dalme.org",
};

export const publicUrl = `https://${urlPatterns[process.env.NODE_ENV]}`;
export const apiUrl = `${publicUrl}/api`;
export const coreUrl = `${publicUrl}/core`;
export const loginUrl = `${coreUrl}/accounts/login/`;
export const modalLoginUrl = `${apiUrl}/auth/`;
export const purlUrl = `${publicUrl}/purl`;

export const fetcher = (request) => fetch(request, { credentials: "include" });

export let headers = () =>
  new Headers({
    "X-CSRFToken": Cookies.get("csrftoken"),
    "Content-Type": "application/json",
  });
