"""
Este arquivo realiza a parte da criação de posts.
Aqui o usuário coloca o título, a descrição, a imagem e clica no botão de enviar, e o arquivo envia estes dados paara o banco de dados
"""

import streamlit as st
from assets.css.no_login_centralized import set_style
from datetime import datetime
import json
import requests

try:
    st.caption("Arrase criando posts chamativos para atrair mais seguidores! 🌠")
    image_error = False # Define se a imagem falhou no carregamento/url não existe

    with open('./data/login.json', 'r', encoding="utf-8") as f:
        username = json.load(f)
        username = username["user"]["username"]

    DATABASE = f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/posts/.json"


    with st.container(border=True):

        title = st.text_input("Digite o título do Post", placeholder="Título")
        description = st.text_area("Digite a descrição do post", placeholder="Descrição")

        date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        st.caption(date)

        category = st.multiselect(":material/category: Categorias", options=["🌀 ToDo", "🤖 Robótica", "🪐 Física", "🌎 Cultura", "📚 Estudo", "🤣 Comédia", "💸 Economia", "🎮 Games", "🌝 Curiosidade",  "🧠 Genialidade", "🔴 Outros"])


        with st.empty():
            image_text = st.text_input(":material/content_copy: Imagem", placeholder="Copie o endereço de uma imagem da internet e cole aqui")

            if image_text:
                try:
                    image = st.image(image_text, width=300)
                except:
                    image_error = True
                    st.error("Não foi possível encontrar esta imagem")


        submit = st.button("Enviar")
        if submit:
            if title == "" or description == "" or category == []:
                st.warning(":material/warning: Preencha todos os campos")
            else:

                # Deleta o "0": "0" do posts padrão
                try: r = requests.delete(f"https://neutrumsocial1-default-rtdb.firebaseio.com/{username}/posts/0/.json")
                except: pass


                data = {
                    title: {
                        "descrição": description,
                        "data": date,
                        "categoria": category,
                    }
                }

                if image_error:
                    pass
                else:
                    data[title]["imagem"] = image_text

                r = requests.patch(DATABASE, json=data)

        try:
            with st.expander("Meus posts"):
                r = requests.get(DATABASE)
                json_data = r.json() or {}

                for title, post in json_data.items():
                    if not isinstance(post, dict):
                        continue  # Ignora entradas inválidas

                    st.markdown(f"### {title}")
                    st.write("🗓️", post.get("data", "—"))
                    st.write("📝", post.get("descrição", "—"))

                    categories = post.get("categoria", [])
                    if isinstance(categories, list) and categories:
                        st.write("🏷️", ", ".join(categories))
                    else:
                        st.write("🏷️ Sem categoria")

                    img_url = post.get("image")
                    if img_url:
                        try:
                            st.image(img_url, width=300)
                        except:
                            st.error("Não foi possível carregar esta imagem")

                    st.markdown("---")
        except:
            st.info("Você não tem nenhum post")

except:
    set_style(True, True, True)

    st.title('🌟 Vamos criar conteúdo e ganhar fama!')
    st.caption('Crie conteúdos únicos e com criativdade!')

    if st.button(':material/login: Criar conta ou Entrar'):
        st.switch_page('pages/welcome.py')
