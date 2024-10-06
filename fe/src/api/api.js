const apiUrl = process.env.API_URL;

const headers = {
    'Content-Type': 'application/json'
};

const responseToJson = r => {
    const P = r.json()
    if (r.status !== 200) {
        return P.then(body => {
            return Promise.reject({ error: true, body });
        });
    }
    return P.then(body => Promise.resolve({ error: false, body }));
};

export default {
    getStatic(path) {
        return fetch(`${apiUrl}/static/${path}`);
    },
    get(path) {
        return fetch(apiUrl + path, {
            headers
        }).then(responseToJson);
    },
    post(path, body) {
        return fetch(apiUrl + path, {
            method: 'POST',
            headers,
            body: JSON.stringify(body)
        }).then(responseToJson);
    }
};