import styled from 'styled-components';
import { shade } from 'polished';

export const Container = styled.div`
    height: 100vh;

    display: flex;
    align-items: stretch;
`;

export const Content = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;

    place-content: center;

    width: 100%;

    form {
        margin: 10px 0;
        width: 340px;
        text-align: center;

        h1 {
            margin: 18px;
        }

        a {
            color: #FFF;
            display: block;
            margin-top: 18px;
            text-declaration: none;
            transition: color 0.2s; 

            &:hover {
                color: ${shade(0.2, '#FFF')}
            }
        }
    }
`;