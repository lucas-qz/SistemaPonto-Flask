from flask import Flask,render_template,redirect,url_for,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import generate_password_hash,check_password_hash
from sqlalchemy.sql import text

from datetime import datetime, timezone
import pytz
app = Flask(__name__)
app.secret_key = 'MdMprJSp3G08W1cHMEzAazx8Uw3CAAlG7SYFr1PEa36mauqUTRTsFI0G6psEuyx1'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '',
        servidor = 'db',
        database = 'banco1'
    )

"""
#--- CONEXÃO COM SQLITE LOCAL ---------    
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testDb.db'
#--- CONEXÃO COM SQLITE LOCAL ---------  
"""

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Usuario(db.Model):  
    id_usuario = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    nome_usuario = db.Column(db.String(50), nullable = False)  
    login_usuario = db.Column(db.String(20), nullable = False, unique=True) 
    senha_usuario = db.Column(db.String(255), nullable = False) 
    def __repr__(self):
        return '<Name %r>' %self.name 

class Marcacao(db.Model):     
    id_hr= db.Column(db.Integer, primary_key = True, autoincrement = True) 
    data = db.Column(db.DateTime(50), nullable = False)
    dia = db.Column(db.String(50), nullable = False)
    mes = db.Column(db.String(50), nullable = False)
    ano = db.Column(db.String(50), nullable = False)        
    hora = db.Column(db.String(50), nullable = False)
    st = db.Column(db.String(2), nullable = False)
    id_usuario = db.Column(db.Integer, nullable = False) 
    def __repr__(self):
        return '<hr %r>' %self.hr 
 
@app.route('/testdb')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/cadastro_usuario')
def cadastro_usuario(): 
    return render_template('cadastro_usuario.html') 

@app.route('/validar_usuario',methods=['POST',])
def validar_usuario():
    nome = request.form['nome']
    login = request.form['login']
    senha = generate_password_hash( request.form['senha']).decode('utf-8') 
    cadastro = Usuario.query.filter_by(login_usuario = login).first() 
    if cadastro:
        flash('Atenção: Usuario indisponível!','atencao')
        return redirect(url_for('cadastro_usuario'))
    novo_usuario = Usuario(nome_usuario = nome, login_usuario = login, senha_usuario = senha)
    db.session.add(novo_usuario)
    db.session.commit()
    flash(f'Usuário(a) {novo_usuario.nome_usuario} cadastrado(a) com sucesso!','sucesso') 
    return redirect(url_for('pagina_login'))

@app.route('/recireciona') 
def recireciona():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:   
        return redirect(url_for('pagina_login'))     
    usuario = Usuario.query.filter_by(login_usuario = session['usuario_logado']).first()
    dataSPX = datetime.now(timezone.utc).astimezone(pytz.timezone('America/Sao_Paulo')).isoformat().replace('-03:00', '').replace('T', ' ')    
    dia = dataSPX[8:10] 
    mes = dataSPX[5:7]
    ano = dataSPX[0:4]
    hora = dataSPX[11:19]
    x =datetime.strptime(f'{ano}-{mes}-{dia} {dataSPX[11:13]}:{dataSPX[14:16]}:{dataSPX[17:19]}', '%Y-%m-%d %H:%M:%S')

    qnt =  Marcacao.query.filter_by( dia=dia, mes=mes, ano=ano, id_usuario = usuario.id_usuario).count()
    if qnt < 4:
        if qnt == 0:
            nova_marcacao = Marcacao( data=x, dia=dia, mes=mes, ano=ano, hora=hora, id_usuario=usuario.id_usuario,st='E1')
        if qnt == 1:
            nova_marcacao = Marcacao( data=x, dia=dia, mes=mes, ano=ano, hora=hora, id_usuario=usuario.id_usuario,st='S1')
        if qnt == 2:
            nova_marcacao = Marcacao( data=x, dia=dia, mes=mes, ano=ano, hora=hora, id_usuario=usuario.id_usuario,st='E2')
        if qnt == 3:
            nova_marcacao = Marcacao( data=x, dia=dia, mes=mes, ano=ano, hora=hora, id_usuario=usuario.id_usuario,st='S2')
        db.session.add(nova_marcacao)
        db.session.commit()                                     
        flash('Registro de Ponto realizado com Sucesso','sucesso')
        return redirect(url_for('marca')) 
    else:
        flash('Não pode realizar mais de 4 marcações no dia. Procure o RH!','atencao')
        return redirect(url_for('marca')) 

