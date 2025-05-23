from flask import Flask, render_template, request, redirect, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "chave_secreta"  # Importante para flash

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="matricula",
        user="postgres",
        password="luis14"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = None
        cursor = None
        try:
            # Pegando os dados do form
            nome = request.form.get('nome')
            numero = request.form.get('numero')
            email = request.form.get('email')
            cpf = request.form.get('cpf')
            id_aluno = int(request.form.get('id_aluno'))
            cidade = request.form.get('cidade')

            id_curso = int(request.form.get('id_curso'))
            nome_curso = request.form.get('nome_curso')
            email_professor = request.form.get('email_professor')
            cidade_professor = request.form.get('cidade_professor')
            id_professor = int(request.form.get('id_professor'))
            nome_professor = request.form.get('nome_professor')
            cpf_professor = request.form.get('cpf_professor')
            numero_professor = request.form.get('numero_professor')

            print("Dados recebidos:", nome, numero, email, cpf, id_aluno, cidade)
            print("Curso e professor:", id_curso, nome_curso, email_professor, cidade_professor,
                  id_professor, nome_professor, cpf_professor, numero_professor)

            conn = conectar()
            cursor = conn.cursor()

            # Inserir aluno
            cursor.execute("""
                INSERT INTO aluno (nome, numero, email, cpf, id_aluno, cidade)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nome, numero, email, cpf, id_aluno, cidade))

            # Inserir curso e professor - usando nomes consistentes com formulário
            cursor.execute("""
                INSERT INTO curso_professor_ (
                    id_curso, nome_curso, email_professor, cidade_professor,
                    id_professor, nome_professor, cpf_professor, numero_professor
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_curso, nome_curso, email_professor, cidade_professor,
                id_professor, nome_professor, cpf_professor, numero_professor
            ))

            # Associar aluno ao curso
            cursor.execute("""
                INSERT INTO curso_aluno (
                    fk_aluno_id_aluno,
                    fk_id_curso,
                    fk_id_professor
                ) VALUES (%s, %s, %s)
            """, (id_aluno, id_curso, id_professor))

            conn.commit()
            flash("Dados inseridos com sucesso!", "success")
            print("Dados inseridos com sucesso!")

        except Exception as e:
            print("Erro ao inserir dados:", e)
            if conn:
                conn.rollback()
            flash(f"Erro ao inserir: {e}", "danger")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return redirect('/')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
