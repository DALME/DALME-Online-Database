const urlPatterns = {
  development: "127.0.0.1.sslip.io:8000",
  beta: "beta.dalme.org",
  production: "dalme.org",
};

export const publicUrl = `https://${urlPatterns[process.env.NODE_ENV]}`;
export const apiUrl = `${publicUrl}/api`;
export const coreUrl = `${publicUrl}/core`;
export const purlUrl = `${publicUrl}/purl`;
export const loginUrl = `${apiUrl}/jwt/login/`;
export const logoutUrl = `${apiUrl}/jwt/logout/`;
export const tokenRefreshUrl = `${apiUrl}/jwt/token/refresh/`;