@app.route('/')
def pagina_login():  
    return render_template('pagina_login.html')

@app.route('/validar_login',methods=['POST',])
def validar_login():
    usuario = Usuario.query.filter_by(login_usuario = request.form['login']).first()
    if usuario:
        senha = check_password_hash(usuario.senha_usuario, request.form['senha'])
        if usuario and senha:
            session['usuario_logado'] = request.form['login']
            flash(f'Usuário {usuario.nome_usuario} logado com sucesso!','sucesso') 
            return redirect(url_for('marca'))
        else:
            flash('Usuário e/ou senha inválidos!','atencao')
            return redirect(url_for('pagina_login'))
    else:
        flash('Usuário e/ou senha inválidos!','atencao')
        return redirect(url_for('pagina_login'))

@app.route('/sair')
def sair():
    session['usuario_logado'] = None 
    return redirect(url_for('pagina_login'))

@app.route('/marca')
def marca():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:   
        return redirect(url_for('pagina_login')) 
    usuario = Usuario.query.filter_by(login_usuario = session['usuario_logado']).first()
    dataSPX = datetime.now(timezone.utc).astimezone(pytz.timezone('America/Sao_Paulo')).isoformat().replace('-03:00', '').replace('T', ' ')    
    dia = dataSPX[8:10] 
    mes = dataSPX[5:7]
    ano = dataSPX[0:4]
    marcacoes = Marcacao.query.filter_by( dia=dia, mes=mes, ano=ano, id_usuario=usuario.id_usuario).order_by(Marcacao.data.desc()) 
    return render_template('marca.html',marcacoes=marcacoes,usuario=usuario) 

@app.route('/espelho')
def espelho(): 
    if session['usuario_logado'] == None or 'usuario_logado' not in session:   
        return redirect(url_for('pagina_login')) 
    dataSPX = datetime.now(timezone.utc).astimezone(pytz.timezone('America/Sao_Paulo')).isoformat().replace('-03:00', '').replace('T', ' ')    
    data = f'{dataSPX[8:10]}/{dataSPX[5:7]}/{dataSPX[0:4]}' 
    usuario = Usuario.query.filter_by(login_usuario = session['usuario_logado']).first()
    marcacoes = Marcacao.query.filter_by(id_usuario = usuario.id_usuario).order_by(Marcacao.data.desc()) 
    return render_template('espelho.html',marcacoes=marcacoes,usuario=usuario, data=data) 

@app.route('/dashboard')
def dashboard():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:   
        return redirect(url_for('pagina_login'))  
    dataSPX = datetime.now(timezone.utc).astimezone(pytz.timezone('America/Sao_Paulo')).isoformat().replace('-03:00', '').replace('T', ' ')    
    dia = dataSPX[8:10] 
    mes = dataSPX[5:7]
    ano = dataSPX[0:4]
    usuario = Usuario.query.filter_by(login_usuario = session['usuario_logado']).first()
    hj =  Marcacao.query.filter_by( dia=dia, mes=mes, ano=ano, id_usuario = usuario.id_usuario).count()
    ms = Marcacao.query.filter_by( mes=mes, ano=ano, id_usuario = usuario.id_usuario).count()
    ano = Marcacao.query.filter_by( ano=ano, id_usuario = usuario.id_usuario).count()
    total = Marcacao.query.filter_by( id_usuario = usuario.id_usuario).count()  
    return render_template('dashboard.html',usuario=usuario,hj=hj,mes=ms,ano=ano,total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port="5000")

