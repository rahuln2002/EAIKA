export const saveToken = (token: string) => {
    localStorage.setItem("access_token", token);

    window.dispatchEvent(new Event("authChanged"));
};

export const getToken = () => {
    return localStorage.getItem("access_token");
};

export const logout = () => {
    localStorage.removeItem("access_token");

    window.dispatchEvent(new Event("authChanged"));
};

export const isAuthenticated = () => {
    return !!localStorage.getItem("access_token");
};
