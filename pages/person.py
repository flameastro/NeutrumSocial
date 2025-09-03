"""
Este arquivo é responsável por configurar suas informações, como nome, sobrenome, descrição, data de nascimento.
Estes dados são todos enviados pelo banco de dados da firebase.
"""

import streamlit as st
import requests
import json
from assets.css.no_login_centralized import set_style

st.markdown('''
<style>
    h4#nome-de-usuario, h4#senha, h4#nome, h4#sobrenome, h4#meu-perfil {
        margin: 0;
        padding: 0;
    }

    button[data-testid="stPopoverButton"] {
        margin: 10px 0}
</style>
''', unsafe_allow_html=True)

try:
    set_style(False, False, True)
    with open('./data/login.json', 'r', encoding="utf-8") as f:
        pass

    with st.container(border=True):
        st.title('Meu Perfil')

        col1, col2 = st.columns([1, 1])

        with col1:
            st.write('#### Nome de usuário')
            with open('./data/login.json', 'r', encoding="utf-8") as f:
                username = json.load(f)
                username = username["user"]["username"]
            st.caption(username)

            st.write('#### Senha')
            with open('./data/login.json', 'r', encoding="utf-8") as f:
                password = json.load(f)
                password = password["user"]["password"]
            with st.popover("Revelar", icon='👀'):
                st.caption(password)

            st.write("#### Nome")
            try: 
                with open('./data/user-name.json', 'r', encoding="utf-8") as f: 
                    name = json.load(f)
                st.caption(name["nome"])
            except:
                with st.empty():
                    name = st.text_input("Coloque seu nome").title()

                    if name:
                        data = {
                            "nome": name
                        }

                        with open('./data/user-name.json', 'w', encoding="utf-8") as f:
                            json.dump(data, f, indent=4)
                        st.caption(name)

                        DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/.json"

                        r = requests.patch(DATABASE, json=data)
                        json_data = r.json()


            st.write("#### Sobrenome")
            try:
                with open('./data/user-lastname.json', 'r', encoding="utf-8") as f: 
                    lastname = json.load(f)
                st.caption(lastname["sobrenome"])
            except:
                with st.empty():
                    lastname = st.text_input("Coloque seu sobrenome").title()

                    if lastname:

                        data = {
                            "sobrenome": lastname
                        }

                        with open('./data/user-lastname.json', 'w', encoding="utf-8") as f:
                            json.dump(data, f, indent=4)
                        st.caption(lastname.title())

                        DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/.json"

                        r = requests.patch(DATABASE, json=data)
                        json_data = r.json()


            st.write("#### Data de Nascimento")
            try:
                with open('./data/user-birth.json', 'r', encoding="utf-8") as f: 
                    birth = json.load(f)
                st.caption(birth["nascimento"])
            except:
                with st.empty():
                    birth = st.date_input("Coloque sua data de Nascimento (AAAA/MM/DD)", min_value="1900-01-01")

                    if birth != birth.today():
                        birth = str(birth)

                        data = {
                            "nascimento": birth
                        }

                        with open('./data/user-birth.json', 'w', encoding="utf-8") as f:
                            json.dump(data, f, indent=4)
                        st.caption(birth)

                        DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/.json"

                        r = requests.patch(DATABASE, json=data)
                        json_data = r.json()


            st.write("#### Descrição")
            try:
                with open('./data/user-description.json', 'r', encoding="utf-8") as f: 
                    description = json.load(f)
                st.caption(description["descrição"])
            except:
                with st.empty():
                    description = st.text_input("Coloque sua descrição")

                    if description:

                        data = {
                            "descrição": description
                        }

                        with open('./data/user-description.json', 'w', encoding="utf-8") as f:
                            json.dump(data, f, indent=4)
                        st.caption(description)

                        DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/.json"

                        r = requests.patch(DATABASE, json=data)
                        json_data = r.json()


        with col2:
            try:
                if open(f'./data/user-image.png'):
                    st.image(f'./data/user-image.png', width=200, caption="Foto de Perfil")
            except:
                with st.empty():
                    image = st.file_uploader("Imagem", type=["png"], accept_multiple_files=False)

                    if image:
                        st.image(image, width=200, caption="Foto de Perfil")

                        try: open(f"./data/user-image.png", "x").close()
                        except: pass

                        with open("./data/user-image.png", 'wb') as f:
                            f.write(image.read())

            DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/status/seguidores/.json"

            r = requests.get(DATABASE)
            followers = r.json()

            st.write(f"#### Seguidores")
            st.caption(str(followers))


            DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/status/seguindo/.json"

            r = requests.get(DATABASE)
            following = r.json()

            st.write(f"#### Seguindo")
            st.caption(str(following))

            st.write("#### Posts")
            DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/posts/.json"

            r = requests.get(DATABASE)
            posts = r.json()

            quantidade = 0
            if posts == ['0']:
                st.caption("0")
            else:
                for post in posts:
                    quantidade += 1
                st.caption(str(quantidade))

except Exception as error:
    set_style(True, True, True)

    st.title('🌞 Vamos deixar nosso perfil bonito!')
    st.caption('Que tal decorar o perfil com descrição e informações pessoais?')

    if st.button(':material/login: Criar conta ou Entrar'):
        st.switch_page('pages/welcome.py')
