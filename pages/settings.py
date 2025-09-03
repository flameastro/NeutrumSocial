"""
Este arquivo é responsável pelas configurações do site em si.
Permite que o usuário possa sair, deletar sua conta ou ver mais sobre o projeto.
"""

import streamlit as st
from assets.css.no_login_centralized import set_style
import json
import requests
import os
from time import sleep


recharge = False
try:
    st.title(':material/build: Configurações')

    with st.popover(":material/info: Sobre", use_container_width=True):
        st.caption("""O que é o NeutrumSocial?

É uma simulação de uma rede social, que permite que o usuário possa interagir com o sistema, podendo criar seus próprios posts, configurar sua conta, conversar com amigos e muito mais.

Por que foi criado?

Meu objetivo era fazer um projeto de uma rede social "sem limites" - onde o usuário pode criar coisas com sua imaginação e vontade.""")

    with st.popover(":material/logout: Sair", use_container_width=True):
        st.caption("Caso você deseja sair, precisará entrar novamente para acessar sua conta. Isso não irá apagar seus dados, nem deletará a sua conta.")

        if st.button("Sair", use_container_width=True):
            with st.spinner("Saindo..."):
                sleep(0.5)

            with open('./data/login.json', 'r', encoding="utf-8") as f:
                username = json.load(f)
                username = username['user']['username']


            files = ['./data/follow.json', './data/login.json', './data/user-birth.json', './data/user-description.json', './data/user-image.png', './data/user-lastname.json', './data/user-name.json', './data/welcome-data.txt']

            for file in files:
                try:
                    os.remove(file)
                except:
                    pass

            recharge = True

    with st.popover(":material/no_accounts: Deletar Conta", use_container_width=True):
        st.caption("Atenção: Esta ação é irreversível e apagará todos os seus dados.")

        verify = st.text_input("Digite sua senha para confirmar a exclusão da conta", type="password")

        with open('./data/login.json', 'r', encoding="utf-8") as f:
            password = json.load(f)
            password = password['user']['password']

        if st.button("Deletar Conta", use_container_width=True):
            if verify == password:
                with st.spinner("Deletando conta..."):
                    sleep(0.5)

                with open('./data/login.json', 'r', encoding="utf-8") as f:
                    username = json.load(f)
                    username = username['user']['username']


                files = ['./data/follow.json', './data/login.json', './data/user-birth.json', './data/user-description.json', './data/user-image.png', './data/user-lastname.json', './data/user-name.json', './data/welcome-data.txt']

                for file in files:
                    try:
                        os.remove(file)
                    except:
                        pass
                DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/.json"
                r = requests.delete(DATABASE)

                # Decrementa -1 em users
                r = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/users/.json")
                update_users = int(r.json()) - 1

                r = requests.patch(f"https://neutrumsocial1-default-rtdb.firebaseio.com/users/.json", json=update_users)

                st.success("Conta deletada com sucesso!")
                recharge = True

            else:
                st.error("Senha incorreta.")
except:
    set_style(True, True, True)

    st.title('👀 Pronto para ver o que ninguêm vê?')
    st.caption('Vamos explorar as configurações - Uma selva de funcionalidades!')

    if st.button(':material/login: Criar conta ou Entrar'):
        st.switch_page('pages/welcome.py')

if recharge:
    st.switch_page("pages/initial.py")
