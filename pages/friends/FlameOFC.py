import streamlit as st
import requests
import json

me = "Snowzinn"
friend = "FlameOFC"

letra = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{me}/chat/{friend}/letra/.json").json()
main = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{me}/chat/{friend}/main/.json").json()
sec = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{me}/chat/{friend}/sec/.json").json()

with open("./data/login.json", "r") as arquivo:
    username = json.load(arquivo)["user"]["username"]

mensagens = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{me}/chat/{friend}/.json").json()
for i, mensagem in mensagens.items():
    if mensagem == "None" or i == "letra" or i =="main" or i == "sec":
        pass
    else:

        if i[0] == "a":
            if me == main:
                with st.chat_message("user", avatar=":material/mood:"):
                    st.caption(f":green[{main}]")
                    st.write(mensagem)
            else:
                with st.chat_message("user", avatar=":material/account_circle:"):
                    st.caption(f":blue[Eu {sec}]")
                    st.write(mensagem)
        else:
            if me == main:
                with st.chat_message("user", avatar=":material/account_circle:"):
                    st.caption(f":blue[Eu {me}]")
                    st.write(mensagem)
            else:
                with st.chat_message("user", avatar=":material/mood:"):
                    st.caption(f":green[Amigo {friend}]")
                    st.write(mensagem)


enviar_mensagem = st.chat_input("Digite sua mensagem")

if enviar_mensagem:
    with st.spinner("Enviado Mensagem, aguarde..."):
        # Enviando a mensagem para o banco de dados
        r = requests.get(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{me}/chat/{friend}/.json").json()

        pessoa_a = f"a{[sum(pessoa[0].count('a') for pessoa, _ in r.items() if pessoa[0] == 'a')][0] + 1}"
        pessoa_b = f"b{[sum(pessoa[0].count('b') for pessoa, _ in r.items() if pessoa[0] == 'b')][0] + 1}"

        if letra == "a":
            data = {
                pessoa_a: enviar_mensagem
            }
        else:
            data = {
                pessoa_b: enviar_mensagem
            }

        r = requests.patch(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{me}/chat/{friend}/.json", json=data)
        r = requests.patch(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{friend}/chat/{me}/.json", json=data)

        st.rerun()
