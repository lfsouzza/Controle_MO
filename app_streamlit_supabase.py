
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

st.title("Relatório Diário de Serviços")

# Formulário
nome = st.text_input("Nome do colaborador")
matricula = st.text_input("Matrícula")
frente = st.text_input("Frota")
om = st.text_input("Número da OM")
turno = st.selectbox("Turno", ["A", "B", "C","D","ADM"])
descricao = st.text_area("Descrição do serviço (máx 500 caracteres)", max_chars=500)
data = st.date_input("Data", min_value=date.today() - timedelta(days=1), max_value=date.today(), value=date.today())

if st.button("Registrar"):
    if not om.isdigit():
        st.error("OM deve conter apenas números")
    elif not nome or not matricula or not frente or not descricao:
        st.error("Todos os campos são obrigatórios")
    else:
        try:
            cursor.execute("""
                INSERT INTO alocacoes (colaborador, matricula, frente, om, turno, descricao, data)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nome, matricula, frente, om, turno, descricao, data))
            conn.commit()
            st.success("Registro enviado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

st.markdown("---")
st.subheader("Cadastro de Colaboradores")

# Formulário de cadastro
with st.form("form_colaborador"):
    nome_colab = st.text_input("Nome do colaborador")
    matricula_colab = st.text_input("Matrícula")
    frente_colab = st.text_input("Frente")
    funcao_colab = st.text_input("Função")
    enviar = st.form_submit_button("Cadastrar colaborador")

    if enviar:
        if not nome_colab or not matricula_colab or not frente_colab or not funcao_colab:
            st.warning("Todos os campos são obrigatórios.")
        else:
            cursor.execute("SELECT * FROM colaboradores WHERE matricula = %s", (matricula_colab,))
            existe = cursor.fetchone()
            if existe:
                st.error("Já existe um colaborador com essa matrícula.")
            else:
                cursor.execute("""
                    INSERT INTO colaboradores (nome, matricula, frente, funcao)
                    VALUES (%s, %s, %s, %s)
                """, (nome_colab, matricula_colab, frente_colab, funcao_colab))
                conn.commit()
                st.success("Colaborador cadastrado com sucesso!")

# Exibir colaboradores cadastrados
st.markdown("### Colaboradores cadastrados")
cursor.execute("SELECT nome, matricula, frente, funcao FROM colaboradores")
dados = cursor.fetchall()

if dados:
    import pandas as pd
    df_colab = pd.DataFrame(dados, columns=["Nome", "Matrícula", "Frente", "Função"])
    st.dataframe(df_colab)
else:
    st.info("Nenhum colaborador cadastrado.")
