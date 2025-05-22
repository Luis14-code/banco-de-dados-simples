import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="matricula",
        user="postgres",
        password="luis14"
    )

def adicionar_aluno(cursor):
    nome = input("Nome do aluno: ")
    numero = input("Número do aluno: ")
    email = input("Email do aluno: ")
    cpf = input("CPF do aluno: ")
    id_aluno = int(input("ID do aluno: "))
    cidade = input("Cidade do aluno: ")

    comando = """
        INSERT INTO aluno (nome, numero, email, cpf, id_aluno, cidade)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(comando, (nome, numero, email, cpf, id_aluno, cidade))
    return id_aluno

def adicionar_curso_professor(cursor):
    id_curso = int(input("ID do curso: "))
    nome_curso = input("Nome do curso: ")
    email_professor = input("Email do professor: ")
    cidade_professor = input("Cidade do professor: ")
    id_professor = int(input("ID do professor: "))
    nome_professor = input("Nome do professor: ")
    cpf_professor = input("CPF do professor: ")
    numero_professor = input("Número do professor: ")

    comando = """
        INSERT INTO curso_professor_ (
            id_curso, nome_curso, email_professor, cidade_professor,
            id_professor, nome_professor, cpf_professor, numero_professor
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(comando, (
        id_curso, nome_curso, email_professor, cidade_professor,
        id_professor, nome_professor, cpf_professor, numero_professor
    ))
    return id_curso, id_professor

def associar_aluno_curso(cursor, id_aluno, id_curso, id_professor):
    comando = """
        INSERT INTO curso_aluno (
            fk_aluno_id_aluno, fk_curso_professor__id_curso, fk_curso_professor__id_professor
        ) VALUES (%s, %s, %s)
    """
    cursor.execute(comando, (id_aluno, id_curso, id_professor))

def main():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        id_aluno = adicionar_aluno(cursor)
        id_curso, id_professor = adicionar_curso_professor(cursor)
        associar_aluno_curso(cursor, id_aluno, id_curso, id_professor)

        conexao.commit()
        print("Dados inseridos com sucesso!")

    except Exception as e:
        print(f"Erro: {e}")
        if conexao:
            conexao.rollback()

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

if __name__ == "__main__":
    main()
