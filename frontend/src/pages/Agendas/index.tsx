import React, { useCallback } from 'react';
import logoImg from '../../assets/logo.svg';
import { Form } from '@unform/web';
import Button from "../../components/Button";

import { useAuth } from "../../context/AuthContext";

const Agendas: React.FC = () => {

    const { signOut } = useAuth();

    const handleSubmit = useCallback(() => {
        try {
            signOut();
        } catch(err) {
            console.log(err)
        }
    }, [signOut]);

    return (
        <Form onSubmit={handleSubmit}>
            <img src={logoImg} alt="Zenbox" />
            <h1>Agendas</h1>
            <Button type="submit">Logout</Button>
        </Form>
    );
};

export default Agendas;