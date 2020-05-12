import React, {useRef, useCallback } from 'react';
import { Link } from "react-router-dom";
import { FiLogIn, FiMail, FiLock } from 'react-icons/fi';
import { Form } from '@unform/web';
import { FormHandles } from '@unform/core';
import * as Yup from 'yup';

import { useAuth } from "../../context/AuthContext";

import logoImg from '../../assets/logo.svg';

import Input from "../../components/Input";
import Button from "../../components/Button";

import { Container, Content, Background } from './styles';

interface SignInFormData {
    email: string;
    password: string;
};

const SignIn: React.FC = () => {
    const formRef = useRef<FormHandles>(null);

    const { signIn } = useAuth();

    const handleSubmit = useCallback(async (data: SignInFormData) => {
        try {
            const schema = Yup.object().shape({
                email: Yup.string().required('E-mail obrigatorio').email('Digite um e-mail valido'),
                password: Yup.string().required('Senha obrigatoria'),
            });

            await schema.validate(data, {
                abortEarly: false,
            });

            signIn({
                email: data.email,
                password: data.password,
            });
        } catch(err) {
            console.log(err)
        }
    }, [signIn]);

    return (
        <Container>
            <Content>
                <img src={logoImg} alt="Zenbox" />
                <Form ref={formRef} onSubmit={handleSubmit}>
                    <h1>Login</h1>

                    <Input name="email" icon={FiMail} placeholder="E-mail" />
                    <Input name="password" icon={FiLock} type="password" placeholder="Senha" />

                    <Button type="submit">Entrar</Button>

                    <h1>Ou entre por reconhecimento facial</h1>

                    <Button type="submit">Entrar</Button>

                    <a href="forgot">Esqueci minha senha</a>
                </Form>

                <Link to="/signup">
                    <FiLogIn />
                    Criar conta
                </Link>
            </Content>

            <Background />
        </Container>
    );
};

export default SignIn;