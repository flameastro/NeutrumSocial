"""
Este arquivo mostra todos os posts (sem ser os seus próprios) na página.
"""

import streamlit as st
from assets.css.no_login_centralized import set_style
import json
import requests

try:
    st.caption("Explore os posts do momento, veja o que está rolando!")

    st.divider()

    with open('./data/login.json', 'r', encoding="utf-8") as f:
        username = json.load(f)
        username = username["user"]["username"]

    r = requests.get("https://neutrumsocial1-default-rtdb.firebaseio.com/.json")
    json_data = r.json()

    for user in json_data:
        if 'users' == user or username == user: pass
        else:
            DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{user}/posts.json"
            r = requests.get(DATABASE)
            json_data = r.json()

            if json_data == ['0']: pass
            else:
                categories = []
                for key, value in json_data.items():
                    with st.container(border=True):
                        st.write(user)
                        st.write(f"## **{key}**")
                        for key2, value2 in value.items():
                            if key2 == 'data':
                                st.write(f"📆 {value2}")
                            elif key2 == "categoria":
                                for category in value2:
                                    categories.append(category)
                                st.write(f"🏷️: {", ".join(categories)}")
                            elif key2 == "descrição":
                                st.write(f"📃 {value2}")
                            elif key2 == "imagem":
                                try:
                                    st.image(value2, width=300)
                                except:
                                    st.caption(f"[*Não foi possível carregar a imagem*]({value2})")

                st.divider()

except:
    set_style(True, True, True)

    st.title('🚀 Quer começar a sua jornada?')
    st.caption('Para pilotar sua nave, vamos nos conectar!')

    if st.button(':material/login: Criar conta ou Entrar'):
        st.switch_page('pages/welcome.py')
