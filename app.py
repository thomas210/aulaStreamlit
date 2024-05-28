import pandas as pd
import streamlit as st
import random

# Funções CRUD
def load_data():
    try:
        df = pd.read_csv('alunos.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['cpf', 'nome', 'media'])
    return df

def save_data(df):
    df.to_csv('alunos.csv', index=False)

def create(df, nome, cpf, media):
    if cpf in df['cpf'].values:
        return -3

    new_entry = pd.DataFrame({'cpf': [cpf], 'nome': [nome], 'media': [media]})
    df = pd.concat([df, new_entry], ignore_index=True)
    save_data(df)
    return -1

def read(df, cpf):
    aluno = df[df['cpf'] == cpf]
    if aluno.empty:
        return -2
    return aluno.index[0]

def update(df, nome, cpf):
    indice_aluno = read(df, cpf)
    if indice_aluno == -2:
        return -2

    df.at[indice_aluno, 'nome'] = nome
    save_data(df)
    return -1

def delete(df, cpf):
    indice_aluno = read(df, cpf)
    if indice_aluno == -2:
        return -2

    df = df.drop(indice_aluno).reset_index(drop=True)
    save_data(df)
    return -1

# Função principal com Streamlit
def main():
    st.title("Faculdade Nova Roma")
    df = load_data()

    menu = ["Criar Aluno", "Buscar Aluno", "Atualizar Aluno", "Remover Aluno", "Listar Tudo", "Sair"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Criar Aluno":
        st.subheader("Criar Aluno")
        nome = st.text_input("Nome do aluno")
        cpf = st.text_input("CPF do aluno")
        media = st.number_input("Média do aluno", min_value=0, max_value=10, step=1)

        if st.button("Criar"):
            resultado = create(df, nome, cpf, media)
            if resultado == -3:
                st.error("Não posso criar pois o CPF já está cadastrado")
            elif resultado == -1:
                st.success("Aluno cadastrado com sucesso")
            else:
                st.error("Aconteceu algo que não esperada")

    elif choice == "Buscar Aluno":
        st.subheader("Buscar Aluno")
        cpf = st.text_input("CPF do aluno")

        if st.button("Buscar"):
            indice = read(df, cpf)
            if indice != -2:
                aluno = df.iloc[indice]
                st.write(f"CPF: {aluno['cpf']}")
                st.write(f"Nome: {aluno['nome']}")
                st.write(f"Média: {aluno['media']}")
            else:
                st.error("Aluno não encontrado")

    elif choice == "Atualizar Aluno":
        st.subheader("Atualizar Aluno")
        cpf = st.text_input("CPF do aluno")
        nome = st.text_input("Novo nome do aluno")

        if st.button("Atualizar"):
            resultado = update(df, nome, cpf)
            if resultado == -1:
                st.success("Aluno atualizado com sucesso")
            elif resultado == -2:
                st.error("Aluno não encontrado, não é possível atualizar")
            else:
                st.error("Deu alguma coisa aí, peça ajuda")

    elif choice == "Remover Aluno":
        st.subheader("Remover Aluno")
        cpf = st.text_input("CPF do aluno")

        if st.button("Remover"):
            resultado = delete(df, cpf)
            if resultado == -1:
                st.success("Aluno removido com sucesso")
            elif resultado == -2:
                st.error("Aluno não encontrado")
            else:
                st.error("Deu merda aí viss")

    elif choice == "Listar Tudo":
        st.subheader("Todos os Alunos Cadastrados")
        st.dataframe(df)

    elif choice == "Sair":
        st.write("Saindo...")
        st.stop()

if __name__ == "__main__":
    main()
