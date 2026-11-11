import streamlit as st
import requests
import os
import re
import html
from datetime import datetime, timedelta
from dotenv import load_dotenv
from ui.theme import apply_theme, render_status_badge, render_metric_card, render_plate, render_empty_state

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def format_timestamp(ts):
    if not ts:
        return "-"
    try:
        if isinstance(ts, (int, float)) or (isinstance(ts, str) and ts.isdigit()):
            val = float(ts)
            if val > 1e11:
                val = val / 1000.0
            dt = datetime.fromtimestamp(val)
        elif isinstance(ts, str):
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            return str(ts)
        
        if ZoneInfo:
            try:
                dt = dt.astimezone(ZoneInfo("America/Sao_Paulo"))
            except Exception:
                pass
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return str(ts)

# 13. Configuração da página chamada uma única vez no topo
st.set_page_config(
    page_title="Estacionamento Smart",
    page_icon="🚗",
    layout="wide"
)

apply_theme()

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
    if "nav_index" not in st.session_state:
        st.session_state.nav_index = 0

init_session()

def api_request(method, endpoint, data=None, auth=True, base_url=None):
    headers = {}
    if auth and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    if not base_url:
        if endpoint.startswith("/location") or endpoint.startswith("/vaga") or endpoint.startswith("/tarifa") or endpoint.startswith("/reservation") or endpoint.startswith("/admin/reservation"):
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
            if not response.text.strip():
                return {}, None
            try:
                return response.json(), None
            except Exception:
                return {"raw": response.text}, None
        elif response.status_code in [401, 403]:
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
                err_msg = msg if msg else str(err_json)
            except:
                err_msg = response.text
            return None, f"Erro ({response.status_code}): {err_msg}"
    except Exception as e:
        return None, f"Erro de conexão: {str(e)}"

# --- TELA DE LOGIN / CADASTRO (C) (Original) ---
def auth_page():
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

def fetch_user_vehicles():
    return api_request("GET", "/vehicle", base_url=XANO_VEHICLES_URL)

@st.dialog("Editar Veículo")
def edit_vehicle_dialog(v_id, v_plate, v_brand, v_model, v_color, v_year, v_type):
    ed_plate = st.text_input("Placa", value=v_plate).strip().upper()
    ed_brand = st.text_input("Marca", value=v_brand).strip()
    ed_model = st.text_input("Modelo", value=v_model).strip()
    ed_color = st.text_input("Cor", value=v_color).strip()
    current_year = datetime.now().year
    ed_year = st.number_input("Ano", min_value=1980, max_value=current_year + 1, value=int(v_year) if v_year else current_year, step=1)
    ed_type = st.selectbox("Tipo", ["carro", "moto", "pcd"], index=["carro", "moto", "pcd"].index(v_type) if v_type in ["carro", "moto", "pcd"] else 0)
    
    st.write("")
    if st.button("Salvar Alterações", type="primary", use_container_width=True):
        plate_clean = ed_plate.replace("-", "").strip()
        pattern_old = r"^[A-Z]{3}[0-9]{4}$"
        pattern_mercosul = r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$"
        
        if not plate_clean or not ed_brand or not ed_model or not ed_color:
            st.error("Preencha todos os campos obrigatórios.")
        elif not (re.match(pattern_old, plate_clean) or re.match(pattern_mercosul, plate_clean)):
            st.error("Formato de placa inválido (use ABC1234 ou ABC1D23).")
        else:
            payload = {
                "id": v_id,
                "plate": ed_plate,
                "brand": ed_brand,
                "model": ed_model,
                "color": ed_color,
                "year": int(ed_year),
                "type": ed_type
            }
            _, err_up = api_request("PUT", f"/vehicle/{v_id}", payload, base_url=XANO_VEHICLES_URL)
            if err_up:
                st.error(err_up)
            else:
                st.toast("Veículo atualizado com sucesso!", icon=":material/check_circle:")
                st.rerun()

