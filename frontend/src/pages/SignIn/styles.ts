import styled from 'styled-components';
import signInBackgroundImg from '../../assets/meditation.jpg';
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
    max-width: 700px;

    form {
        margin: 10px 0;
        width: 340px;
        text-align: center;

        h1 {
            margin: 8px;
        }

        a {
            color: #FFF;
            display: block;
            margin-top: 8px;
            text-declaration: none;
            transition: color 0.2s; 

            &:hover {
                color: ${shade(0.2, '#FFF')}
            }
        }
    }
    > a {
        color: #ff9000;
        display: block;
        margin-top: 8px;
        text-declaration: none;
        transition: color 0.2s; 

        display: flex;
        align-items: center;

        svg {
            margin-right: 16px;
        }

        &:hover {
            color: ${shade(0.2, '#ff9000')};
        }
    }
`;

export const Background = styled.div`
    flex: 1;
    background: url(${signInBackgroundImg}) no-repeat center;
    background-size: cover; 
`;