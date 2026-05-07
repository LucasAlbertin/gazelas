import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Gazelas Bet 2026", layout="centered")

# Conexão com Supabase (Lendo dos Secrets)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- 🔐 CREDENCIAIS DO ADMIN ---
ADMIN_USER = "Admin"
ADMIN_PASS = "gazelas123"

# --- FUNÇÕES DE BANCO DE DADOS (SUPABASE) ---

def get_jogos():
    res = supabase.table("jogos").select("*").order("data_hora").execute()
    return pd.DataFrame(res.data)

def salvar_palpite(usuario, jogo_id, p_a, p_b):
    data = {"usuario": usuario, "jogo_id": jogo_id, "palpite_a": p_a, "palpite_b": p_b}
    supabase.table("palpites").upsert(data).execute()

def criar_usuario(nome, senha):
    try:
        supabase.table("usuarios").insert({"nome": nome, "senha": senha}).execute()
        return True
    except: return False

def verificar_login(nome, senha):
    res = supabase.table("usuarios").select("*").eq("nome", nome).eq("senha", senha).execute()
    return len(res.data) > 0

def get_todos_usuarios():
    res = supabase.table("usuarios").select("nome, senha").execute()
    return pd.DataFrame(res.data)

def atualizar_resultado_real(j_id, g_a, g_b):
    supabase.table("jogos").update({"gols_a": g_a, "gols_b": g_b}).eq("id", j_id).execute()

def reset_banco_dados():
    # Limpa palpites e usuários, e reseta resultados dos jogos
    supabase.table("palpites").delete().neq("usuario", "").execute()
    supabase.table("usuarios").delete().neq("nome", "").execute()
    supabase.table("jogos").update({"gols_a": None, "gols_b": None}).neq("time_a", "").execute()

def calcular_ranking():
    usuarios_res = supabase.table("usuarios").select("nome").execute()
    jogos_res = supabase.table("jogos").select("*").not_.is_("gols_a", "null").execute()
    palpites_res = supabase.table("palpites").select("*").execute()
    
    pontos = {u['nome']: 0 for u in usuarios_res.data}
    jogos_dict = {j['id']: j for j in jogos_res.data}
    
    for p in palpites_res.data:
        if p['jogo_id'] in jogos_dict:
            j = jogos_dict[p['jogo_id']]
            pts = 0
            pa, pb = p['palpite_a'], p['palpite_b']
            ra, rb = j['gols_a'], j['gols_b']
            if pa == ra and pb == rb: pts = 3
            elif (pa > pb and ra > rb) or (pa < pb and ra < rb) or (pa == pb and ra == rb): pts = 1
            if p['usuario'] in pontos: pontos[p['usuario']] += pts
            
    return pd.DataFrame(list(pontos.items()), columns=['Participante', 'Pontos']).sort_values(by='Pontos', ascending=False)

# --- INTERFACE ---
st.title("⚽🦌 Gazelas Bet")

if 'usuario_logado' not in st.session_state: st.session_state.usuario_logado = None

if st.session_state.usuario_logado is None:
    st.subheader("🔐 Acesso ao Bolão")
    aba_l, aba_c = st.tabs(["Entrar", "Criar Conta"])
    with aba_l:
        nl = st.text_input("Nome:")
        sl = st.text_input("Senha:", type="password")
        if st.button("Entrar"):
            if nl == ADMIN_USER and sl == ADMIN_PASS:
                st.session_state.usuario_logado = "ADMIN"; st.rerun()
            elif verificar_login(nl, sl):
                st.session_state.usuario_logado = nl; st.rerun()
            else: st.error("Login incorreto!")
    with aba_c:
        nn = st.text_input("Novo Nome:")
        sn = st.text_input("Nova Senha:", type="password")
        if st.button("Cadastrar"):
            if nn and sn and criar_usuario(nn, sn): st.success("Criado!")
            else: st.error("Erro ou nome já existe.")

else:
    user = st.session_state.usuario_logado
    st.write(f"Olá, **{user}**!")
    t1, t2, t3, t4, t5 = st.tabs(["⚽ Palpites", "🏆 Ranking", "👀 Espiar", "🌍 Copa", "⚙️ Admin"])

    with t1:
        if user == "ADMIN": st.warning("Admin não palpita.")
        else:
            jogos = get_jogos()
            jogos['data_f'] = pd.to_datetime(jogos['data_hora']).dt.strftime('%d/%m/%Y')
            for dia in jogos['data_f'].unique():
                with st.expander(f"📅 Jogos de {dia}"):
                    for _, j in jogos[jogos['data_f'] == dia].iterrows():
                        st.write(f"{j['time_a']} x {j['time_b']}")
                        # Aqui você pode completar com os inputs de palpites como já tínhamos!

    with t5:
        if user == "ADMIN":
            st.subheader("Painel de Controle")
            if st.checkbox("⚠️ RESETAR BANCO PARA LANÇAMENTO"):
                if st.button("CONFIRMAR APAGAR TUDO"):
                    reset_banco_dados()
                    st.success("Tabelas limpas!")