"""
Sistema de Coletor de Avaliações
Exemplo de demonstração com Flask

Funcionalidades:
- Link público para avaliações
- Dashboard administrativo
- Armazenamento em SQLite
- Gráficos e estatísticas básicas
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect('avaliacoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            nota INTEGER,
            categoria TEXT,
            comentario TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Função para conectar ao banco
def get_db():
    conn = sqlite3.connect('avaliacoes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página inicial - Link de avaliação
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema de Avaliações</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .btn { background: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px; }
            .btn:hover { background: #0056b3; }
            .admin-btn { background: #28a745; }
            .admin-btn:hover { background: #218838; }
            .center { text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 Sistema de Avaliações</h1>
            <div class="center">
                <p>Bem-vindo ao nosso sistema de coleta de avaliações!</p>
                <a href="/avaliar" class="btn">📝 Fazer Avaliação</a>
                <a href="/admin" class="btn admin-btn">📊 Dashboard Admin</a>
            </div>
        </div>
    </body>
    </html>
    '''

# Formulário de avaliação
@app.route('/avaliar', methods=['GET', 'POST'])
def avaliar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        nota = int(request.form['nota'])
        categoria = request.form['categoria']
        comentario = request.form['comentario']

        # Salvar no banco
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO avaliacoes (nome, email, nota, categoria, comentario)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, nota, categoria, comentario))
        conn.commit()
        conn.close()

        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Avaliação Enviada</title>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
                .success { color: #28a745; font-size: 24px; margin: 20px 0; }
                .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success">✅ Avaliação enviada com sucesso!</div>
                <p>Obrigado pelo seu feedback!</p>
                <a href="/" class="btn">Voltar ao início</a>
            </div>
        </body>
        </html>
        '''

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fazer Avaliação</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .form-group { margin: 20px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { background: #28a745; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; width: 100%; }
            button:hover { background: #218838; }
            .stars { font-size: 24px; }
            .star { color: #ddd; cursor: pointer; }
            .star.active { color: #ffc107; }
        </style>
        <script>
            function setRating(rating) {
                document.getElementById('nota').value = rating;
                for(let i = 1; i <= 5; i++) {
                    const star = document.getElementById('star' + i);
                    if(i <= rating) {
                        star.classList.add('active');
                    } else {
                        star.classList.remove('active');
                    }
                }
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>📝 Fazer Avaliação</h1>
            <form method="POST">
                <div class="form-group">
                    <label>Nome:</label>
                    <input type="text" name="nome" required>
                </div>

                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" name="email" required>
                </div>

                <div class="form-group">
                    <label>Nota (1-5 estrelas):</label>
                    <div class="stars">
                        <span class="star" id="star1" onclick="setRating(1)">⭐</span>
                        <span class="star" id="star2" onclick="setRating(2)">⭐</span>
                        <span class="star" id="star3" onclick="setRating(3)">⭐</span>
                        <span class="star" id="star4" onclick="setRating(4)">⭐</span>
                        <span class="star" id="star5" onclick="setRating(5)">⭐</span>
                    </div>
                    <input type="hidden" name="nota" id="nota" required>
                </div>

                <div class="form-group">
                    <label>Categoria:</label>
                    <select name="categoria" required>
                        <option value="">Selecione...</option>
                        <option value="Atendimento">Atendimento</option>
                        <option value="Produto">Produto</option>
                        <option value="Entrega">Entrega</option>
                        <option value="Preço">Preço</option>
                        <option value="Geral">Geral</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Comentário:</label>
                    <textarea name="comentario" rows="4" placeholder="Deixe seu comentário aqui..."></textarea>
                </div>

                <button type="submit">Enviar Avaliação</button>
            </form>
        </div>
    </body>
    </html>
    '''

# Dashboard administrativo
@app.route('/admin')
def admin():
    conn = get_db()
    cursor = conn.cursor()

    # Buscar todas as avaliações
    cursor.execute('SELECT * FROM avaliacoes ORDER BY data_criacao DESC')
    avaliacoes = cursor.fetchall()

    # Calcular estatísticas
    cursor.execute('SELECT AVG(nota) as media FROM avaliacoes')
    media = cursor.fetchone()['media'] or 0

    cursor.execute('SELECT COUNT(*) as total FROM avaliacoes')
    total = cursor.fetchone()['total']

    # Distribuição por nota
    cursor.execute('SELECT nota, COUNT(*) as quantidade FROM avaliacoes GROUP BY nota')
    dist_notas = cursor.fetchall()

    # Distribuição por categoria
    cursor.execute('SELECT categoria, COUNT(*) as quantidade FROM avaliacoes GROUP BY categoria')
    dist_categorias = cursor.fetchall()

    conn.close()

    # Preparar dados para gráficos
    notas_data = {str(row['nota']): row['quantidade'] for row in dist_notas}
    categorias_data = {row['categoria']: row['quantidade'] for row in dist_categorias}

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Avaliações</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ color: #333; text-align: center; }}
            .stats {{ display: flex; gap: 20px; margin: 30px 0; }}
            .stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); flex: 1; text-align: center; }}
            .stat-number {{ font-size: 36px; font-weight: bold; color: #007bff; }}
            .stat-label {{ font-size: 14px; color: #666; }}
            .avaliacoes {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 20px 0; }}
            .avaliacao {{ border-bottom: 1px solid #eee; padding: 15px 0; }}
            .avaliacao:last-child {{ border-bottom: none; }}
            .avaliacao-header {{ display: flex; justify-content: between; align-items: center; margin-bottom: 10px; }}
            .nome {{ font-weight: bold; }}
            .data {{ color: #666; font-size: 12px; }}
            .nota {{ color: #ffc107; }}
            .categoria {{ background: #e9ecef; padding: 2px 8px; border-radius: 12px; font-size: 12px; }}
            .comentario {{ margin-top: 10px; font-style: italic; }}
            .charts {{ display: flex; gap: 20px; margin: 30px 0; }}
            .chart {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); flex: 1; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Dashboard de Avaliações</h1>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total}</div>
                    <div class="stat-label">Total de Avaliações</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{media:.1f}</div>
                    <div class="stat-label">Nota Média</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{'⭐' * int(media)}</div>
                    <div class="stat-label">Classificação</div>
                </div>
            </div>

            <div class="charts">
                <div class="chart">
                    <h3>Distribuição por Nota</h3>
                    {_generate_chart_html("notas", notas_data)}
                </div>
                <div class="chart">
                    <h3>Distribuição por Categoria</h3>
                    {_generate_chart_html("categorias", categorias_data)}
                </div>
            </div>

            <div class="avaliacoes">
                <h3>Avaliações Recentes</h3>
                {_generate_avaliacoes_html(avaliacoes)}
            </div>

            <div style="text-align: center; margin: 30px 0;">
                <a href="/" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Voltar ao Início</a>
            </div>
        </div>
    </body>
    </html>
    '''

def _generate_chart_html(tipo, data):
    if not data:
        return "<p>Nenhum dado disponível</p>"

    html = "<div style='margin: 20px 0;'>"
    max_val = max(data.values()) if data else 1

    for key, value in data.items():
        percentage = (value / max_val) * 100
        html += f"""
        <div style='margin: 10px 0;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                <span>{key}</span>
                <span>{value}</span>
            </div>
            <div style='background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden;'>
                <div style='background: #007bff; height: 100%; width: {percentage}%; transition: width 0.3s;'></div>
            </div>
        </div>
        """

    html += "</div>"
    return html

def _generate_avaliacoes_html(avaliacoes):
    if not avaliacoes:
        return "<p>Nenhuma avaliação encontrada.</p>"

    html = ""
    for av in avaliacoes[:10]:  # Mostrar apenas as 10 mais recentes
        stars = "⭐" * av['nota']
        html += f"""
        <div class="avaliacao">
            <div class="avaliacao-header">
                <span class="nome">{av['nome']}</span>
                <span class="categoria">{av['categoria']}</span>
                <span class="data">{av['data_criacao']}</span>
            </div>
            <div class="nota">{stars} ({av['nota']}/5)</div>
            {f'<div class="comentario">"{av["comentario"]}"</div>' if av['comentario'] else ''}
        </div>
        """

    return html

# API para dados em JSON (opcional)
@app.route('/api/avaliacoes')
def api_avaliacoes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM avaliacoes ORDER BY data_criacao DESC LIMIT 50')
    avaliacoes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(avaliacoes)

if __name__ == '__main__':
    init_db()
    print("🚀 Sistema de Avaliações iniciado!")
    print("📝 Link público: http://localhost:5000/avaliar")
    print("📊 Dashboard admin: http://localhost:5000/admin")
    app.run(debug=True, host='0.0.0.0', port=5000)
