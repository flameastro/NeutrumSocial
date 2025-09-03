"""
Este arquivo é responsável por executar todo o projeto, conhecido como EXECUTADOR.
É ele quem cria as páginas e configura alguns estilos para cada página.
"""

import streamlit as st
import requests
import json


st.set_page_config(
    page_title="NeutrumSocial",
    page_icon="assets/image/icon.png",
    layout="wide"
)

st.markdown('''<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap" rel="stylesheet">
<style>
    #MainMenu, footer, .st-emotion-cache-1gwi02i {
        visibility: hidden;
    }

    * {
        font-family: "Space Grotesk", sans-serif;
    }

    .st-emotion-cache-1pru02b {
        font-size: 0.9em;
        font-weight: 900;
        color: grey;
    }

    .e16b601d6 {
        font-weight: 700;
        color: #d6d6d6;
    }

    .rc-overflow-item {
        padding: 5px;
    }

    span[data-testid="stIconMaterial"] {
        color: #add1ff;
    }
</style>
</head>''', unsafe_allow_html=True)


pages = {
    "🏠 Principal": [
        st.Page("pages/initial.py", title="Início", icon=":material/home:"),
        st.Page("pages/search.py", title="Pesquisar", icon=":material/search:"),
        st.Page("pages/create.py", title="Post", icon=":material/publish:")
    ],

    "💬 Chat": [

    ],

    "🌵 Outros": [
        st.Page("pages/person.py", title="Perfil", icon=":material/account_circle:"),
        st.Page("pages/settings.py", title="Configurações", icon=":material/settings:")
    ],
}

try:
    with open('./data/login.json', 'r', encoding="utf-8") as f: 
        pass
except:
    pages["🥏 Primeiros Passos"] = st.Page("pages/welcome.py", title="Bem-vindo", icon=":material/emoji_people:"),

### Chat
try:
    with open("./data/login.json", 'r', encoding="utf-8") as f:
        username = json.load(f)["user"]["username"]

    # Coletando os seguindo e os seguidores
    following = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/status/lista_following/.json").json()

    followers = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/status/lista_seguidores/.json").json()
    users = set()

    # Adicionando cada na lista (set)
    for following in following:
        users.add(following)

    for seguidor in followers:
        users.add(seguidor)

    users.remove("None")
    users = list(users)

    if len(users) == 0:
        pass
    else:
        # Criando os arquivos para cada seguindo/seguidor da lista.
        for user in users:
            try:
                with open(f"pages/friends/{user}.py", "r", encoding="utf-8") as f: 
                    pass
            except:
                with open(f"pages/friends/{user}.py", "w", encoding="utf-8") as f:
                    f.write(f'''import streamlit as st
import requests
import json

me = "{username}"
friend = "{user}"

letter = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/$me!/chat/$friend!/letra/.json").json()
main = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/$me!/chat/$friend!/main/.json").json()
sec = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/$me!/chat/$friend!/sec/.json").json()

with open("./data/login.json", "r", encoding="utf-8") as f:
    username = json.load(f)["user"]["username"]

messages = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/$me!/chat/$friend!/.json").json()
for key, message in messages.items():
    if message == "None" or (key == "letra" and message == "a") or (key == "letra" and message == "b") or (key == "main" and message == me) or (key == "main" and message == friend):
        pass
    else:

        if key[0] == "a":
            if me == main:
                with st.chat_message("user", avatar=":material/mood:"):
                    st.caption(f":green[$main!]")
                    st.write(message)
            else:
                with st.chat_message("user", avatar=":material/account_circle:"):
                    st.caption(f":blue[Eu $sec!]")
                    st.write(message)
        else:
            if me == main:
                with st.chat_message("user", avatar=":material/account_circle:"):
                    st.caption(f":blue[Eu $me!]")
                    st.write(message)
            else:
                with st.chat_message("user", avatar=":material/mood:"):
                    st.caption(f":green[Amigo $friend!]")
                    st.write(message)


send_message = st.chat_input("Digite sua mensagem")

if send_message:
    with st.spinner("Enviado Mensagem, aguarde..."):
        # Enviando a mensagem para o banco de dados
        r = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/$me!/chat/$friend!/.json").json()

        a_person = f"a$[sum(pessoa[0].count('a') for pessoa, _ in r.items() if pessoa[0] == 'a')][0] + 1!"
        b_person = f"b$[sum(pessoa[0].count('b') for pessoa, _ in r.items() if pessoa[0] == 'b')][0] + 1!"

        if letter == "a":
            data = $
                a_person: send_message
            !
        else:
            data = $
                b_person: send_message
            !

        r = requests.patch(f"https://neutrumsocial1-default-rtdb.firebaseio.com/$me!/chat/$friend!/.json", json=data)
        r = requests.patch(f"https://neutrumsocial1-default-rtdb.firebaseio.com/$friend!/chat/$me!/.json", json=data)

        st.rerun()
'''.replace("$", "{").replace("!", "}"))

            pages["💬 Chat"].append(st.Page(f"pages/friends/{user}.py", title=user, icon=":material/mood:"))

except:
    pass


pg = st.navigation(pages)
pg.run()