@st.dialog("Confirmar Exclusão")
def confirm_delete_vehicle_dialog(v_id):
    st.warning("Tem certeza que deseja excluir este veículo? Esta ação não pode ser desfeita.")
    col_y, col_n = st.columns(2)
    if col_y.button("Sim, Excluir", type="primary", use_container_width=True):
        _, err_del = api_request("DELETE", f"/vehicle/{v_id}", base_url=XANO_VEHICLES_URL)
        if err_del:
            st.error(err_del)
        else:
            st.toast("Veículo excluído com sucesso!", icon=":material/delete:")
            st.rerun()
    if col_n.button("Cancelar", use_container_width=True):
        st.rerun()

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
        vehicles, err = fetch_user_vehicles()
    
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
                elif year < 1980 or year > current_year + 1:
                    st.error(f"Ano inválido. Deve estar entre 1980 e {current_year + 1}.")
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
        st.info("Você ainda não cadastrou veículos.")
        if st.button("Cadastrar Primeiro Veículo", type="primary"):
            st.rerun()
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
            m1.metric("Total", total_v, delta=None, border=True)
            m2.metric("Carros", total_carro, delta=None, border=True)
            m3.metric("Motos", total_moto, delta=None, border=True)
            m4.metric("PCD", total_pcd, delta=None, border=True)
        
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
                    st.markdown(f"<div class='plate-box'>{v_plate}</div>", unsafe_allow_html=True)
                    st.markdown(f"Cor: {v_color.title()} &nbsp;|&nbsp; Ano: {v_year} &nbsp;|&nbsp; {type_badge}", unsafe_allow_html=True)
                    st.write("")
                    
                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        if st.button("Editar", key=f"btn_edit_veh_{v_id}", use_container_width=True):
                            edit_vehicle_dialog(v_id, v_plate, v_brand, v_model, v_color, v_year, v_type_val)
                    with col_act2:
                        if st.button("Excluir", key=f"btn_del_veh_{v_id}", use_container_width=True):
                            confirm_delete_vehicle_dialog(v_id)

def fetch_slot_map_cached_data(location_id, vehicle_id, start_time_str, end_time_str, force_refresh=False):
    import time
    cache_key = (location_id, vehicle_id, start_time_str, end_time_str)
    if "slot_map_cache" not in st.session_state:
        st.session_state.slot_map_cache = {}
    
    cached = st.session_state.slot_map_cache.get(cache_key)
    now = time.time()
    
    if not force_refresh and cached and (now - cached.get("timestamp", 0) < 60):
        return cached.get("slots"), cached.get("avail"), cached.get("reservations"), None
        
    slots, err_slots = api_request("GET", f"/vaga?location_id={location_id}")
    if err_slots:
        return None, None, None, err_slots
        
    avail_url = f"/reservation/availability?location_id={location_id}&vehicle_id={vehicle_id}&start_time={start_time_str}&end_time={end_time_str}"
    avail, err_avail = api_request("GET", avail_url)
    if err_avail:
        return None, None, None, err_avail
        
    reservations, err_res = api_request("GET", "/reservation")
    if err_res:
        return None, None, None, err_res
        
    st.session_state.slot_map_cache[cache_key] = {
        "timestamp": now,
        "slots": slots,
        "avail": avail,
        "reservations": reservations
    }
    return slots, avail, reservations, None

