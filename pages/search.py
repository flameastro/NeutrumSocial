"""
Este arquivo permite pesquisar por usuários, assim podendo ver informações básicas e seguir o usuário.
Além de mostrar também uma aba com alguns usuários.
"""

import streamlit as st
import requests
from assets.css.no_login_centralized import set_style
import json

try:
    st.caption("Que tal encontrar amigos e novas pessoas?")
    find_username = st.text_input(":material/id_card: Digite o nome de usuário que deseja encontrar", placeholder="Nome de usuário")

    DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{find_username}/.json"

    r = requests.get(DATABASE)
    json_data = r.json()

    submit = st.button(':material/travel_explore: Encontrar', type="primary")

    # Abre o arquivo de login para obter o nome de usuário do usuário atual
    with open('./data/login.json', 'r', encoding="utf-8") as f:
        username = json.load(f); username = username['user']['username']

    # st.session_state
    if 'clique' not in st.session_state:
        st.session_state['clique'] = False

    if submit:
        st.session_state['clique'] = True

    if st.session_state['clique']:
        with st.spinner("Carregando"):
            if json_data is None or find_username == "" or find_username == "users": # Verifica se o usuário existe
                st.error(':material/error: Usuário não encontrado. Tente novamente.')

            elif find_username == username: # Verifica se o usuário buscado é o mesmo que o usuário atual
                st.warning(':material/warning: Você não pode procurar a si mesmo.')

            else: # Se nenhum dos casos acima for verdadeiro, exibe os dados do usuário encontrado
                for key, value in json_data.items():
                    if 'criação' in key or 'senha' in key or 'posts' in key or 'chat' in key:
                        pass

                    else:
                        if key == 'status':
                            for key2, value2 in value.items():
                                if "lista_seguidores" in key2 or "lista_seguindo" in key2:
                                    pass
                                else:
                                    st.write(f"<span style='display:inline-block; width:150px; font-weight:bold'>{key2}:</span> {value2}", unsafe_allow_html=True)

                        else:
                            st.markdown(f"<span style='display:inline-block; width:150px; font-weight:bold'>{key}:</span> {value}", unsafe_allow_html=True)


                # Verificando se o usuário já segue o outro usuário
                DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/status/lista_seguindo/.json"
            
                r = requests.get(DATABASE)
                json_data = r.json()

                if find_username in json_data:
                    st.success(f":material/check: Seguindo {find_username}")

                else:
                    with st.empty():
                        follow_button = st.button("Seguir")
                        if follow_button:
                            # Criando a data de chat/conversa
                            data = {"chat": {find_username: {"letra": "a", "main": username, "sec": find_username}}}
                            r = requests.patch(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/.json", json=data)

                            data = {"chat": {username: {"letra": "b", "main": username, "sec": find_username}}}
                            r = requests.patch(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{find_username}/.json", json=data)


                            # Atualizando a lista_seguindo do usuário que seguiu
                            DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/status/lista_seguindo/.json"
                            r = requests.get(DATABASE)

                            data = {
                                len(r.json()): find_username
                            }
                            r = requests.patch(DATABASE, json=data)

                            # Atualizando o "seguindo" do usuário que seguiu
                            DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/status/.json"
                            r = requests.get(DATABASE)

                            following = r.json()['seguindo'] + 1

                            data = {
                                'seguindo': following
                            }
                            r = requests.patch(DATABASE, json=data)

                            # Atualizando a lista_seguidores do usuário que foi seguido
                            DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{find_username}/status/lista_seguidores/.json"
                            r = requests.get(DATABASE)

                            data = {
                                len(r.json()): username
                            }
                            r = requests.patch(DATABASE, json=data)

                            # Atualizando o "seguidores" do usuário que foi seguido
                            DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{find_username}/status/.json"
                            r = requests.get(DATABASE)

                            followers = r.json()['seguidores'] + 1

                            data = {
                                'seguidores': followers
                            }
                            r = requests.patch(DATABASE, json=data)

                            st.rerun()

    with st.popover("Deseja encontrar pessoas?"):
        st.caption("Aqui vai algumas sugestões de pessoas que você pode encontrar")

        DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/.json"

        r = requests.get(DATABASE)
        json_data = r.json()

        for user in json_data:
            if user == username or 'users' in user:
                pass
            else:
                st.write(user)


except Exception as erro:
    set_style(True, True, True)

    st.title('😃 Que tal encontrar amigos e novas pessoas?')
    st.caption('Antes de encontrar pessoas, é preciso ter um nome!')

    if st.button(':material/login: Criar conta ou Entrar'):
        st.switch_page('pages/welcome.py')
