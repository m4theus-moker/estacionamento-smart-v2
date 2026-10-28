import streamlit as st
import requests
import os
import re
import html
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# 13. Configuração da página chamada uma única vez no topo
st.set_page_config(
    page_title="Estacionamento Smart",
    page_icon="🚗",
    layout="wide"
)

def apply_background():
    st.markdown("""
    <style>
        .stApp {
            background-color: #030504 !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stExpander"] {
            border: 1px solid rgba(34, 197, 94, 0.45) !important;
            border-radius: 8px;
        }
        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(34, 197, 94, 0.45) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Aplica o fundo temático de estacionamento
apply_background()

# 15. Centralização de textos de interface
TEXTS = {
    "app_title": "Estacionamento Smart",
    "app_subtitle": "Sistema Inteligente de Gestão de Vagas",
    "login_tab": "Entrar",
    "register_tab": "Criar Conta",
    "email_label": "E-mail",
    "password_label": "Senha",
    "confirm_password_label": "Confirmar Senha",
    "name_label": "Nome Completo",
    "cpf_label": "CPF",
    "phone_label": "Telefone",
    "login_btn": "Entrar no Sistema",
    "register_btn": "Registrar Conta",
    "my_vehicles_title": "Meus Veículos",
    "logout_btn": "Sair"
}

# Feature flag para telas futuras (ocultas por padrão)
TELAS_DISPONIVEIS = True

# Recupera URLs base do Xano do ambiente
XANO_API_URL = os.getenv("XANO_API_URL")
XANO_VEHICLES_URL = os.getenv("XANO_VEHICLES_URL")
XANO_PARKING_URL = os.getenv("XANO_PARKING_URL")

def init_session():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None

init_session()

def api_request(method, endpoint, data=None, auth=True, base_url=None):
    headers = {}
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    if not base_url:
        if endpoint.startswith("/location") or endpoint.startswith("/vaga") or endpoint.startswith("/tarifa"):
            if not XANO_PARKING_URL:
                return None, "Erro de Configuração: XANO_PARKING_URL não está definida no arquivo .env."
            base = XANO_PARKING_URL
        else:
            base = XANO_API_URL
    else:
        base = base_url

    url = f"{base}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return None, f"Método HTTP inválido: {method} em {url}"
        
        if response.status_code in [200, 201]:
            try:
                return response.json(), None
            except:
                return {}, None
        elif response.status_code == 401 or response.status_code == 403:
            # Se token expirou, limpa sessão para forçar novo login
            if auth:
                st.session_state.token = None
                st.session_state.user_role = None
                st.session_state.user_email = None
            return None, "E-mail ou senha incorretos / Sessão expirada."
        elif response.status_code == 409:
            return None, "Conflito de horário: Vaga já reservada neste período (409)."
        elif response.status_code == 404:
            return None, f"Endpoint não encontrado (`{url}`). Verifique a API."
        else:
            try:
                err_json = response.json()
                msg = err_json.get("message", "")
                if msg:
                    err_msg = msg
                else:
                    err_msg = str(err_json)
            except:
                err_msg = response.text
            return None, f"Erro ({response.status_code}): {err_msg}"
    except Exception as e:
        return None, f"Erro de conexão: {str(e)}"

# --- TELA DE LOGIN / CADASTRO (C) ---
def auth_page():
    # Variáveis de cor e opacidade ajustáveis
    parking_bg = "#030504"
    line_color = "rgba(34, 197, 94, 0.40)"
    label_color = "rgba(34, 197, 94, 0.55)"
    lane_color = "rgba(34, 197, 94, 0.18)"

    svg_top = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='700' height='200' viewBox='0 0 700 200' fill='none' stroke='{line_color}' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='0' y1='0' x2='0' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='140' y1='0' x2='140' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='280' y1='0' x2='280' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='420' y1='0' x2='420' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='560' y1='0' x2='560' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='700' y1='0' x2='700' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='0' y1='197' x2='700' y2='197' stroke='{line_color}' stroke-width='3'/><g transform='translate(70, 80)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><path d='M-12 -15 C-12 -20 -8 -22 0 -22 C8 -22 12 -20 12 -15 L12 5 L-12 5 Z' fill='none' stroke-width='1.5'/><rect x='-9' y='-18' width='18' height='8' rx='2' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>CARRO</text></g><g transform='translate(210, 80)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><path d='M-12 -15 C-12 -20 -8 -22 0 -22 C8 -22 12 -20 12 -15 L12 5 L-12 5 Z' fill='none' stroke-width='1.5'/><rect x='-9' y='-18' width='18' height='8' rx='2' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>CARRO</text></g><g transform='translate(350, 80)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><circle cx='-10' cy='5' r='7' fill='none' stroke-width='1.5'/><circle cx='10' cy='5' r='7' fill='none' stroke-width='1.5'/><path d='M-10 5 L-2 -10 L8 -10 L10 5' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>MOTO</text></g><g transform='translate(490, 80)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><circle cx='0' cy='-14' r='3.5' fill='none' stroke-width='1.5'/><path d='M-4 -8 C-4 -12 4 -12 4 -8 C4 -6 0 -4 0 0 L0 8' fill='none' stroke-width='1.5'/><circle cx='3' cy='5' r='6' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>PCD</text></g><g transform='translate(630, 80)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><path d='M3 -22 L-6 -2 L2 -2 L-3 18' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>ELÉTRICO</text></g></svg>"

    svg_bottom = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='700' height='200' viewBox='0 0 700 200' fill='none' stroke='{line_color}' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='0' y1='0' x2='700' y2='0' stroke='{line_color}' stroke-width='3'/><line x1='0' y1='0' x2='0' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='140' y1='0' x2='140' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='280' y1='0' x2='280' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='420' y1='0' x2='420' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='560' y1='0' x2='560' y2='200' stroke='{line_color}' stroke-width='3'/><line x1='700' y1='0' x2='700' y2='200' stroke='{line_color}' stroke-width='3'/><g transform='translate(70, 110)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><path d='M-12 -15 C-12 -20 -8 -22 0 -22 C8 -22 12 -20 12 -15 L12 5 L-12 5 Z' fill='none' stroke-width='1.5'/><rect x='-9' y='-18' width='18' height='8' rx='2' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>CARRO</text></g><g transform='translate(210, 110)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><path d='M-12 -15 C-12 -20 -8 -22 0 -22 C8 -22 12 -20 12 -15 L12 5 L-12 5 Z' fill='none' stroke-width='1.5'/><rect x='-9' y='-18' width='18' height='8' rx='2' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>CARRO</text></g><g transform='translate(350, 110)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><circle cx='-10' cy='5' r='7' fill='none' stroke-width='1.5'/><circle cx='10' cy='5' r='7' fill='none' stroke-width='1.5'/><path d='M-10 5 L-2 -10 L8 -10 L10 5' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>MOTO</text></g><g transform='translate(490, 110)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><circle cx='0' cy='-14' r='3.5' fill='none' stroke-width='1.5'/><path d='M-4 -8 C-4 -12 4 -12 4 -8 C4 -6 0 -4 0 0 L0 8' fill='none' stroke-width='1.5'/><circle cx='3' cy='5' r='6' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>PCD</text></g><g transform='translate(630, 110)' fill='{label_color}' stroke='{label_color}' font-family='sans-serif' font-size='14' font-weight='bold' text-anchor='middle'><path d='M3 -22 L-6 -2 L2 -2 L-3 18' fill='none' stroke-width='1.5'/><text x='0' y='30' letter-spacing='1'>ELÉTRICO</text></g></svg>"

    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {parking_bg} !important;
            background-image: 
                url("{svg_top}"),
                url("{svg_bottom}"),
                repeating-linear-gradient(90deg, {lane_color} 0px, {lane_color} 30px, transparent 30px, transparent 60px),
                radial-gradient(circle at center, rgba(3,5,4,0.95) 0%, rgba(3,5,4,0.99) 100%);
            background-size: 
                700px 28%,
                700px 28%,
                100% 3px,
                100% 100%;
            background-position: 
                top left,
                bottom left,
                center,
                center;
            background-repeat: 
                repeat-x,
                repeat-x,
                repeat-x,
                no-repeat;
            background-attachment: fixed;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown(f"## :material/directions_car: {TEXTS['app_title']}")
        st.caption(TEXTS['app_subtitle'])
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")
        
        with st.container(border=True):
            tab_login, tab_register = st.tabs([f":material/login: {TEXTS['login_tab']}", f":material/person_add: {TEXTS['register_tab']}"])

            with tab_login:
                with st.form("login_form", border=False):
                    email = st.text_input(TEXTS['email_label'], placeholder="seu@email.com")
                    password = st.text_input(TEXTS['password_label'], type="password", placeholder="••••••••")
                    
                    st.write("")
                    submitted_login = st.form_submit_button(TEXTS['login_btn'], type="primary", use_container_width=True)
                    
                    if submitted_login:
                        if not email or not password:
                            st.warning("Preencha e-mail e senha.")
                        else:
                            with st.spinner("Autenticando..."):
                                data, err = api_request("POST", "/auth/login", {"email": email, "password": password}, auth=False)
                                if err:
                                    st.error(err)
                                else:
                                    token = data.get("authToken") or data.get("token")
                                    st.session_state.token = token
                                    st.session_state.user_email = email
                                    
                                    me_data, me_err = api_request("GET", "/auth/me", auth=True)
                                    if not me_err and me_data:
                                        st.session_state.user_role = me_data.get("role", "client")
                                    else:
                                        st.session_state.user_role = data.get("role", "client")
                                        
                                    st.toast("Login realizado com sucesso!", icon=":material/rocket:")
                                    st.rerun()

            with tab_register:
                st.markdown("### Crie sua conta de cliente")
                with st.form("register_form", border=False):
                    reg_name = st.text_input(TEXTS['name_label'], placeholder="Seu Nome Completo")
                    reg_email = st.text_input(TEXTS['email_label'], placeholder="seu@email.com")
                    reg_cpf = st.text_input(TEXTS['cpf_label'], placeholder="000.000.000-00", help="Digite 11 dígitos")
                    reg_phone = st.text_input(TEXTS['phone_label'], placeholder="(00) 00000-0000", help="DDD + Número")
                    reg_password = st.text_input(TEXTS['password_label'], type="password", placeholder="••••••••", help="Mínimo de 8 caracteres")
                    reg_password_confirm = st.text_input(TEXTS['confirm_password_label'], type="password", placeholder="••••••••")
                    
                    st.write("")
                    submitted_reg = st.form_submit_button(TEXTS['register_btn'], type="primary", use_container_width=True)
                    
                    if submitted_reg:
                        cpf_clean = re.sub(r'\D', '', reg_cpf)
                        phone_clean = re.sub(r'\D', '', reg_phone)
                        
                        if not reg_name or not reg_email or not reg_cpf or not reg_phone or not reg_password or not reg_password_confirm:
                            st.warning("Preencha todos os campos obrigatórios.")
                        elif len(cpf_clean) != 11:
                            st.warning("CPF inválido. Certifique-se de informar 11 dígitos.")
                        elif len(phone_clean) < 10:
                            st.warning("Telefone inválido. Informe o DDD e o número.")
                        elif len(reg_password) < 8:
                            st.warning("A senha deve ter pelo menos 8 caracteres.")
                        elif reg_password != reg_password_confirm:
                            st.warning("As senhas não coincidem.")
                        else:
                            with st.spinner("Criando conta..."):
                                payload = {
                                    "email": reg_email,
                                    "password": reg_password,
                                    "name": reg_name,
                                    "cpf": reg_cpf,
                                    "phone": reg_phone
                                }
                                data, err = api_request("POST", "/auth/signup", payload, auth=False)
                                if err:
                                    st.error(err)
                                else:
                                    st.toast("Conta criada com sucesso! Faça login na aba ao lado.", icon=":material/celebration:")

# --- TELA MEUS VEÍCULOS (D) ---
def page_my_vehicles():
    st.title("Meus Veículos")
    
    safe_email = html.escape(st.session_state.user_email or "")
    st.markdown(f"""
        <div style="padding: 0.8rem 1rem; border-radius: 8px; background-color: #0e1117; border: 2px solid #22c55e; margin-bottom: 1.2rem;">
            <h3 style="margin: 0; color: #ffffff;">Olá, {safe_email}</h3>
            <p style="margin: 4px 0 0 0; color: #d1d5db; font-size: 1.05rem;">Gerencie sua frota de veículos cadastrados para futuras reservas de vagas.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Carregando veículos..."):
        vehicles, err = api_request("GET", "/vehicle", base_url=XANO_VEHICLES_URL)
    
    is_empty = not vehicles or err is not None
    
    with st.expander(":material/add_circle: Adicionar veículo", expanded=is_empty):
        with st.form("add_vehicle", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                plate = st.text_input("Placa do Veículo", placeholder="ABC1D23").strip().upper()
                brand = st.text_input("Marca", placeholder="Fiat").strip()
                model = st.text_input("Modelo", placeholder="Uno").strip()
            with col_f2:
                color = st.text_input("Cor", placeholder="Preto").strip()
                current_year = datetime.now().year
                year = st.number_input("Ano", min_value=1950, max_value=current_year + 1, value=current_year, step=1)
                v_type_display = st.segmented_control("Tipo de Veículo", ["Carro", "Moto", "PCD"], default="Carro")
                v_type_map = {"Carro": "carro", "Moto": "moto", "PCD": "pcd"}
                v_type = v_type_map.get(v_type_display, "carro")
            
            st.write("")
            col_b1, col_b2, col_b3 = st.columns([2, 2, 2])
            with col_b2:
                submitted_veh = st.form_submit_button("Salvar Veículo", type="primary", use_container_width=True)
            
            if submitted_veh:
                plate_clean = plate.replace("-", "").strip()
                pattern_old = r"^[A-Z]{3}[0-9]{4}$"
                pattern_mercosul = r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$"
                
                if not plate_clean or not brand or not model or not color:
                    st.error("Preencha todos os campos obrigatórios (Placa, Marca, Modelo, Cor).")
                elif not (re.match(pattern_old, plate_clean) or re.match(pattern_mercosul, plate_clean)):
                    st.error("Formato de placa inválido. Use o formato antigo (ABC-1234) ou Mercosul (ABC1D23).")
                else:
                    with st.spinner("Cadastrando veículo..."):
                        payload = {
                            "plate": plate,
                            "brand": brand,
                            "model": model,
                            "color": color,
                            "year": int(year),
                            "type": v_type
                        }
                        _, err_add = api_request("POST", "/vehicle", payload, base_url=XANO_VEHICLES_URL)
                        if err_add:
                            if "404" in err_add:
                                st.warning("⚠️ O endpoint /vehicle ainda não foi configurado no API Group de veículos do Xano.")
                            else:
                                st.error(err_add)
                        else:
                            st.toast("Veículo cadastrado com sucesso!", icon=":material/check_circle:")
                            st.cache_data.clear() if hasattr(st, "cache_data") else None
                            st.rerun()
    
    st.subheader("Sua Frota Cadastrada")
    
    if err:
        if "404" in err:
            st.info("ℹ️ Endpoint GET /vehicle ainda não implementado no Xano.")
        else:
            st.error(err)
    elif not vehicles:
        st.info("Você ainda não cadastrou veículos. Use o formulário acima para adicionar o primeiro.")
    else:
        for v in vehicles:
            if 'type' in v and v['type']:
                v['type'] = str(v['type']).strip().lower()
            else:
                v['type'] = 'carro'
                
        total_v = len(vehicles)
        total_carro = sum(1 for v in vehicles if v.get('type') == 'carro')
        total_moto = sum(1 for v in vehicles if v.get('type') == 'moto')
        total_pcd = sum(1 for v in vehicles if v.get('type') == 'pcd')
        
        with st.container(border=True):
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total", total_v)
            m2.metric("Carros", total_carro)
            m3.metric("Motos", total_moto)
            m4.metric("PCD", total_pcd)
        
        # Linha de filtros e ordenação rápida
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            search_query = st.text_input(":material/search: Buscar", placeholder="Digite placa, marca ou modelo...").strip().lower()
        with col_s2:
            sort_option = st.selectbox("Ordenar", ["Mais recentes", "Marca/Modelo", "Tipo"], label_visibility="collapsed")

        if search_query:
            vehicles = [v for v in vehicles if search_query in str(v.get('plate','')).lower() or search_query in str(v.get('brand','')).lower() or search_query in str(v.get('model','')).lower()]
        
        if sort_option == "Mais recentes":
            vehicles.sort(key=lambda x: x.get('year', 0), reverse=True)
        elif sort_option == "Marca/Modelo":
            vehicles.sort(key=lambda x: f"{x.get('brand','')}{x.get('model','')}".lower())
        elif sort_option == "Tipo":
            vehicles.sort(key=lambda x: x.get('type',''))

        if not vehicles:
            st.warning("Nenhum veículo encontrado com o termo buscado.")
            return

        type_icons = {"carro": ":material/directions_car:", "moto": ":material/two_wheeler:", "pcd": ":material/accessible:"}
        type_colors = {"carro": "#3b82f6", "moto": "#f59e0b", "pcd": "#10b981"}
        
        cols = st.columns(2)
        for idx, v in enumerate(vehicles):
            col_target = cols[idx % 2]
            with col_target:
                v_id = v.get('id')
                v_plate = v.get('plate')
                v_brand = v.get('brand', '')
                v_model = v.get('model', '')
                v_color = v.get('color', '')
                v_year = v.get('year', '')
                v_type_val = v.get('type', 'carro')
                icon = type_icons.get(v_type_val, ":material/directions_car:")
                badge_color = type_colors.get(v_type_val, "#6b7280")
                type_badge = f"<span style='background-color:{badge_color}; color:white; padding:2px 8px; border-radius:10px; font-size:0.75rem; font-weight:600;'>{v_type_val.capitalize()}</span>"
                
                with st.container(border=True):
                    st.markdown(f"### {icon} **{v_brand.title()} {v_model.title()}**")
                    st.code(f"{v_plate}", language=None)
                    st.markdown(f"Cor: {v_color.title()} &nbsp;|&nbsp; Ano: {v_year} &nbsp;|&nbsp; {type_badge}", unsafe_allow_html=True)
                    st.write("")
                    
                    confirm_key = f"confirm_del_{v_id}"
                    if confirm_key not in st.session_state:
                        st.session_state[confirm_key] = False
                        
                    if not st.session_state[confirm_key]:
                        if st.button("Excluir", key=f"btn_del_{v_id}"):
                            st.session_state[confirm_key] = True
                            st.rerun()
                    else:
                        st.warning("Tem certeza?")
                        col_yes, col_no = st.columns(2)
                        if col_yes.button("Sim", key=f"yes_del_{v_id}"):
                            with st.spinner("Excluindo veículo..."):
                                _, err_del = api_request("DELETE", f"/vehicle/{v_id}", base_url=XANO_VEHICLES_URL)
                                if err_del:
                                    if "404" in err_del:
                                        st.warning("⚠️ O endpoint DELETE /vehicle/{id} ainda não existe no Xano.")
                                    else:
                                        st.error(err_del)
                                else:
                                    st.toast("Veículo excluído com sucesso!", icon=":material/delete:")
                                    st.session_state[confirm_key] = False
                                    st.cache_data.clear() if hasattr(st, "cache_data") else None
                                    st.rerun()
                        if col_no.button("Não", key=f"no_del_{v_id}"):
                            st.session_state[confirm_key] = False
                            st.rerun()

# --- TELAS FUTURAS (PLACEHOLDERS) ---
def page_consult_reservations():
    st.header("🅿️ Consultar & Reservar Vagas")
    st.info("🚧 Funcionalidade em desenvolvimento. Disponível em breve.")

def page_my_reservations():
    st.header("📋 Minhas Reservas")
    st.info("🚧 Funcionalidade em desenvolvimento. Disponível em breve.")

@st.dialog("Editar Local")
def edit_location_dialog(loc_id, loc_name, loc_address, loc_desc):
    ed_name = st.text_input("Nome", value=loc_name)
    ed_addr = st.text_input("Endereço", value=loc_address)
    ed_desc = st.text_area("Descrição", value=loc_desc)
    st.write("")
    if st.button("Salvar", type="primary", use_container_width=True):
        _, err_ed_l = api_request("PUT", f"/location/{loc_id}", {"id": loc_id, "name": ed_name, "address": ed_addr, "description": ed_desc})
        if err_ed_l:
            st.error(err_ed_l)
        else:
            st.toast("Local atualizado com sucesso!", icon=":material/check_circle:")
            st.rerun()

@st.dialog("Editar Vaga")
def edit_vaga_dialog(vaga_id, location_id, vaga_numero, vaga_tipo, vaga_status):
    ev_num = st.text_input("Número", value=vaga_numero)
    ev_tipo = st.selectbox("Tipo", ["carro", "moto", "pcd", "eletrico"], index=["carro", "moto", "pcd", "eletrico"].index(vaga_tipo) if vaga_tipo in ["carro", "moto", "pcd", "eletrico"] else 0)
    ev_status = st.selectbox("Status", ["livre", "ocupada", "reservada"], index=["livre", "ocupada", "reservada"].index(vaga_status) if vaga_status in ["livre", "ocupada", "reservada"] else 0)
    st.write("")
    if st.button("Salvar", type="primary", use_container_width=True):
        if not ev_num:
            st.error("Informe o número da vaga.")
        else:
            _, err_ev = api_request("PUT", f"/vaga/{vaga_id}", {"location_id": location_id, "numero": ev_num, "tipo": ev_tipo, "status": ev_status})
            if err_ev:
                st.error(err_ev)
            else:
                st.toast("Vaga atualizada!", icon=":material/check_circle:")
                st.rerun()

@st.dialog("Editar Tarifa")
def edit_tarifa_dialog(rate_id, location_id, rate_tipo, rate_valor):
    er_tipo = st.selectbox("Tipo", ["carro", "moto", "pcd", "eletrico"], index=["carro", "moto", "pcd", "eletrico"].index(rate_tipo) if rate_tipo in ["carro", "moto", "pcd", "eletrico"] else 0)
    er_val = st.number_input("Valor/Hora", min_value=0.0, value=float(rate_valor), step=0.5)
    st.write("")
    if st.button("Salvar", type="primary", use_container_width=True):
        if er_val <= 0:
            st.error("O valor da hora deve ser maior que zero.")
        else:
            _, err_er = api_request("PUT", f"/tarifa/{rate_id}", {"location_id": location_id, "tipo_vaga": er_tipo, "valor_hora": er_val})
            if err_er:
                st.error(err_er)
            else:
                st.toast("Tarifa atualizada!", icon=":material/check_circle:")
                st.rerun()

def page_admin_locations():
    st.header("🏢 Locais & Vagas")
    if st.session_state.user_role != "admin":
        st.error("Acesso restrito a administradores.")
        return

    locations, err = api_request("GET", "/location")
    
    with st.expander(":material/add_circle: Adicionar Local", expanded=not locations):
        with st.form("add_location", clear_on_submit=True):
            loc_name = st.text_input("Nome do Local", placeholder="Estacionamento Central").strip()
            loc_address = st.text_input("Endereço", placeholder="Rua Principal, 123").strip()
            loc_desc = st.text_area("Descrição", placeholder="Estacionamento coberto 24h").strip()
            submitted_loc = st.form_submit_button("Salvar Local", type="primary")
            if submitted_loc:
                if not loc_name or not loc_address:
                    st.error("Preencha nome e endereço.")
                else:
                    _, err_loc = api_request("POST", "/location", {"name": loc_name, "address": loc_address, "description": loc_desc})
                    if err_loc:
                        st.error(err_loc)
                    else:
                        st.toast("Local cadastrado com sucesso!", icon=":material/check_circle:")
                        st.rerun()

    st.subheader("Locais Cadastrados")
    if err:
        st.error(err)
    elif not locations:
        st.info("Nenhum local cadastrado.")
    else:
        loc_options = {loc["name"]: loc["id"] for loc in locations}
        selected_loc_name = st.selectbox("Selecione o Local para gerenciar Vagas", list(loc_options.keys()))
        selected_loc_id = loc_options[selected_loc_name]

        col_l1, col_l2, col_l3 = st.columns([2, 1, 1])
        with col_l1:
            loc_data = next((l for l in locations if l["id"] == selected_loc_id), {})
            st.markdown(f"**Endereço:** {loc_data.get('address')}  \n**Descrição:** {loc_data.get('description', '-')}")
        with col_l2:
            if st.button("Excluir Local", type="secondary"):
                _, err_del = api_request("DELETE", f"/location/{selected_loc_id}")
                if err_del:
                    st.error(err_del)
                else:
                    st.toast("Local excluído com sucesso!", icon=":material/delete:")
                    st.rerun()
        with col_l3:
            if st.button("Editar Local", type="secondary"):
                edit_location_dialog(selected_loc_id, loc_data.get("name", ""), loc_data.get("address", ""), loc_data.get("description", ""))

        st.divider()
        st.subheader(f"Vagas em {selected_loc_name}")
        
        vagas, err_v = api_request("GET", f"/vaga?location_id={selected_loc_id}")
        
        with st.form("add_vaga", clear_on_submit=True):
            v_col1, v_col2 = st.columns(2)
            with v_col1:
                v_numero = st.text_input("Número/Código da Vaga", placeholder="A01").strip()
            with v_col2:
                v_tipo_disp = st.selectbox("Tipo de Vaga", ["carro", "moto", "pcd", "eletrico"])
            
            submitted_vaga = st.form_submit_button("Adicionar Vaga", type="primary")
            if submitted_vaga:
                if not v_numero:
                    st.error("Informe o número da vaga.")
                else:
                    _, err_add_v = api_request("POST", "/vaga", {"location_id": selected_loc_id, "numero": v_numero, "tipo": v_tipo_disp})
                    if err_add_v:
                        st.error(err_add_v)
                    else:
                        st.toast("Vaga adicionada com sucesso!", icon=":material/check_circle:")
                        st.rerun()

        if err_v:
            st.error(err_v)
        elif not vagas:
            st.info("Nenhuma vaga cadastrada neste local.")
        else:
            for vaga in vagas:
                col_v1, col_v2, col_v3, col_v4 = st.columns([2, 2, 1, 1])
                with col_v1:
                    st.markdown(f"Vaga: **{vaga.get('numero')}**")
                with col_v2:
                    st.markdown(f"Tipo: `{vaga.get('tipo')}` | Status: `{vaga.get('status')}`")
                with col_v3:
                    if st.button("Excluir", key=f"del_vaga_{vaga.get('id')}"):
                        _, err_dv = api_request("DELETE", f"/vaga/{vaga.get('id')}")
                        if err_dv:
                            st.error(err_dv)
                        else:
                            st.toast("Vaga excluída!", icon=":material/delete:")
                            st.rerun()
                with col_v4:
                    if st.button("Editar", key=f"edit_vaga_btn_{vaga.get('id')}"):
                        edit_vaga_dialog(vaga.get('id'), selected_loc_id, vaga.get("numero", ""), vaga.get("tipo", "carro"), vaga.get("status", "livre"))

def page_admin_rates():
    st.header("💲 Tarifas")
    if st.session_state.user_role != "admin":
        st.error("Acesso restrito a administradores.")
        return

    locations, err_l = api_request("GET", "/location")
    if err_l or not locations:
        st.info("Cadastre locais antes de definir tarifas.")
        return

    loc_options = {loc["name"]: loc["id"] for loc in locations}
    selected_loc_name = st.selectbox("Local", list(loc_options.keys()), key="rate_loc_sel")
    selected_loc_id = loc_options[selected_loc_name]

    rates, err_r = api_request("GET", f"/tarifa?location_id={selected_loc_id}")

    with st.form("add_rate", clear_on_submit=True):
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            r_tipo = st.selectbox("Tipo de Vaga", ["carro", "moto", "pcd", "eletrico"], key="rate_tipo_sel")
        with r_col2:
            r_valor = st.number_input("Valor por Hora (R$)", min_value=0.0, value=10.0, step=0.5)
        
        submitted_rate = st.form_submit_button("Salvar Tarifa", type="primary")
        if submitted_rate:
            if r_valor <= 0:
                st.error("O valor da hora deve ser maior que zero.")
            else:
                _, err_ar = api_request("POST", "/tarifa", {"location_id": selected_loc_id, "tipo_vaga": r_tipo, "valor_hora": r_valor})
                if err_ar:
                    st.error(err_ar)
                else:
                    st.toast("Tarifa salva com sucesso!", icon=":material/check_circle:")
                    st.rerun()

    st.subheader(f"Tarifas cadastradas para {selected_loc_name}")
    if err_r:
        st.error(err_r)
    elif not rates:
        st.info("Nenhuma tarifa cadastrada para este local.")
    else:
        for rate in rates:
            col_r1, col_r2, col_r3, col_r4 = st.columns([2, 2, 1, 1])
            with col_r1:
                st.markdown(f"Tipo: **{rate.get('tipo_vaga')}**")
            with col_r2:
                st.markdown(f"Valor/Hora: **R$ {rate.get('valor_hora'):.2f}**")
            with col_r3:
                if st.button("Excluir", key=f"del_rate_{rate.get('id')}"):
                    _, err_dr = api_request("DELETE", f"/tarifa/{rate.get('id')}")
                    if err_dr:
                        st.error(err_dr)
                    else:
                        st.toast("Tarifa excluída!", icon=":material/delete:")
                        st.rerun()
            with col_r4:
                if st.button("Editar", key=f"edit_rate_btn_{rate.get('id')}"):
                    edit_tarifa_dialog(rate.get('id'), selected_loc_id, rate.get("tipo_vaga", "carro"), rate.get("valor_hora", 10.0))

def page_admin_reservations():
    st.header("📊 Todas as Reservas")
    st.info("🚧 Funcionalidade em desenvolvimento. Disponível em breve.")

# --- CONTROLE DE FLUXO PRINCIPAL E SIDEBAR (A, B) ---
if not st.session_state.token:
    auth_page()
else:
    email = st.session_state.user_email or "usuario@email.com"
    initial = email[0].upper() if email else "U"
    role = st.session_state.user_role
    
    if role == "admin":
        badge_html = "<span style='background-color:#ef4444; color:white; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:600;'>Administrador</span>"
    else:
        badge_html = "<span style='background-color:#3b82f6; color:white; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:600;'>Cliente</span>"
        
    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
            <div style="background-color: #22c55e; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.1rem; flex-shrink: 0;">
                {initial}
            </div>
            <div style="overflow: hidden; text-overflow: ellipsis; width: 100%;">
                <p style="margin: 0; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 0.92rem;" title="{email}">{email}</p>
                <div style="margin-top: 3px;">{badge_html}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    
    if role == "admin":
        menu_options = ["Locais & Vagas", "Tarifas", "Meus Veículos"]
    else:
        menu_options = ["Meus Veículos"]
            
    if len(menu_options) > 1:
        st.sidebar.markdown("### Navegação")
        selected_page = st.sidebar.radio(
            "Selecione",
            menu_options,
            format_func=lambda x: (
                ":material/domain: Locais & Vagas" if x == "Locais & Vagas" else
                ":material/payments: Tarifas" if x == "Tarifas" else
                ":material/directions_car: Meus Veículos" if "Veículos" in x else
                f":material/menu: {x}"
            ),
            label_visibility="collapsed"
        )
    else:
        selected_page = menu_options[0]
        st.sidebar.markdown(f":material/directions_car: **{selected_page}**")
    
    st.sidebar.divider()
    if st.sidebar.button(":material/logout: Sair", use_container_width=True):
        st.session_state.token = None
        st.session_state.user_role = None
        st.session_state.user_email = None
        st.rerun()

    if selected_page == "Meus Veículos" or selected_page == "🚘 Meus Veículos":
        page_my_vehicles()
    elif selected_page == "Consultar & Reservar":
        page_consult_reservations()
    elif selected_page == "Minhas Reservas":
        page_my_reservations()
    elif selected_page == "Locais & Vagas":
        page_admin_locations()
    elif selected_page == "Tarifas":
        page_admin_rates()
    elif selected_page == "Todas as Reservas":
        page_admin_reservations()
