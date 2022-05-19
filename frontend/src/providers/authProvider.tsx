// in src/authProvider.js
import decodeJwt from 'jwt-decode';

type loginFormType = {
  username: string;
  password: string;
};

export const authProvider =  {
  login: ({username, password} : loginFormType) => {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const request = new Request('http://localhost:8000/api/token', {
      method: 'POST',
      body: JSON.stringify({username, password}),
      //body: formData,
      headers: new Headers({'Content-Type': 'application/json'}),
    });
    return fetch(request)
      .then(response => {
        if (response.status < 200 || response.status >= 300) {
          throw new Error(response.statusText);
        }
        return response.json();
      })
      .then(({token}) => {
        const decodedToken : any = decodeJwt(token);
        localStorage.setItem('token', token);
        localStorage.setItem('permissions', decodedToken.permissions);
      });
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('permissions');
    return Promise.resolve();
  },
  checkError: (error: { status: number }) => {
    const status = error.status;
    if (status === 401 || status === 403) {
      localStorage.removeItem('token');
      return Promise.reject();
    }
    return Promise.resolve();
  },
  checkAuth: () => {
    return localStorage.getItem('token') ? Promise.resolve() : Promise.reject();
  },
  getPermissions: () => {
    const role = localStorage.getItem('permissions');
    return role ? Promise.resolve(role) : Promise.reject();
  },
};
