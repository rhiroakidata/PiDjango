import React, { createContext, useCallback, useState, useContext } from 'react';
import api from "../services/api";

interface SignInCredentials {
    email: string;
    password: string;
};

interface AuthState {
    token: string;
    user: object;
};

interface AuthContextData {
    user: object;
    signIn(credentials: SignInCredentials): Promise<void>;
    signOut(): void;
};

const AuthContext = createContext<AuthContextData>(
    {} as AuthContextData
);

const AuthProvider: React.FC = ({ children }) => {
    const [data, setData] = useState<AuthState>(() => {
        const token = localStorage.getItem('@Zenbox:token');
        const user = localStorage.getItem('@Zenbox:user');

        if(token && user) {
            return { token, user: JSON.parse(user) };
        }
        return {} as AuthState;
    });

    function getCookie(name: String) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCookie('CSRF-TOKEN');

    const signIn = useCallback(async ({ email, password }) => {
        const response = await api.post('login', {
            email,
            password,
        },
        {
            headers: {
                 'X-CSRFTOKEN': csrfToken,
             },
        },
        );

        const { token, user } = JSON.parse(response.data);

        localStorage.setItem('@Zenbox:token', token);
        localStorage.setItem('@Zenbox:user', JSON.stringify(user));

        setData({ token, user });
    }, []);

    const signOut = useCallback(() => {
        localStorage.removeItem('@Zenbox:token');
        localStorage.removeItem('@Zenbox:user');

        setData({} as AuthState);
    }, []);

    return (
        <AuthContext.Provider value={{ user: data.user, signIn, signOut }}>
            {children}
        </AuthContext.Provider>
    );
};

function useAuth(): AuthContextData {
    const context = useContext(AuthContext);

    if(!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }

    return context;
};

export {AuthProvider, useAuth};