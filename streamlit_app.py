import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Gazelas Bet 2026", layout="centered")
DB_NAME = "bolao_oficial.db"

# --- 🔐 CREDENCIAIS SECRETAS DO ADMIN ---
ADMIN_USER = "Admin"
ADMIN_PASS = "gazelas123"

# --- FUNÇÕES DE BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS jogos (
                    id INTEGER PRIMARY KEY,
                    time_a TEXT,
                    time_b TEXT,
                    data_hora TEXT,
                    gols_a INTEGER,
                    gols_b INTEGER)''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS palpites (
                    usuario TEXT,
                    jogo_id INTEGER,
                    palpite_a INTEGER,
                    palpite_b INTEGER,
                    PRIMARY KEY (usuario, jogo_id))''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    nome TEXT PRIMARY KEY,
                    senha TEXT)''')
    
    c.execute('SELECT count(*) FROM jogos')
    if c.fetchone()[0] == 0:
        jogos_da_copa = [
            # Grupo A
            ('🇲🇽 México', '🇿🇦 África do Sul', '2026-06-11 16:00:00'),
            ('🇰🇷 Coreia do Sul', '🇨🇿 República Tcheca', '2026-06-11 20:00:00'),
            ('🇨🇿 República Tcheca', '🇿🇦 África do Sul', '2026-06-18 13:00:00'),
            ('🇲🇽 México', '🇰🇷 Coreia do Sul', '2026-06-18 22:00:00'),
            ('🇨🇿 República Tcheca', '🇲🇽 México', '2026-06-24 22:00:00'),
            ('🇿🇦 África do Sul', '🇰🇷 Coreia do Sul', '2026-06-24 22:00:00'),
            # Grupo B
            ('🇨🇦 Canadá', '🇧🇦 Bósnia', '2026-06-12 16:00:00'),
            ('🇶🇦 Catar', '🇨🇭 Suíça', '2026-06-13 16:00:00'),
            ('🇨🇭 Suíça', '🇧🇦 Bósnia', '2026-06-18 16:00:00'),
            ('🇨🇦 Canadá', '🇶🇦 Catar', '2026-06-18 19:00:00'),
            ('🇨🇦 Canadá', '🇨🇭 Suíça', '2026-06-24 16:00:00'),
            ('🇧🇦 Bósnia', '🇶🇦 Catar', '2026-06-24 16:00:00'),
            # Grupo C
            ('🇧🇷 Brasil', '🇲🇦 Marrocos', '2026-06-13 19:00:00'),
            ('🇭🇹 Haiti', '🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia', '2026-06-13 22:00:00'),
            ('🇧🇷 Brasil', '🇭🇹 Haiti', '2026-06-19 21:30:00'),
            ('🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia', '🇲🇦 Marrocos', '2026-06-19 19:00:00'),
            ('🇧🇷 Brasil', '🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia', '2026-06-24 19:00:00'),
            ('🇲🇦 Marrocos', '🇭🇹 Haiti', '2026-06-24 19:00:00'),
            # Grupo D
            ('🇺🇸 Estados Unidos', '🇵🇾 Paraguai', '2026-06-12 22:00:00'),
            ('🇦🇺 Austrália', '🇹🇷 Turquia', '2026-06-14 01:00:00'),
            ('🇺🇸 Estados Unidos', '🇦🇺 Austrália', '2026-06-19 16:00:00'),
            ('🇹🇷 Turquia', '🇵🇾 Paraguai', '2026-06-19 00:00:00'),
            ('🇺🇸 Estados Unidos', '🇹🇷 Turquia', '2026-06-25 23:00:00'),
            ('🇦🇺 Austrália', '🇵🇾 Paraguai', '2026-06-25 23:00:00'),
            # Grupo E
            ('🇩🇪 Alemanha', '🇨🇼 Curaçau', '2026-06-14 14:00:00'),
            ('🇨🇮 Costa do Marfim', '🇪🇨 Equador', '2026-06-14 20:00:00'),
            ('🇩🇪 Alemanha', '🇨🇮 Costa do Marfim', '2026-06-20 17:00:00'),
            ('🇨🇼 Curaçau', '🇪🇨 Equador', '2026-06-20 21:00:00'),
            ('🇩🇪 Alemanha', '🇪🇨 Equador', '2026-06-25 17:00:00'),
            ('🇨🇼 Curaçau', '🇨🇮 Costa do Marfim', '2026-06-25 17:00:00'),
            # Grupo F
            ('🇳🇱 Holanda', '🇯🇵 Japão', '2026-06-14 17:00:00'),
            ('🇸🇪 Suécia', '🇹🇳 Tunísia', '2026-06-14 23:00:00'),
            ('🇳🇱 Holanda', '🇸🇪 Suécia', '2026-06-20 14:00:00'),
            ('🇹🇳 Tunísia', '🇯🇵 Japão', '2026-06-20 23:00:00'),
            ('🇯🇵 Japão', '🇸🇪 Suécia', '2026-06-25 20:00:00'),
            ('🇳🇱 Holanda', '🇹🇳 Tunísia', '2026-06-25 20:00:00'),
            # Grupo G
            ('🇧🇪 Bélgica', '🇪🇬 Egito', '2026-06-15 16:00:00'),
            ('🇮🇷 Irã', '🇳🇿 Nova Zelândia', '2026-06-15 22:00:00'),
            ('🇧🇪 Bélgica', '🇮🇷 Irã', '2026-06-21 16:00:00'),
            ('🇳🇿 Nova Zelândia', '🇪🇬 Egito', '2026-06-20 22:00:00'),
            ('🇧🇪 Bélgica', '🇳🇿 Nova Zelândia', '2026-06-27 00:00:00'),
            ('🇮🇷 Irã', '🇪🇬 Egito', '2026-06-27 00:00:00'),
            # Grupo H
            ('🇪🇸 Espanha', '🇨🇻 Cabo Verde', '2026-06-15 13:00:00'),
            ('🇸🇦 Arábia Saudita', '🇺🇾 Uruguai', '2026-06-15 19:00:00'),
            ('🇪🇸 Espanha', '🇸🇦 Arábia Saudita', '2026-06-21 13:00:00'),
            ('🇨🇻 Cabo Verde', '🇺🇾 Uruguai', '2026-06-21 19:00:00'),
            ('🇪🇸 Espanha', '🇺🇾 Uruguai', '2026-06-26 21:00:00'),
            ('🇨🇻 Cabo Verde', '🇸🇦 Arábia Saudita', '2026-06-26 21:00:00'),
            # Grupo I
            ('🇫🇷 França', '🇸🇳 Senegal', '2026-06-16 16:00:00'),
            ('🇮🇶 Iraque', '🇳🇴 Noruega', '2026-06-16 19:00:00'),
            ('🇫🇷 França', '🇮🇶 Iraque', '2026-06-22 18:00:00'),
            ('🇳🇴 Noruega', '🇸🇳 Senegal', '2026-06-22 21:00:00'),
            ('🇫🇷 França', '🇳🇴 Noruega', '2026-06-26 16:00:00'),
            ('🇮🇶 Iraque', '🇸🇳 Senegal', '2026-06-26 16:00:00'),
            # Grupo J
            ('🇦🇹 Áustria', '🇯🇴 Jordânia', '2026-06-16 01:00:00'),
            ('🇦🇷 Argentina', '🇩🇿 Argélia', '2026-06-16 22:00:00'),
            ('🇦🇷 Argentina', '🇦🇹 Áustria', '2026-06-22 14:00:00'),
            ('🇯🇴 Jordânia', '🇩🇿 Argélia', '2026-06-23 00:00:00'),
            ('🇦🇹 Áustria', '🇩🇿 Argélia', '2026-06-27 23:00:00'),
            ('🇦🇷 Argentina', '🇯🇴 Jordânia', '2026-06-27 23:00:00'),
            # Grupo K
            ('🇵🇹 Portugal', '🇨🇩 Congo', '2026-06-17 14:00:00'),
            ('🇺🇿 Uzbequistão', '🇨🇴 Colômbia', '2026-06-17 21:00:00'),
            ('🇵🇹 Portugal', '🇺🇿 Uzbequistão', '2026-06-23 14:00:00'),
            ('🇨🇩 Congo', '🇨🇴 Colômbia', '2026-06-23 23:00:00'),
            ('🇵🇹 Portugal', '🇨🇴 Colômbia', '2026-06-27 20:30:00'),
            ('🇨🇩 Congo', '🇺🇿 Uzbequistão', '2026-06-27 20:30:00'),
            # Grupo L
            ('🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra', '🇭🇷 Croácia', '2026-06-17 17:00:00'),
            ('🇬🇭 Gana', '🇵🇦 Panamá', '2026-06-17 20:00:00'),
            ('🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra', '🇬🇭 Gana', '2026-06-23 17:00:00'),
            ('🇵🇦 Panamá', '🇭🇷 Croácia', '2026-06-23 20:00:00'),
            ('🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra', '🇵🇦 Panamá', '2026-06-27 18:00:00'),
            ('🇬🇭 Gana', '🇭🇷 Croácia', '2026-06-27 18:00:00')
        ]
        for t_a, t_b, d_h in jogos_da_copa:
            c.execute("INSERT INTO jogos (time_a, time_b, data_hora) VALUES (?, ?, ?)", (t_a, t_b, d_h))
        conn.commit()
    conn.close()

def adicionar_novo_jogo(time_a, time_b, data_hora):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO jogos (time_a, time_b, data_hora) VALUES (?, ?, ?)", (time_a, time_b, data_hora))
    conn.commit()
    conn.close()

def criar_usuario(nome, senha):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_login(nome, senha):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    u = c.fetchone()
    conn.close()
    return u is not None

def get_todos_usuarios():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT nome, senha FROM usuarios", conn)
    conn.close()
    return df

def get_jogos():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM jogos ORDER BY data_hora ASC", conn)
    conn.close()
    return df

def salvar_palpite(usuario, jogo_id, p_a, p_b):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO palpites (usuario, jogo_id, palpite_a, palpite_b) VALUES (?, ?, ?, ?)", (usuario, jogo_id, p_a, p_b))
    conn.commit()
    conn.close()

def get_palpites_usuario(usuario):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM palpites WHERE usuario = ?", conn, params=(usuario,))
    conn.close()
    return df

def get_todos_palpites_do_jogo(jogo_id):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT usuario as Participante, palpite_a as 'Gols A', palpite_b as 'Gols B' FROM palpites WHERE jogo_id = ? ORDER BY usuario", conn, params=(jogo_id,))
    conn.close()
    return df

def atualizar_resultado_real(j_id, g_a, g_b):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE jogos SET gols_a = ?, gols_b = ? WHERE id = ?", (g_a, g_b, j_id))
    conn.commit()
    conn.close()

def calcular_ranking():
    conn = sqlite3.connect(DB_NAME)
    usuarios_df = pd.read_sql_query("SELECT nome FROM usuarios", conn)
    query = "SELECT p.usuario, p.palpite_a, p.palpite_b, j.gols_a, j.gols_b FROM palpites p JOIN jogos j ON p.jogo_id = j.id WHERE j.gols_a IS NOT NULL"
    palpites_df = pd.read_sql_query(query, conn)
    conn.close()

    pontos = {nome: 0 for nome in usuarios_df['nome']}
    
    for _, row in palpites_df.iterrows():
        user = row['usuario']
        pA, pB = row['palpite_a'], row['palpite_b']
        rA, rB = row['gols_a'], row['gols_b']
        
        pts = 0
        if pA == rA and pB == rB: pts = 3 
        elif (pA > pB and rA > rB) or (pA < pB and rA < rB) or (pA == pB and rA == rB): pts = 1 
        
        if user in pontos: pontos[user] += pts
        
    return pd.DataFrame(list(pontos.items()), columns=['Participante', 'Pontos']).sort_values(by='Pontos', ascending=False).reset_index(drop=True)

def calcular_tabela_copa():
    grupos = {
        'Grupo A': ['🇲🇽 México', '🇿🇦 África do Sul', '🇰🇷 Coreia do Sul', '🇨🇿 República Tcheca'],
        'Grupo B': ['🇨🇦 Canadá', '🇧🇦 Bósnia', '🇶🇦 Catar', '🇨🇭 Suíça'],
        'Grupo C': ['🇧🇷 Brasil', '🇲🇦 Marrocos', '🇭🇹 Haiti', '🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia'],
        'Grupo D': ['🇺🇸 Estados Unidos', '🇵🇾 Paraguai', '🇦🇺 Austrália', '🇹🇷 Turquia'],
        'Grupo E': ['🇩🇪 Alemanha', '🇨🇼 Curaçau', '🇨🇮 Costa do Marfim', '🇪🇨 Equador'],
        'Grupo F': ['🇳🇱 Holanda', '🇯🇵 Japão', '🇸🇪 Suécia', '🇹🇳 Tunísia'],
        'Grupo G': ['🇧🇪 Bélgica', '🇪🇬 Egito', '🇮🇷 Irã', '🇳🇿 Nova Zelândia'],
        'Grupo H': ['🇪🇸 Espanha', '🇨🇻 Cabo Verde', '🇸🇦 Arábia Saudita', '🇺🇾 Uruguai'],
        'Grupo I': ['🇫🇷 França', '🇸🇳 Senegal', '🇮🇶 Iraque', '🇳🇴 Noruega'],
        'Grupo J': ['🇦🇹 Áustria', '🇯🇴 Jordânia', '🇦🇷 Argentina', '🇩🇿 Argélia'],
        'Grupo K': ['🇵🇹 Portugal', '🇨🇩 Congo', '🇺🇿 Uzbequistão', '🇨🇴 Colômbia'],
        'Grupo L': ['🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra', '🇭🇷 Croácia', '🇬🇭 Gana', '🇵🇦 Panamá']
    }

    conn = sqlite3.connect(DB_NAME)
    jogos_realizados = pd.read_sql_query("SELECT time_a, time_b, gols_a, gols_b FROM jogos WHERE gols_a IS NOT NULL", conn)
    conn.close()

    tabela = {}
    for grupo, times in grupos.items():
        for time in times:
            tabela[time] = {'Grupo': grupo, 'Time': time, 'Pts': 0, 'J': 0, 'V': 0, 'E': 0, 'D': 0, 'GP': 0, 'GC': 0, 'SG': 0}

    for _, jogo in jogos_realizados.iterrows():
        ta, tb = jogo['time_a'], jogo['time_b']
        ga, gb = int(jogo['gols_a']), int(jogo['gols_b'])

        if ta in tabela:
            tabela[ta]['J'] += 1
            tabela[ta]['GP'] += ga
            tabela[ta]['GC'] += gb
            tabela[ta]['SG'] += (ga - gb)
            if ga > gb:
                tabela[ta]['Pts'] += 3
                tabela[ta]['V'] += 1
            elif ga == gb:
                tabela[ta]['Pts'] += 1
                tabela[ta]['E'] += 1
            else:
                tabela[ta]['D'] += 1

        if tb in tabela:
            tabela[tb]['J'] += 1
            tabela[tb]['GP'] += gb
            tabela[tb]['GC'] += ga
            tabela[tb]['SG'] += (gb - ga)
            if gb > ga:
                tabela[tb]['Pts'] += 3
                tabela[tb]['V'] += 1
            elif gb == ga:
                tabela[tb]['Pts'] += 1
                tabela[tb]['E'] += 1
            else:
                tabela[tb]['D'] += 1

    return pd.DataFrame(list(tabela.values()))

# --- INICIALIZAÇÃO ---
init_db()
if 'usuario_logado' not in st.session_state: st.session_state.usuario_logado = None

# --- INTERFACE ---
st.title("⚽🦌 Gazelas Bet")

if st.session_state.usuario_logado is None:
    st.subheader("🔐 Acesso ao Bolão")
    aba_login, aba_criar = st.tabs(["Entrar", "Criar Conta Nova"])
    
    with aba_login:
        n_l = st.text_input("Seu Nome:")
        s_l = st.text_input("Sua Senha:", type="password")
        if st.button("Entrar", type="primary"):
            if n_l == ADMIN_USER and s_l == ADMIN_PASS:
                st.session_state.usuario_logado = "ADMIN"
                st.rerun()
            elif verificar_login(n_l, s_l):
                st.session_state.usuario_logado = n_l
                st.rerun()
            else: st.error("Nome ou senha incorretos!")
            
    with aba_criar:
        st.info("Escolha um nome que seus amigos reconheçam (Ex: Lucas, Alemao, Fer)")
        n_n = st.text_input("Escolha um Nome:")
        s_n = st.text_input("Crie uma Senha:", type="password")
        if st.button("Criar Conta"):
            if n_n.upper() == ADMIN_USER.upper():
                st.error("🚨 Nome reservado pelo sistema! Escolha outro.")
            elif n_n and s_n:
                if criar_usuario(n_n, s_n): st.success("Conta criada! Vá em 'Entrar'.")
                else: st.error("🚨 Nome já existe!")
            else: st.warning("Preencha tudo!")
else:
    user = st.session_state.usuario_logado
    col_n, col_s = st.columns([4, 1])
    
    with col_n: 
        if user == "ADMIN":
            st.error("Você está logado como **ADMINISTRADOR MESTRE**.")
        else:
            st.write(f"Bem-vindo(a), **{user}**!")
            
    with col_s: 
        if st.button("Sair"):
            st.session_state.usuario_logado = None
            st.rerun()

    tab1, tab2, tab3, tab_copa, tab4 = st.tabs(["⚽ Palpitar", "🏆 Ranking", "👀 Espiar", "🌍 Copa", "⚙️ Admin"])

    with tab1:
        if user == "ADMIN":
            st.warning("⚠️ O Administrador Mestre não pode dar palpites. Saia desta conta e entre com a sua conta de jogador normal para palpitar.")
        else:
            st.subheader("Meus Palpites")
            jogos = get_jogos()
            p_u = get_palpites_usuario(user)
            
            jogos['data_apenas'] = pd.to_datetime(jogos['data_hora']).dt.strftime('%d/%m/%Y')
            dias_unicos = jogos['data_apenas'].unique()
            
            for dia in dias_unicos:
                # --- AQUI ESTÁ A SANFONA (EXPANDER) ---
                with st.expander(f"📅 Jogos do dia {dia}"):
                    jogos_do_dia = jogos[jogos['data_apenas'] == dia]
                    
                    for _, j in jogos_do_dia.iterrows():
                        st.markdown("---")
                        h_j = datetime.strptime(j['data_hora'], '%Y-%m-%d %H:%M:%S')
                        travado = datetime.now() >= h_j
                        
                        c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 3])
                        with c1: st.write(f"**{j['time_a']}**")
                        with c5: st.write(f"**{j['time_b']}**")
                        
                        p_at = p_u[p_u['jogo_id'] == j['id']]
                        v_a = int(p_at.iloc[0]['palpite_a']) if not p_at.empty else 0
                        v_b = int(p_at.iloc[0]['palpite_b']) if not p_at.empty else 0
                        
                        if travado:
                            with c2: st.warning(f"{v_a}", icon="🔒")
                            with c3: st.write("X")
                            with c4: st.warning(f"{v_b}", icon="🔒")
                            st.caption(f"Jogo iniciado ({h_j.strftime('%H:%M')}).")
                        else:
                            with c2: pa_a = st.number_input(f"A_{j['id']}", min_value=0, value=v_a, label_visibility="collapsed")
                            with c3: st.write("X")
                            with c4: pa_b = st.number_input(f"B_{j['id']}", min_value=0, value=v_b, label_visibility="collapsed")
                            if st.button(f"Salvar {j['time_a']} x {j['time_b']}", key=f"btn_{j['id']}"):
                                salvar_palpite(user, int(j['id']), pa_a, pa_b)
                                st.success("Salvo!")
                            st.caption(f"Fecha às: {h_j.strftime('%H:%M')}")

    with tab2:
        st.markdown("### *Gazelas Bet*⚽🦌")
        df_rank = calcular_ranking()
        if not df_rank.empty:
            txt = "_Classificação_ 🏆\n\n"
            for i, r in df_rank.iterrows():
                p = i + 1
                emoji = "🥇" if p==1 else "🥈" if p==2 else "🥉" if p==3 else "▪️" if p<=10 else "🔻"
                txt += f"{emoji}{p}. {r['Participante']} - {r['Pontos']} pts\n"
            st.markdown(txt)
            st.code(txt, language="text")
        else:
            st.info("Nenhum usuário cadastrado ainda.")

    with tab3:
        st.subheader("👀 Espiar")
        js = get_jogos()
        ops = {j['id']: f"{j['time_a']} x {j['time_b']} ({datetime.strptime(j['data_hora'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m %H:%M')})" for _, j in js.iterrows()}
        sel = st.selectbox("Jogo:", options=list(ops.keys()), format_func=lambda x: ops[x])
        if sel:
            j_i = js[js['id'] == sel].iloc[0]
            if datetime.now() >= datetime.strptime(j_i['data_hora'], '%Y-%m-%d %H:%M:%S'):
                df_palpites_jogo = get_todos_palpites_do_jogo(sel)
                if not df_palpites_jogo.empty:
                    st.dataframe(df_palpites_jogo, hide_index=True, use_container_width=True)
                else:
                    st.info("Ninguém deu palpite para este jogo ainda.")
            else: st.warning("⚠️ Shhhh! Os palpites estão ocultos para ninguém copiar!")

    with tab_copa:
        st.subheader("🌍 Tabela Oficial da Copa")
        st.write("Classificação baseada nos resultados reais informados no Admin!")
        df_copa = calcular_tabela_copa()
        if not df_copa.empty:
            grupos_ordenados = sorted(df_copa['Grupo'].unique())
            for grupo in grupos_ordenados:
                st.markdown(f"### {grupo}")
                df_grupo = df_copa[df_copa['Grupo'] == grupo].sort_values(
                    by=['Pts', 'SG', 'GP'], ascending=[False, False, False]
                )
                df_grupo = df_grupo.drop(columns=['Grupo']).reset_index(drop=True)
                df_grupo.index = df_grupo.index + 1
                st.dataframe(df_grupo, use_container_width=True)

    with tab4:
        if user == "ADMIN":
            st.subheader("🔑 Painel do Mestre")
            
            with st.expander("👥 Lista de Usuários e Senhas (Sigiloso)"):
                st.dataframe(get_todos_usuarios(), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.write("**Preencha os placares oficiais:**")
            jogos_adm = get_jogos()
            for _, jo in jogos_adm.iterrows():
                c_a, c_b, c_c, c_d = st.columns([2,1,1,2])
                with c_a: st.write(f"{jo['time_a']} x {jo['time_b']}")
                ga = int(jo['gols_a']) if pd.notnull(jo['gols_a']) else 0
                gb = int(jo['gols_b']) if pd.notnull(jo['gols_b']) else 0
                with c_b: n_ga = st.number_input("G_A", value=ga, key=f"ad_a_{jo['id']}", label_visibility="collapsed")
                with c_c: n_gb = st.number_input("G_B", value=gb, key=f"ad_b_{jo['id']}", label_visibility="collapsed")
                with c_d: 
                    if st.button("Salvar Resultado", key=f"ad_btn_{jo['id']}"):
                        atualizar_resultado_real(jo['id'], n_ga, n_gb)
                        st.success("Atualizado!")
                        
            st.markdown("---")
            st.subheader("➕ Adicionar Jogo (Oitavas, Quartas...)")
            st.write("Crie novos jogos sem perder os dados antigos da primeira fase.")
            c_t1, c_t2, c_dt, c_bt = st.columns([2, 2, 2, 1])
            with c_t1: novo_t_a = st.text_input("Time A (Ex: 🇧🇷 Brasil)")
            with c_t2: novo_t_b = st.text_input("Time B (Ex: 🇫🇷 França)")
            with c_dt: novo_data = st.text_input("Data (AAAA-MM-DD HH:MM:SS)", value="2026-06-28 16:00:00")
            with c_bt: 
                st.write("") 
                st.write("")
                if st.button("Criar Jogo", type="primary"):
                    if novo_t_a and novo_t_b and novo_data:
                        adicionar_novo_jogo(novo_t_a, novo_t_b, novo_data)
                        st.success("Jogo adicionado com sucesso!")
                    else:
                        st.warning("Preencha todos os campos!")
        else:
            st.error("Acesso restrito ao Administrador da Banca.")