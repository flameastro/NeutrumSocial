"""
Este arquivo é a página de boas-vindas, é quando o usuário não possui o arquivo de login.
Coleta as informações do usuário e insere no database.
"""

import streamlit as st
import requests
import json
from time import sleep
from datetime import datetime

st.title('Bem vindo!')

try:
    with open('data/welcome-data.txt', 'r', encoding="utf-8") as f:
        pass
except:
    try:
        DATABASE = "https://neutrumsocial1-default-rtdb.firebaseio.com/.json"


        r = requests.get(DATABASE)
        json_data = r.json()

        if json_data == None:
            data = {
                "users": 1
            }

            r = requests.patch(DATABASE, json=data)
        else:
            old_users = json_data["users"]

            data = {
                "users": old_users + 1
            }

            r = requests.patch(DATABASE, json=data)
    except: pass

    st.balloons()

    st.toast("+1 Membro!", icon="🤗")
    sleep(2)

    st.toast("Faça login para receber todas as funcionalidades!", icon="⛄")


try:
    with open('./data/login.json', 'r', encoding="utf-8") as f:
        pass

except Exception as erro:
    st.subheader('O que é o :rainbow[NeutrumSocial]?')
    st.caption('NeutrumSocial é um projeto grande de uma simulação de Rede Social. Aqui você pode ser livre para criar contas, testar, fazer postagens e tudo mais! **Lembrete: Isso é uma simulação!**')

    st.subheader('Por que isso foi criado?')
    st.caption('Isso é uma simulação de um sistema completo, o que não é nada fácil de fazer, além de que fortalece a criatividade e o aprendizado. Isso é um desafio para Iniciantes, e com este sistema qualquer desenvolvedor será capaz de aprender algo. O objetivo desse projeto é apenas simular uma rede social, como anteriormente dito, e brincar com suas funcionalidades. Espero que você, usuário goste, e boa jornada.')

    st.subheader('🪐 Recursos do NeutrumSocial')
    st.caption("""Com o NeutrumSocial, você pode:
- 📝 Criar postagens com textos, imagens e links
- 💬 Enviar mensagens privadas
- 🧑‍🤝‍🧑 Seguir outros usuários
- 🔔 Receber notificações de interações
- 📊 Ver estatísticas básicas do seu perfil
- 🔐 Simulação de login/cadastro""")

    st.subheader('Como começar?')
    st.caption('O primeiro passo para entrar no NeutrumSocial é criar um nome de usuário e uma senha. Você pode fazer isso preenchendo seus dados. Caso não tenha uma conta, você pode criar uma no primeiro contâiner - Cadastrar. Porém, se já possui uma, você pode fazer login no segundo contâiner - Entrar.')

    def analysis_register():
        requirements = True # Garante que todos os requisitos estão corretos

        ## Nome de usuário
        # Verifica se o nome de usuário tem entre 6 caracteres e 25 caracteres
        if len(username) < 6 or len(username) > 25:
            st.badge('O nome de usuário deve estar entre 6 a 25 caracteres', color='red', icon='✖')
            requirements = False
        else:
            st.badge('O nome de usuário está entre 6 a 25 caracteres', color="green", icon='✔')

        # Verifica se o nome de usuário não tem caracteres especiais
        if username.isalnum():
            st.badge('O nome de usuário não tem símbolos especiais', color="green", icon='✔')
        else:
            st.badge('O nome de usuário não deve ter símbolos especiais', color='red', icon='✖')
            requirements = False


        ## Senha
        # Verifica se a senha tem entre 8 caracteres e 30 caracteres
        if len(password) > 30 or len(password) < 8:
            st.badge('A senha deve estar entre 8 a 30 caracteres', color='red', icon='✖')
            requirements = False
        else:
            st.badge('A senha está entre 8 a 30 caracteres', color="green", icon='✔')


        # Verifica se a senha não tem caracteres especiais
        if password.isalnum():
            st.badge('A senha não tem símbolos especiais', color="green", icon='✔')
        else:
            st.badge('A senha não deve ter símbolos especiais', color='red', icon='✖')
            requirements = False


        # Verifica se os requisitos são satisfeitos
        if requirements:
            DATABASE = "https://neutrumsocial1-default-rtdb.firebaseio.com/.json"

            firebase_data = { # BANCO DE DADOS FIREBASE
                username: {
                    "criação": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "senha": password,
                    "posts": {"0": "0"},
                    "status": {
                        "lista_seguindo": ["None"],
                        "lista_seguidores": ["None"],
                        "seguidores": 0,
                        "seguindo": 0,
                    }
                }
            }

            r = requests.get(DATABASE)
            json_data = r.json()

            if json_data and username in json_data:
                st.warning('Este nome de usuário já existe. Tente outro.')
            else:
                with st.spinner('Verificando Informações...'):
                    sleep(0.5)
                    r = requests.patch(DATABASE, json=firebase_data)
                    if r.status_code == 200:
                        st.info("Usuário criado com sucesso!")
                        st.toast("Usuário criado com sucesso!", icon="✔")

                        data = {
                            "user": {
                                "username": username,
                                "password": password,
                                "status": {
                                    "lista": [],
                                    "followers": 0,
                                    "following": 0
                                }
                            }
                        }

                        with open('./data/login.json', 'w', encoding="utf-8") as f:
                            json.dump(data, f, indent=4)

                            st.info('Página prestes a recarregar')
                            st.toast("Página prestes a recarregar!", icon="🔁")

                            sleep(0.5)
                            st.rerun()
                    else:
                        st.error("Erro ao criar o usuário:", r.status_code)

    def analysis_login():
        DATABASE = "https://neutrumsocial1-default-rtdb.firebaseio.com/.json"

        r = requests.get(DATABASE)
        json_data = r.json()

        if username in json_data:
            if json_data[username]["senha"] == password:
                if r.status_code == 200:
                    with st.spinner('Verificando Informações...'):
                        sleep(0.5)

                        st.info("Informações Corretas!")
                        st.toast("Informações Corretas!", icon="✔")

                        data = {
                            "user": {
                                "username": username,
                                "password": password,
                                "status": {
                                    "lista": [],
                                    "followers": 0,
                                    "following": 0
                                }
                            }
                        }

                        with open('./data/login.json', 'w', encoding="utf-8") as f:
                            json.dump(data, f, indent=4)

                            st.info('Página prestes a recarregar')
                            st.toast("Página prestes a recarregar🔁")

                            sleep(1)
                            st.rerun()

                    st.write('Login realizado!')
                else:
                    st.warning(f'Erro: {r.status_code}')
            else:
                st.warning('Senha incorreta')
        else:
            st.warning('Nome de usuário não encontrado')

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.expander('**Cadastrar - Criar uma conta**', expanded=True):
            st.markdown('<style>h2 {text-align: center;}</style><h2>Cadastrar</h2>', unsafe_allow_html=True)

            username = st.text_input('Crie seu nome de usuário')
            password = st.text_input('Crie sua senha', type="password")

            submit = st.button("Cadastrar", use_container_width=True)
            if submit:
                analysis_register()

    with col2:
        with st.expander('**Entrar - Já tem uma conta**', expanded=True):
            st.markdown('<style>h2 {text-align: center;}</style><h2>Entrar</h2>', unsafe_allow_html=True)

            username = st.text_input('Digite seu nome de usuário')
            password = st.text_input('Digite sua senha', type="password")

            submit = st.button("Entrar", use_container_width=True)
            if submit:
                analysis_login()
