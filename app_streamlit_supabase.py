
import streamlit as st
import psycopg2
from datetime import date, timedelta


#cd "C:\Users\Felipe\Documents\01. Projetos\01. Programação\Controle_MO"
#venv\Scripts\activate
#streamlit run app_streamlit_supabase.py

# Conexão com Supabase (preencha com suas credenciais)
conn = psycopg2.connect(
    host="aws-0-sa-east-1.pooler.supabase.com",
    database="postgres",
    user="postgres.dvigdrcdmnxpnhflkqzs",
    password="*10junPEOVl3@",
    port=6543
)
cursor = conn.cursor()

st.title("Registro de Ordem de Manutenção")

# Formulário
nome = st.text_input("Nome do colaborador")
matricula = st.text_input("Matrícula")
frente = st.text_input("Frente")
om = st.text_input("Número da OM")
turno = st.selectbox("Turno", ["Manhã", "Tarde", "Noite"])
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