def page_consult_reservations():
    st.header("🅿️ Consultar & Reservar Vagas")
    
    locations, err_loc = api_request("GET", "/location")
    if err_loc:
        st.error(err_loc)
        return
    if not locations:
        st.info("Nenhum local cadastrado ou disponível no momento.")
        return

    loc_options = {loc["name"]: loc["id"] for loc in locations}
    selected_loc_name = st.selectbox("Selecione o Local", list(loc_options.keys()))
    selected_loc_id = loc_options[selected_loc_name]

    vehicles, err_veh = fetch_user_vehicles()
    if err_veh:
        st.error(err_veh)
        return
    if not vehicles:
        st.warning("Você precisa cadastrar pelo menos um veículo em 'Meus Veículos' antes de fazer reservas.")
        return

    veh_options = {f"{v.get('brand')} {v.get('model')} ({v.get('plate')}) - {v.get('type') if v.get('type') else 'tipo não informado'}": v for v in vehicles}
    selected_veh_label = st.selectbox("Selecione o Veículo", list(veh_options.keys()))
    selected_veh = veh_options[selected_veh_label]

    now = datetime.now()
    default_end = now + timedelta(hours=1)

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        start_date = st.date_input("Data de Início", value=now.date())
        start_time = st.time_input("Horário de Início", value=now.time())
    with col_d2:
        end_date = st.date_input("Data de Término", value=default_end.date())
        end_time = st.time_input("Horário de Término", value=default_end.time())

    start_dt = datetime.combine(start_date, start_time)
    end_dt = datetime.combine(end_date, end_time)

    # Fetch rates for estimation
    rates, _ = api_request("GET", f"/tarifa?location_id={selected_loc_id}")
    rate_val = 10.0
    if rates:
        match_rate = next((r for r in rates if r.get('tipo_vaga') == selected_veh.get('type')), None)
        if match_rate:
            rate_val = float(match_rate.get('valor_hora', 10.0))

    duration_hours = max(0.5, (end_dt - start_dt).total_seconds() / 3600.0)
    estimated_price = duration_hours * rate_val

    st.info(f"💰 **Preço estimado:** R$ {estimated_price:.2f} (Base: R$ {rate_val:.2f}/h para {duration_hours:.1f}h)")

    if "slot_map_consultation" not in st.session_state:
        st.session_state.slot_map_consultation = {
            "location_id": None,
            "vehicle_id": None,
            "start_time": None,
            "end_time": None,
            "slots": None,
            "avail": None,
            "reservations": None
        }

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        consult_clicked = st.button("Consultar Disponibilidade", type="primary")
    with col_btn2:
        refresh_clicked = st.button("Atualizar", use_container_width=True)

    if consult_clicked or refresh_clicked:
        if start_dt < datetime.now() - timedelta(minutes=1):
            st.error("O horário de início não pode ser no passado.")
        elif end_dt <= start_dt:
            st.error("O horário de término deve ser posterior ao horário de início.")
        else:
            with st.spinner("Buscando dados do mapa de vagas..."):
                start_iso = start_dt.isoformat()
                end_iso = end_dt.isoformat()
                slots, avail, reservations, err_msg = fetch_slot_map_cached_data(
                    selected_loc_id, selected_veh.get("id"), start_iso, end_iso, force_refresh=refresh_clicked
                )
                if err_msg:
                    st.error(f"Erro ao carregar dados: {err_msg}")
                    st.session_state.slot_map_consultation = {
                        "location_id": None, "vehicle_id": None, "start_time": None, "end_time": None,
                        "slots": None, "avail": None, "reservations": None
                    }
                else:
                    st.session_state.slot_map_consultation = {
                        "location_id": selected_loc_id,
                        "vehicle_id": selected_veh.get("id"),
                        "start_time": start_iso,
                        "end_time": end_iso,
                        "slots": slots,
                        "avail": avail,
                        "reservations": reservations
                    }

    consult_data = st.session_state.slot_map_consultation
    if consult_data.get("slots") is not None and consult_data.get("avail") is not None and consult_data.get("reservations") is not None:
        slots = consult_data["slots"]
        avail = consult_data["avail"]
        reservations = consult_data["reservations"]
        st.success(f"Consulta carregada! Total de vagas: {len(slots)} | Livres: {len(avail) if isinstance(avail, list) else 0}")
        
        st.subheader("Grid de Vagas Disponíveis")
        if not avail:
            st.info("Nenhuma vaga disponível para este período e tipo de veículo.")
        else:
            grid_cols = st.columns(4)
            for idx, vaga in enumerate(avail):
                g_col = grid_cols[idx % 4]
                with g_col:
                    with st.container(border=True):
                        st.markdown(f"#### 🅿️ {vaga.get('numero')}")
                        st.caption(f"Tipo: {vaga.get('tipo', '').upper()}")
                        if st.button("Reservar", key=f"book_grid_{vaga.get('id')}", use_container_width=True):
                            payload = {
                                "location_id": consult_data["location_id"],
                                "vaga_id": vaga.get("id"),
                                "vehicle_id": consult_data["vehicle_id"],
                                "start_time": consult_data["start_time"],
                                "end_time": consult_data["end_time"]
                            }
                            with st.spinner("Confirmando reserva..."):
                                res_data, err_book = api_request("POST", "/reservation", payload)
                                if err_book:
                                    st.error(f"Erro ao realizar reserva: {err_book}")
                                elif not isinstance(res_data, dict) or not res_data.get("id"):
                                    st.error(f"Erro: A resposta da API não retornou o ID da reserva. Resposta: {res_data}")
                                else:
                                    res_id = res_data.get('id')
                                    st.session_state.success_message = f"Reserva #{res_id} realizada com sucesso!"
                                    st.session_state.last_created_res_id = res_id
                                    st.session_state.slot_map_consultation = {
                                        "location_id": None, "vehicle_id": None, "start_time": None, "end_time": None,
                                        "slots": None, "avail": None, "reservations": None
                                    }
                                    st.session_state.nav_index = 2
                                    st.rerun()

