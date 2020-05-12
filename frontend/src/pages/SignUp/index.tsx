import React, { useCallback, useRef } from 'react';
import { Link, useHistory } from 'react-router-dom';
import { FiArrowLeft, FiMail, FiLock, FiUser, FiFileText } from 'react-icons/fi';
import { Form } from '@unform/web';
import { FormHandles } from "@unform/core";
import api from '../../services/api';

import * as Yup from 'yup';

import Input from "../../components/Input";
import Button from "../../components/Button";

import { Container, Content } from './styles';

interface SignUpFormData {
    name: string;
    email: string;
    password: string;
}

const SignUp: React.FC = () => {
    const formRef = useRef<FormHandles>(null);
    const history = useHistory();
    const handleSubmit = useCallback(async (data: SignUpFormData) => {
        try {
            const schema = Yup.object().shape({
                name: Yup.string().required('Nome obrigatorio'),
                cpf: Yup.number().typeError('Deve ser somente numeros'),
                email: Yup.string().required('E-mail obrigatorio').email('Digite um e-mail valido'),
                password: Yup.string().required('Senha obrigatoria'),
            });

            await schema.validate(data, {
                abortEarly: false,
            });

            await api.post('/api/users', data);

            history.push('/');

        } catch(err) {
            console.log(err);
        }
    }, [history]);

    return (
        <Container>
            <Content>
                <Form onSubmit={handleSubmit}>
                    <h1>Cadastro</h1>

                    <Input name="name" icon={FiUser} type="name" placeholder="Nome" />
                    <Input name="cpf" icon={FiFileText} type="cpf" placeholder="CPF" />
                    <Input name="email" icon={FiMail} placeholder="E-mail" />
                    <Input name="password" icon={FiLock} type="password" placeholder="Senha" />
                    <Input name="secondPassword" icon={FiLock} type="password" placeholder="Repetir Senha" />
                    <Input name="phone" icon={FiFileText} type="phone" placeholder="Telefone" />
                    <Input name="address" icon={FiFileText} type="address" placeholder="Endereço" />

                    <Button type="submit">Cadastrar</Button>
                </Form>
                <Link to="">
                    <FiArrowLeft />
                    Voltar
                </Link>
            </Content>
        </Container>
    );
}

export default SignUp;