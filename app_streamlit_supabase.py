
import streamlit as st
import psycopg2
from datetime import date, timedelta

# Conexão com Supabase (preencha com suas credenciais)
db_config = st.secrets["supabase"]

conn = psycopg2.connect(
    host=db_config["host"],
    database=db_config["database"],
    user=db_config["user"],
    password=db_config["password"],
    port=db_config["port"]
)
cursor = conn.cursor()

st.set_page_config(page_title="Controle de Mão de Obra", layout="centered")
st.title("📋 Controle de Mão de Obra - SOTREQ")

menu = st.sidebar.radio("Menu", ["📥 Registro de OM", "👤 Cadastro de Colaboradores"])

# --- REGISTRO DE OM ---
if menu == "📥 Registro de OM":
    # Buscar colaboradores
    cursor.execute("SELECT matricula, nome, funcao FROM colaboradores ORDER BY nome")
    colaboradores = cursor.fetchall()

    if not colaboradores:
        st.warning("⚠️ Nenhum colaborador cadastrado. Acesse o menu 'Cadastro de Colaboradores'.")
    else:
        colab_dict = {mat: (nome, funcao) for mat, nome, funcao in colaboradores}

        st.subheader("Registrar Ordem de Manutenção")

        with st.form("form_om"):
            matricula = st.selectbox("Matrícula", options=list(colab_dict.keys()))
            nome = colab_dict[matricula][0]
            funcao = colab_dict[matricula][1]

            st.text_input("Nome", value=nome, disabled=True)
            st.text_input("Função", value=funcao, disabled=True)

            frente = st.text_input("Frente")
            om = st.text_input("Número da OM")
            turno = st.selectbox("Turno", ["Manhã", "Tarde", "Noite"])
            descricao = st.text_area("Descrição do serviço", max_chars=500)
            data = st.date_input("Data", min_value=date.today() - timedelta(days=1), max_value=date.today(), value=date.today())

            enviar = st.form_submit_button("Registrar")

            if enviar:
                if not frente or not om or not descricao:
                    st.error("Preencha todos os campos obrigatórios.")
                elif not om.isdigit():
                    st.error("A OM deve conter apenas números.")
                else:
                    try:
                        cursor.execute("""
                            INSERT INTO alocacoes (colaborador, matricula, frente, om, turno, descricao, data)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (nome, matricula, frente, om, turno, descricao, data.strftime("%d/%m/%Y")))
                        conn.commit()
                        st.success("✅ Registro enviado com sucesso!")

# Formulário de cadastro

elif menu == "👤 Cadastro de Colaboradores":
    st.subheader("Cadastrar Novo Colaborador")

with st.form("form_colaborador"):
    funcao_colab = st.text_input("Função")
    nome_colab = st.text_input("Nome do colaborador")
    matricula_colab = st.text_input("Matrícula")
    enviar = st.form_submit_button("Cadastrar colaborador")

    if enviar:
        if not nome_colab or not matricula_colab or not funcao_colab:
            st.warning("Todos os campos são obrigatórios.")
        else:
            cursor.execute("SELECT * FROM colaboradores WHERE matricula = %s", (matricula_colab,))
            existe = cursor.fetchone()
            if existe:
                st.error("Já existe um colaborador com essa matrícula.")
            else:
                try:
                    cursor.execute("""
                    INSERT INTO colaboradores (nome, matricula, funcao)
                    VALUES (%s, %s, %s)
                """, (nome_colab, matricula_colab, funcao_colab))
                conn.commit()
                st.success("Colaborador cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar no banco: {e}")

# Exibir colaboradores cadastrados
st.markdown("### Colaboradores cadastrados")
cursor.execute("SELECT nome, matricula, funcao FROM colaboradores")
dados = cursor.fetchall()

if dados:
    import pandas as pd
    df_colab = pd.DataFrame(dados, columns=["Nome", "Matrícula", "Função"])
    st.dataframe(df_colab)
else:
    st.info("Nenhum colaborador cadastrado.")