@st.dialog("🎟️ Ticket de Reserva")
def view_ticket_dialog(res_id):
    now_ts = datetime.now().timestamp()
    cache_key = f"ticket_cache_{res_id}"
    cache_time_key = f"ticket_cache_time_{res_id}"
    
    ticket_data = None
    if cache_key in st.session_state and cache_time_key in st.session_state:
        if now_ts - st.session_state[cache_time_key] < 60:
            ticket_data = st.session_state[cache_key]
            
    if not ticket_data:
        with st.spinner("Carregando detalhes do ticket..."):
            data, err = api_request("GET", f"/reservation/{res_id}/ticket")
            if err or not isinstance(data, dict):
                st.error("Não foi possível carregar o ticket")
                if st.button("Fechar"):
                    st.rerun()
                return
            
            required_fields = ["ticket_code", "status", "location_name", "vaga_numero", "vehicle_plate"]
            if not all(data.get(f) for f in required_fields):
                st.error("Não foi possível carregar o ticket")
                if st.button("Fechar"):
                    st.rerun()
                return

            ticket_data = data
            st.session_state[cache_key] = ticket_data
            st.session_state[cache_time_key] = now_ts

    t_code = ticket_data.get('ticket_code', '-')
    raw_client = ticket_data.get('client_name', '-')
    client = raw_client.split('@')[0] if '@' in raw_client else raw_client
    plate = ticket_data.get('vehicle_plate', '-')
    loc = ticket_data.get('location_name', '-')
    vaga = ticket_data.get('vaga_numero', '-')
    start_fmt = format_timestamp(ticket_data.get('start_time'))
    end_fmt = format_timestamp(ticket_data.get('end_time'))
    price = ticket_data.get('total_price', ticket_data.get('price', 0.0))
    status = ticket_data.get('status', 'ativa')
    issued_at_fmt = format_timestamp(ticket_data.get('issued_at', datetime.now().isoformat()))

    st.markdown(f"""
    <div style="border: 2px dashed #22c55e; padding: 20px; border-radius: 8px; background: #0b130e; color: #f9fafb;">
        <div style="text-align: center; border-bottom: 1px solid rgba(34,197,94,0.3); padding-bottom: 10px; margin-bottom: 15px;">
            <h3 style="margin: 0; color: #22c55e;">Estacionamento Smart</h3>
            <p style="margin: 5px 0 0 0; font-size: 0.85rem; color: #9ca3af;">Código do Ticket</p>
            <div style="font-size: 26px; font-weight: bold; color: #22c55e; font-family: monospace; letter-spacing: 2px;">{html.escape(str(t_code))}</div>
        </div>
        <div style="font-size: 0.95rem; line-height: 1.6;">
            <p style="margin: 4px 0;"><strong>👤 Cliente:</strong> {html.escape(str(client))}</p>
            <p style="margin: 4px 0;"><strong>🚗 Veículo (Placa):</strong> <span class="plate-box">{html.escape(str(plate))}</span></p>
            <p style="margin: 4px 0;"><strong>📍 Local:</strong> {html.escape(str(loc))}</p>
            <p style="margin: 4px 0;"><strong>🅿️ Vaga:</strong> {html.escape(str(vaga))}</p>
            <p style="margin: 4px 0;"><strong>🕒 Início:</strong> {start_fmt}</p>
            <p style="margin: 4px 0;"><strong>🕒 Término:</strong> {end_fmt}</p>
            <p style="margin: 4px 0;"><strong>💵 Preço Total:</strong> R$ {price:.2f}</p>
            <p style="margin: 4px 0;"><strong>📊 Status:</strong> {render_status_badge(status)}</p>
        </div>
        <div style="text-align: center; font-size: 11px; color: #9ca3af; margin-top: 15px; border-top: 1px solid rgba(34,197,94,0.3); padding-top: 8px;">
            Emitido em: {issued_at_fmt}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    html_download_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Ticket de Reserva - {html.escape(str(t_code))}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #111; }}
        .ticket {{ border: 2px dashed #22c55e; padding: 20px; border-radius: 8px; max-width: 600px; margin: auto; background: #f9fafb; }}
        .header {{ text-align: center; border-bottom: 1px solid #ddd; padding-bottom: 10px; margin-bottom: 20px; }}
        .code {{ font-size: 24px; font-weight: bold; color: #22c55e; font-family: monospace; }}
        .details {{ margin-bottom: 15px; line-height: 1.6; }}
        .footer {{ text-align: center; font-size: 12px; color: #666; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 10px; }}
        @media print {{
            body {{ margin: 0; }}
            .ticket {{ border: 2px solid #000; box-shadow: none; width: 100%; max-width: none; }}
        }}
    </style>
</head>
<body>
    <div class="ticket">
        <div class="header">
            <h2>Estacionamento Smart - Ticket de Reserva</h2>
            <div class="code">{html.escape(str(t_code))}</div>
        </div>
        <div class="details">
            <p><strong>Cliente:</strong> {html.escape(str(client))}</p>
            <p><strong>Veículo (Placa):</strong> {html.escape(str(plate))}</p>
            <p><strong>Local:</strong> {html.escape(str(loc))}</p>
            <p><strong>Vaga:</strong> {html.escape(str(vaga))}</p>
            <p><strong>Início:</strong> {start_fmt}</p>
            <p><strong>Término:</strong> {end_fmt}</p>
            <p><strong>Preço Total:</strong> R$ {price:.2f}</p>
            <p><strong>Status:</strong> {html.escape(str(status))}</p>
        </div>
        <div class="footer">
            <p>Emitido em: {issued_at_fmt}</p>
        </div>
    </div>
</body>
</html>"""

    st.download_button(
        label="📥 Baixar ticket",
        data=html_download_content,
        file_name=f"ticket-{t_code}.html",
        mime="text/html",
        use_container_width=True
    )

def parse_timestamp_to_datetime(ts):
    if not ts:
        return None
    try:
        val = float(ts)
        if val > 1e11:
            val = val / 1000.0
        if ZoneInfo:
            try:
                return datetime.fromtimestamp(val, tz=ZoneInfo("America/Sao_Paulo"))
            except Exception:
                pass
        return datetime.fromtimestamp(val)
    except Exception:
        return None

def calculate_reservation_status(raw_status, start_ts, end_ts):
    if raw_status and str(raw_status).strip().lower() in ["cancelada", "cancelado"]:
        return "Cancelado"
    
    start_dt = parse_timestamp_to_datetime(start_ts)
    end_dt = parse_timestamp_to_datetime(end_ts)
    
    if ZoneInfo:
        try:
            agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
        except Exception:
            agora = datetime.now()
    else:
        agora = datetime.now()
        
    if not start_dt or not end_dt:
        s = str(raw_status or "válido").strip().capitalize()
        return s if s in ["Válido", "Em andamento", "Expirado", "Cancelado"] else "Válido"
        
    if agora < start_dt:
        return "Válido"
    elif start_dt <= agora < end_dt:
        return "Em andamento"
    else:
        return "Expirado"

def get_my_reservations_lookup_data():
    now_ts = datetime.now().timestamp()
    if "my_res_lookup_cache" in st.session_state and "my_res_lookup_time" in st.session_state:
        if now_ts - st.session_state["my_res_lookup_time"] < 60:
            return st.session_state["my_res_lookup_cache"]
    
    locations, _ = api_request("GET", "/location")
    vagas, _ = api_request("GET", "/vaga")
    vehicles, _ = fetch_user_vehicles()
    
    loc_map = {item["id"]: item for item in (locations or []) if isinstance(item, dict) and "id" in item}
    vaga_map = {item["id"]: item for item in (vagas or []) if isinstance(item, dict) and "id" in item}
    veh_map = {item["id"]: item for item in (vehicles or []) if isinstance(item, dict) and "id" in item}
    
    cache = {"loc_map": loc_map, "vaga_map": vaga_map, "veh_map": veh_map}
    st.session_state["my_res_lookup_cache"] = cache
    st.session_state["my_res_lookup_time"] = now_ts
    return cache

@st.dialog("Confirmar Cancelamento")
def confirm_cancel_dialog(res_id):
    st.warning(f"Tem certeza que deseja cancelar a reserva #{res_id}?")
    col_y, col_n = st.columns(2)
    if col_y.button("Sim, Cancelar", type="primary", use_container_width=True):
        _, err_del = api_request("DELETE", f"/reservation/{res_id}")
        if err_del:
            st.error(err_del)
        else:
            cache_key = f"ticket_cache_{res_id}"
            cache_time_key = f"ticket_cache_time_{res_id}"
            if cache_key in st.session_state:
                del st.session_state[cache_key]
            if cache_time_key in st.session_state:
                del st.session_state[cache_time_key]
            if "my_res_lookup_cache" in st.session_state:
                del st.session_state["my_res_lookup_cache"]
            st.toast("Reserva cancelada com sucesso!", icon=":material/check_circle:")
            st.rerun()
    if col_n.button("Voltar", use_container_width=True):
        st.rerun()

def page_my_reservations():
    st.header(":material/receipt_long: Minhas Reservas")

    if "success_message" in st.session_state and st.session_state.success_message:
        st.success(st.session_state.success_message)
        if "last_created_res_id" in st.session_state and st.session_state.last_created_res_id:
            if st.button("🎟️ Ver Ticket da Nova Reserva", type="primary"):
                view_ticket_dialog(st.session_state.last_created_res_id)
        st.session_state.success_message = None

    reservations, err = api_request("GET", "/reservation")
    if err:
        st.error(err)
    elif not reservations:
        st.info("Você ainda não possui reservas cadastradas.")
        if st.button("Fazer Primeira Reserva", type="primary"):
            st.session_state.nav_index = 1
            st.rerun()
    else:
        lookup = get_my_reservations_lookup_data()
        
        processed_res = []
        for r in reservations:
            r_copy = dict(r)
            calc_status = calculate_reservation_status(r.get('status'), r.get('start_time'), r.get('end_time'))
            r_copy['calculated_status'] = calc_status
            
            loc_id = r.get('location_id')
            loc_item = lookup["loc_map"].get(loc_id)
            loc_name = loc_item.get('name') if loc_item else r.get('location_name', '—')
            r_copy['resolved_location'] = loc_name if loc_name else '—'
            
            vaga_id = r.get('vaga_id')
            vaga_item = lookup["vaga_map"].get(vaga_id)
            vaga_num = vaga_item.get('numero', vaga_item.get('number')) if vaga_item else r.get('vaga_numero', '—')
            r_copy['resolved_vaga'] = str(vaga_num) if vaga_num is not None else '—'
            
            veh_id = r.get('vehicle_id')
            veh_item = lookup["veh_map"].get(veh_id)
            if veh_item:
                v_model = veh_item.get('model', '')
                v_plate = veh_item.get('plate', '')
                veh_str = f"{v_model} ({v_plate})".strip() if (v_model or v_plate) else '—'
            else:
                vm = r.get('vehicle_model', '')
                vp = r.get('vehicle_plate', '')
                veh_str = f"{vm} ({vp})".strip() if (vm or vp) else '—'
            r_copy['resolved_vehicle'] = veh_str if veh_str else '—'
            
            processed_res.append(r_copy)

        processed_res.sort(key=lambda x: x.get('id', 0), reverse=True)
        
        active_res = [r for r in processed_res if r['calculated_status'] in ["Válido", "Em andamento"]]
        history_res = [r for r in processed_res if r['calculated_status'] in ["Expirado", "Cancelado"]]

        tab_active, tab_history = st.tabs([f"Ativas ({len(active_res)})", f"Histórico ({len(history_res)})"])

        badge_color_map = {
            "Válido": "blue",
            "Em andamento": "green",
            "Expirado": "gray",
            "Cancelado": "red"
        }

        with tab_active:
            if not active_res:
                st.info("Nenhuma reserva ativa no momento.")
            else:
                for r in active_res:
                    with st.container(border=True):
                        col_r1, col_r2 = st.columns([3, 1])
                        with col_r1:
                            stat = r['calculated_status']
                            st.badge(stat, color=badge_color_map.get(stat, "blue"), icon=":material/info:")
                            st.markdown(f"**Reserva #{r.get('id')}**")
                            start_fmt = format_timestamp(r.get('start_time'))
                            end_fmt = format_timestamp(r.get('end_time'))
                            st.caption(f"🕒 Início: {start_fmt} | Término: {end_fmt}")
                            st.text(f"Local: {r['resolved_location']} | Vaga: {r['resolved_vaga']} | Veículo: {r['resolved_vehicle']}")
                            price = r.get('price', r.get('total_price', 0))
                            st.caption(f"💵 Preço: R$ {price:.2f}")
                        with col_r2:
                            st.write("")
                            if st.button("🎟️ Ver Ticket", key=f"ticket_res_{r.get('id')}", use_container_width=True):
                                view_ticket_dialog(r.get('id'))
                            if stat in ["Válido", "Em andamento"]:
                                if st.button("Cancelar", key=f"cancel_res_{r.get('id')}", use_container_width=True):
                                    confirm_cancel_dialog(r.get('id'))

        with tab_history:
            if not history_res:
                st.info("Nenhum histórico de reservas.")
            else:
                for r in history_res:
                    with st.container(border=True):
                        col_h1, col_h2 = st.columns([3, 1])
                        with col_h1:
                            stat = r['calculated_status']
                            st.badge(stat, color=badge_color_map.get(stat, "gray"), icon=":material/history:")
                            st.markdown(f"**Reserva #{r.get('id')}**")
                            start_fmt = format_timestamp(r.get('start_time'))
                            end_fmt = format_timestamp(r.get('end_time'))
                            st.caption(f"🕒 Início: {start_fmt} | Término: {end_fmt}")
                            st.text(f"Local: {r['resolved_location']} | Vaga: {r['resolved_vaga']} | Veículo: {r['resolved_vehicle']}")
                            price = r.get('price', r.get('total_price', 0))
                            st.caption(f"💵 Preço: R$ {price:.2f}")
                        with col_h2:
                            st.write("")
                            if st.button("🎟️ Ver Ticket", key=f"ticket_hist_{r.get('id')}", use_container_width=True):
                                view_ticket_dialog(r.get('id'))

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
    if err:
        st.error(err)
        return
    
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
    if err_l:
        st.error(err_l)
        return
    if not locations:
        st.info("Nenhum local cadastrado ou disponível no momento.")
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
    if st.session_state.user_role != "admin":
        st.error("Acesso restrito a administradores.")
        return

    reservations, err = api_request("GET", "/admin/reservation")
    if err:
        st.error(err)
    elif not reservations:
        st.info("Nenhuma reserva cadastrada no sistema.")
    else:
        reservations.sort(key=lambda x: x.get('id', 0), reverse=True)
        for r in reservations:
            with st.container(border=True):
                col_a1, col_a2 = st.columns([3, 1])
                with col_a1:
                    badge = render_status_badge(r.get('status'))
                    st.markdown(f"**Reserva #{r.get('id')}** (Usuário ID: {r.get('user_id')}) &nbsp;&nbsp; {badge}", unsafe_allow_html=True)
                    start_fmt = format_timestamp(r.get('start_time'))
                    end_fmt = format_timestamp(r.get('end_time'))
                    st.markdown(f"📍 **Local:** {r.get('location_id')} | 🅿️ **Vaga:** {r.get('vaga_id')} | 🚗 **Veículo:** {r.get('vehicle_id')}")
                    st.markdown(f"🕒 **Início:** {start_fmt} | **Término:** {end_fmt} | **Preço:** R$ {r.get('price', 0):.2f}")
                with col_a2:
                    st.write("")
                    if st.button("🎟️ Ver Ticket", key=f"admin_ticket_res_{r.get('id')}", use_container_width=True):
                        view_ticket_dialog(r.get('id'))
                    if str(r.get('status')).lower() == 'ativa':
                        if st.button("Cancelar Admin", key=f"admin_cancel_res_{r.get('id')}", use_container_width=True):
                            _, err_del = api_request("DELETE", f"/admin/reservation/{r.get('id')}")
                            if err_del:
                                st.error(err_del)
                            else:
                                cache_key = f"ticket_cache_{r.get('id')}"
                                cache_time_key = f"ticket_cache_time_{r.get('id')}"
                                if cache_key in st.session_state:
                                    del st.session_state[cache_key]
                                if cache_time_key in st.session_state:
                                    del st.session_state[cache_time_key]
                                st.toast("Reserva cancelada pelo administrador!", icon=":material/check_circle:")
                                st.rerun()

# --- CONTROLE DE FLUXO PRINCIPAL E SIDEBAR ---
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
        menu_options = ["Locais & Vagas", "Tarifas", "Meus Veículos", "Todas as Reservas"]
    else:
        menu_options = ["Meus Veículos", "Reservar", "Minhas Reservas"]
            
    if len(menu_options) > 1:
        st.sidebar.markdown("### Navegação")
        if "nav_index" not in st.session_state:
            st.session_state.nav_index = 0
        if st.session_state.nav_index >= len(menu_options):
            st.session_state.nav_index = 0
            
        selected_page = st.sidebar.radio(
            "Selecione",
            menu_options,
            index=st.session_state.nav_index,
            format_func=lambda x: (
                ":material/domain: Locais & Vagas" if x == "Locais & Vagas" else
                ":material/payments: Tarifas" if x == "Tarifas" else
                ":material/directions_car: Meus Veículos" if "Veículos" in x else
                ":material/local_parking: Reservar" if x == "Reservar" else
                ":material/receipt_long: Minhas Reservas" if x == "Minhas Reservas" else
                ":material/bar_chart: Todas as Reservas" if x == "Todas as Reservas" else
                f":material/menu: {x}"
            ),
            label_visibility="collapsed"
        )
        if selected_page in menu_options:
            st.session_state.nav_index = menu_options.index(selected_page)
    else:
        selected_page = menu_options[0]
        st.sidebar.markdown(f":material/directions_car: **{selected_page}**")
    
    st.sidebar.divider()
    if st.sidebar.button(":material/logout: Sair", use_container_width=True):
        st.session_state.token = None
        st.session_state.user_role = None
        st.session_state.user_email = None
        st.rerun()

    if selected_page == "Meus Veículos":
        page_my_vehicles()
    elif selected_page == "Reservar":
        page_consult_reservations()
    elif selected_page == "Minhas Reservas":
        page_my_reservations()
    elif selected_page == "Locais & Vagas":
        page_admin_locations()
    elif selected_page == "Tarifas":
        page_admin_rates()
    elif selected_page == "Todas as Reservas":
        page_admin_reservations()
