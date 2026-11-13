import os
import pandas
import pandas as pd 
from nicegui import ui
import urllib.request 
import json

# 1. SUBSTITUI O AZUL PADRÃO PELO VERDE-ESCURO INSTITUCIONAL
ui.colors(primary='#047857', secondary='#064e3b', accent='#10b981')

# Configuração global de fundo (tom claro esverdeado suave)
ui.query('body').style('background-color: #f0fdf4;')

# --- CABEÇALHO UTILITÁRIO ---
with ui.row().classes('w-full items-center justify-between bg-emerald-900 px-8 py-2 shadow-sm'):
    ui.label('HOSPITAL SOFIA FELDMAN - ENSINO E PESQUISA').classes('text-xs font-bold text-emerald-100 uppercase tracking-widest')
    
    # Links institucionais à direita
    with ui.row().classes('items-center gap-6'):
        ui.link('Portal Institucional', 'https://www.sofiafeldman.org.br').classes('text-xs text-emerald-100 hover:text-white no-underline transition-colors')

# --- ÁREA PRINCIPAL ---
with ui.column().classes('w-full items-center justify-center pt-10 pb-4 px-4 gap-4'):
    
    # Imagem grande em destaque
    ui.image('https://raw.githubusercontent.com/sabslobeu-arch/repositorio-sofia/main/logo-sofia.png').classes('w-72 max-w-md h-auto object-contain rounded-xl shadow-md')
    
    # Título de boas-vindas
    ui.label('Repositório Científico Sofia Feldman').classes('text-2xl font-bold text-emerald-950 text-center')

# --- CONTEÚDO PRINCIPAL COM ABAS ---
with ui.column().classes('w-full max-w-5xl mx-auto p-4 gap-6'):
    
    # DECLARAÇÃO DAS 6 ABAS
    with ui.tabs().classes('w-full bg-white rounded-xl shadow-sm p-1 text-emerald-800') as tabs:
        tab_busca = ui.tab('Busca', icon='search').classes('rounded-lg transition')
        tab_programas = ui.tab('Programas da Pós', icon='school').classes('rounded-lg transition')
        tab_equipe = ui.tab('Equipe de Ensino', icon='groups').classes('rounded-lg transition')
        tab_pesquisadores = ui.tab('Pesquisadores', icon='recent_actors').classes('rounded-lg transition')
        tab_contato = ui.tab('Contato', icon='mail').classes('rounded-lg transition')

    with ui.tab_panels(tabs, value=tab_busca).classes('w-full bg-transparent p-0'):
        
      
        # ========================================================
        # ABA 1: ACERVO E BUSCA (LIGADO AO GOOGLE PLANILHAS)
        # ========================================================
        # ========================================================
        # ABA 1: ACERVO E BUSCA (LIGADO AO GOOGLE PLANILHAS)
        # ========================================================
        with ui.tab_panel(tab_busca).classes('p-0 pt-2'):
            with ui.column().classes('w-full gap-6'):
                
                # BARRA DE PESQUISA UNIFICADA
                with ui.card().classes('w-full p-2 bg-white rounded-2xl shadow-md border border-emerald-100'):
                    
                    with ui.row().classes('w-full items-center no-wrap'):
                        busca_input = ui.input(placeholder='Digite termos clínicos, DOI ou palavras-chave...').classes('flex-grow px-2').props('borderless')
                        
                        def toggle_filtros():
                            area_filtros.visible = not area_filtros.visible
                            btn_avancada.props(f'icon={"expand_less" if area_filtros.visible else "tune"}')

                        btn_avancada = ui.button('Avançada', icon='tune', on_click=toggle_filtros).classes('bg-emerald-50 text-emerald-900 hover:bg-emerald-100 rounded-xl px-4 shadow-none border border-emerald-200 mr-2')
                        ui.button(icon='search', on_click=lambda: executar_busca(False)).classes('bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl px-6 shadow-sm')

                    # Gaveta de Filtros 
                    with ui.column().classes('w-full mt-2 p-5 bg-emerald-50/50 rounded-xl border border-emerald-100 gap-4') as area_filtros:
                        area_filtros.visible = False 
                        
                        ui.label('Filtros Específicos').classes('text-sm font-bold text-emerald-900 uppercase tracking-wider')
                        
                        with ui.row().classes('w-full gap-4'):
                            filtro_titulo = ui.input(label='Título', placeholder='Palavras no título...').classes('flex-grow').props('outlined dense')
                            palavras_chave = ui.input(label='Palavras-chave', placeholder='Ex: neonatologia...').classes('flex-grow').props('outlined dense')
                            filtro_metodologia = ui.input(label='Metodologia', placeholder='Ex: revisão, estudo de caso...').classes('flex-grow').props('outlined dense')
                            
                        # LINHA DOS PROGRAMAS (COM LÓGICA DE CASCATA)
                        with ui.row().classes('w-full gap-4 mt-2 items-center'):
                            filtro_pesquisador = ui.input(label='Pesquisador', placeholder='Nome do autor...').classes('flex-grow').props('outlined dense')
                            
                            programa_principal = ui.select(
                                label='Programa da Pós', 
                                options=[
                                    'Todos', 
                                    'Residência Médica em Ginecologia e Obstetrícia', 
                                    'Residência Médica em Neonatologia', 
                                    'Residência em Enfermagem e Obstetrícia', 
                                    'Residência Multiprofissional em Neonatologia'
                                ], 
                                value='Todos'
                            ).classes('flex-grow').props('outlined dense')
                            
                            # Caixinha de Ênfase (Invisível por padrão)
                            enfase_multi = ui.select(
                                label='Selecione a Ênfase', 
                                options=[
                                    'Todas as Ênfases',
                                    'Psicologia',
                                    'Terapia Ocupacional',
                                    'Serviço Social',
                                    'Fonoaudiologia',
                                    'Nutrição',
                                    'Enfermagem',
                                    'Farmácia'
                                ], 
                                value='Todas as Ênfases'
                            ).classes('w-1/4').props('outlined dense')
                            enfase_multi.visible = False
                            
                            # Lógica para mostrar/esconder a Ênfase
                            def atualizar_enfase(e):
                                if e.value == 'Residência Multiprofissional em Neonatologia':
                                    enfase_multi.visible = True
                                else:
                                    enfase_multi.visible = False
                                    enfase_multi.set_value('Todas as Ênfases')
                                    
                            programa_principal.on_value_change(atualizar_enfase)
                            
                            filtro_ano = ui.input(label='Ano', placeholder='Ex: 2026').classes('w-32').props('outlined dense')
                        
                        with ui.row().classes('w-full justify-end gap-3 mt-2'):
                            def limpar_filtros():
                                filtro_titulo.set_value('')
                                palavras_chave.set_value('')
                                filtro_metodologia.set_value('')
                                filtro_pesquisador.set_value('')
                                programa_principal.set_value('Todos')
                                enfase_multi.set_value('Todas as Ênfases')
                                filtro_ano.set_value('')

                            ui.button('Limpar Filtros', on_click=limpar_filtros).classes('bg-white text-slate-600 hover:bg-slate-100 rounded-lg px-4 border border-slate-200 shadow-none')
                            ui.button('Aplicar Busca Avançada', icon='search', on_click=lambda: executar_busca(True)).classes('bg-emerald-700 hover:bg-emerald-800 text-white font-medium rounded-lg px-6 shadow-sm')

            # --- ÁREA DE RESULTADOS ---
            area_resultados = ui.column().classes('w-full mt-4')
            area_resultados.visible = False 
            
            with area_resultados:
                ui.label('Resultados da Busca').classes('text-xl font-bold text-emerald-900 mb-2 px-2')
                container_resultados = ui.column().classes('w-full gap-4')

            # --- FUNÇÃO DE BUSCA ---
            def executar_busca(is_avancada):
                area_resultados.visible = False
                container_resultados.clear() 
                
                termo_principal = busca_input.value.lower().strip() if busca_input.value else ""
                
                if not is_avancada and not termo_principal:
                    ui.notify('Digite algo para pesquisar.', color='warning')
                    return
                    
                ui.notify('Consultando o acervo...', color='info')
                
                try:
                    # COLE AQUI O SEU LINK DO GOOGLE (Mantenha as aspas)
                    link_google_csv = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQQG779ehUZitbl1NCLdWpt-nR0QKC9qs80cH13ZYFzIPBevuGt8GDXnb4MafKsGvNKFVwle_AeslQK/pub?output=csv '
                    
                    df = pd.read_csv(link_google_csv)
                    df = df.fillna('') 
                    
                    colunas = df.columns.tolist()
                    if len(colunas) > 0 and '<!doctype html>' in str(colunas[0]).lower():
                        ui.notify('⚠️ ALERTA: O link lido não é um CSV ou a planilha está bloqueada/privada.', color='negative', timeout=8000)
                        return
                    
                    planilha_real = []
                    for linha in df.to_dict('records'):
                        linha_limpa = {str(chave).strip().upper(): valor for chave, valor in linha.items()}
                        planilha_real.append(linha_limpa)
                    
                    resultados_encontrados = []
                    
                    for doc in planilha_real:
                        d_titulo = str(doc.get('TITULO', '')).lower()
                        d_autores = str(doc.get('AUTORES', '')).lower()
                        d_chaves = str(doc.get('PALAVRAS-CHAVES', '')).lower()
                        d_doi = str(doc.get('DOI', '')).lower()
                        d_ano = str(doc.get('ANO', '')).lower()
                        d_programa = str(doc.get('PROGRAMA DA POS', '')).lower()
                        d_metodologia = str(doc.get('TIPO DE PESQUISA', '')).lower()
                        
                        texto_completo = f"{d_titulo} {d_autores} {d_chaves} {d_doi} {d_metodologia}"
                        passou_no_filtro = True
                        
                        if termo_principal and termo_principal not in texto_completo:
                            passou_no_filtro = False
                            
                        if is_avancada and passou_no_filtro:
                            if filtro_titulo.value and str(filtro_titulo.value).lower().strip() not in d_titulo:
                                passou_no_filtro = False
                            if palavras_chave.value and str(palavras_chave.value).lower().strip() not in d_chaves:
                                passou_no_filtro = False
                            if filtro_metodologia.value and str(filtro_metodologia.value).lower().strip() not in d_metodologia:
                                passou_no_filtro = False
                            if filtro_pesquisador.value and str(filtro_pesquisador.value).lower().strip() not in d_autores:
                                passou_no_filtro = False
                            if filtro_ano.value and str(filtro_ano.value).lower().strip() not in d_ano:
                                passou_no_filtro = False
                                
                            # --- LÓGICA DE RECONSTRUÇÃO DO NOME DO PROGRAMA ---
                            prog_selecionado = programa_principal.value
                            enf_selecionada = enfase_multi.value
                            
                            if prog_selecionado != 'Todos':
                                texto_busca_programa = prog_selecionado.lower()
                                
                                # Se a pessoa escolheu a multiprofissional E uma ênfase específica, recriamos o texto igual à planilha
                                if prog_selecionado == 'Residência Multiprofissional em Neonatologia' and enf_selecionada != 'Todas as Ênfases':
                                    texto_busca_programa = f"residência multiprofissional em neonatologia (ênfase em {enf_selecionada.lower()})"
                                
                                if texto_busca_programa not in d_programa:
                                    passou_no_filtro = False
                                
                        if passou_no_filtro:
                            resultados_encontrados.append(doc)
                    
                    area_resultados.visible = True
                    
                    with container_resultados:
                        if len(resultados_encontrados) > 0:
                            ui.label(f'{len(resultados_encontrados)} documento(s) encontrado(s)').classes('text-sm text-slate-500 mb-2')
                            
                            for doc in resultados_encontrados:
                                with ui.card().classes('w-full p-0 bg-white rounded-xl shadow-sm border border-emerald-100 hover:shadow-md transition-all duration-300 overflow-hidden'):
                                    
                                    with ui.row().classes('w-full p-5 cursor-pointer hover:bg-emerald-50/30 transition-colors justify-between items-center no-wrap gap-4') as cabecalho:
                                        
                                        with ui.column().classes('flex-grow gap-1'):
                                            with ui.row().classes('gap-2 items-center'):
                                                ui.label(str(doc.get('TIPO DE DOCUMENTO', ''))).classes('bg-emerald-100 text-emerald-800 text-xs font-bold px-2 py-1 rounded uppercase tracking-wide')
                                                ui.label(str(doc.get('ANO', ''))).classes('text-sm text-slate-500 font-medium')
                                            
                                            ui.label(str(doc.get('TITULO', 'Sem Título'))).classes('text-lg font-bold text-emerald-900 leading-tight mt-1')
                                            ui.label(str(doc.get('AUTORES', ''))).classes('text-sm text-slate-600')
                                        
                                        with ui.row().classes('shrink-0 items-center gap-4'):
                                            btn_pdf = ui.button('Baixar PDF', icon='picture_as_pdf').classes('bg-emerald-50 text-emerald-700 hover:bg-emerald-700 hover:text-white border border-emerald-200 shadow-none rounded-lg px-4 py-2 transition-colors')
                                            btn_pdf.on('click.stop', lambda: ui.notify('Link do PDF será conectado aqui!'))
                                            icone_seta = ui.icon('keyboard_arrow_down', size='2rem', color='slate-400').classes('transition-transform duration-300')

                                    with ui.column().classes('w-full px-6 pb-6 pt-2 bg-slate-50/50 border-t border-slate-100 gap-4') as detalhes:
                                        detalhes.visible = False 
                                        
                                        with ui.row().classes('w-full items-start gap-8'):
                                            orientador = str(doc.get('ORIENTADOR', '')).strip()
                                            if orientador:
                                                with ui.row().classes('items-start gap-2'):
                                                    ui.icon('person', size='1.2rem', color='emerald-700')
                                                    with ui.column().classes('gap-0'):
                                                        ui.label('Orientador').classes('text-[10px] font-bold text-slate-500 uppercase tracking-wider')
                                                        ui.label(orientador).classes('text-sm text-slate-800')
                                                        
                                            chaves = str(doc.get('PALAVRAS-CHAVES', '')).strip()
                                            if chaves:
                                                with ui.row().classes('items-start gap-2'):
                                                    ui.icon('vpn_key', size='1.2rem', color='emerald-700')
                                                    with ui.column().classes('gap-0'):
                                                        ui.label('Palavras-chave').classes('text-[10px] font-bold text-slate-500 uppercase tracking-wider')
                                                        ui.label(chaves).classes('text-sm text-slate-800')

                                            metodologia = str(doc.get('TIPO DE PESQUISA', '')).strip()
                                            if metodologia:
                                                with ui.row().classes('items-start gap-2'):
                                                    ui.icon('search', size='1.2rem', color='emerald-700')
                                                    with ui.column().classes('gap-0'):
                                                        ui.label('Metodologia').classes('text-[10px] font-bold text-slate-500 uppercase tracking-wider')
                                                        ui.label(metodologia).classes('text-sm text-slate-800')
                                                        
                                            programa = str(doc.get('PROGRAMA DA POS', '')).strip()
                                            if programa and programa.lower() != 'nenhum':
                                                with ui.row().classes('items-start gap-2'):
                                                    ui.icon('school', size='1.2rem', color='emerald-700')
                                                    with ui.column().classes('gap-0'):
                                                        ui.label('Programa').classes('text-[10px] font-bold text-slate-500 uppercase tracking-wider')
                                                        ui.label(programa).classes('text-sm text-slate-800')

                                    def criar_acao_toggle(det, icone):
                                        def acao():
                                            det.visible = not det.visible
                                            if det.visible:
                                                icone.classes(add='rotate-180')
                                            else:
                                                icone.classes(remove='rotate-180')
                                        return acao
                                        
                                    cabecalho.on('click', criar_acao_toggle(detalhes, icone_seta))
                        else:
                            with ui.column().classes('w-full items-center justify-center p-12 bg-slate-50 border border-red-100 rounded-2xl border-dashed'):
                                ui.icon('search_off', size='3rem', color='red-300').classes('mb-2')
                                ui.label('Nenhum documento encontrado.').classes('text-red-500 text-center font-bold')
                
                except Exception as e:
                    ui.notify(f'Erro técnico: {str(e)}', color='negative')
                    
       

        # ========================================================
        # ABA 3: PROGRAMAS DA PÓS
        # ========================================================
        with ui.tab_panel(tab_programas).classes('p-0 pt-2'):
            ui.label('Nossos Programas de Residência').classes('text-2xl font-bold text-emerald-900 mb-6 px-2')
            
            with ui.row().classes('w-full gap-6'):
                
                # 1. Ginecologia e Obstetrícia
                with ui.card().classes('w-80 p-6 bg-white rounded-2xl shadow-sm border border-emerald-100 hover:shadow-md transition-shadow'):
                    ui.icon('pregnant_woman', color='emerald', size='2rem').classes('mb-2 bg-emerald-50 p-2 rounded-lg')
                    ui.label('Residência Médica em Ginecologia e Obstetrícia').classes('text-lg font-bold text-emerald-900 leading-tight h-14')
                    ui.label('Especialização com foco no cuidado integral à saúde da mulher, gestação, parto e puerpério.').classes('text-sm text-slate-600 mt-2 mb-4 h-16')
                    ui.button('Ver no Site Institucional', icon='open_in_new').props('href="https://sofiafeldman.org.br/residencia-medica-ginecologia-obstetricia/" target="_blank"').classes('w-full bg-emerald-50 text-emerald-900 hover:bg-emerald-100 shadow-none border border-emerald-200 rounded-xl')

                # 2. Neonatologia
                with ui.card().classes('w-80 p-6 bg-white rounded-2xl shadow-sm border border-emerald-100 hover:shadow-md transition-shadow'):
                    ui.icon('child_care', color='emerald', size='2rem').classes('mb-2 bg-emerald-50 p-2 rounded-lg')
                    ui.label('Residência Médica em Neonatologia').classes('text-lg font-bold text-emerald-900 leading-tight h-14')
                    ui.label('Formação avançada no cuidado intensivo e assistência especializada ao recém-nascido.').classes('text-sm text-slate-600 mt-2 mb-4 h-16')
                    ui.button('Ver no Site Institucional', icon='open_in_new').props('href="https://sofiafeldman.org.br/residencia-medica-neonatologia-2/" target="_blank"').classes('w-full bg-emerald-50 text-emerald-900 hover:bg-emerald-100 shadow-none border border-emerald-200 rounded-xl')

                # 3. Enfermagem e Obstetrícia
                with ui.card().classes('w-80 p-6 bg-white rounded-2xl shadow-sm border border-emerald-100 hover:shadow-md transition-shadow'):
                    ui.icon('medical_services', color='emerald', size='2rem').classes('mb-2 bg-emerald-50 p-2 rounded-lg')
                    ui.label('Residência em Enfermagem e Obstetrícia').classes('text-lg font-bold text-emerald-900 leading-tight h-14')
                    ui.label('Qualificação em enfermagem obstétrica para assistência segura e humanizada.').classes('text-sm text-slate-600 mt-2 mb-4 h-16')
                    ui.button('Ver no Site Institucional', icon='open_in_new').props('href="https://sofiafeldman.org.br/residencia-enfermagem-obstetrica-2/" target="_blank"').classes('w-full bg-emerald-50 text-emerald-900 hover:bg-emerald-100 shadow-none border border-emerald-200 rounded-xl')

                # 4. Multiprofissional em Neonatologia
                with ui.card().classes('w-80 p-6 bg-white rounded-2xl shadow-sm border border-emerald-100 hover:shadow-md transition-shadow'):
                    ui.icon('diversity_1', color='emerald', size='2rem').classes('mb-2 bg-emerald-50 p-2 rounded-lg')
                    ui.label('Residência Multiprofissional em Neonatologia').classes('text-lg font-bold text-emerald-900 leading-tight h-14')
                    ui.label('Atuação integrada de diversas categorias profissionais no cuidado intensivo neonatal.').classes('text-sm text-slate-600 mt-2 mb-4 h-16')
                    ui.button('Ver no Site Institucional', icon='open_in_new').props('href="https://sofiafeldman.org.br/residencia-multi-neonatologia/" target="_blank"').classes('w-full bg-emerald-50 text-emerald-900 hover:bg-emerald-100 shadow-none border border-emerald-200 rounded-xl')

        # ========================================================
        # ABA 4: EQUIPE DE ENSINO
        # ========================================================
        # ========================================================
        # ABA: PESQUISADORES / EQUIPE DE ENSINO
        # ========================================================
        with ui.tab_panel(tab_equipe).classes('p-0 pt-2 bg-slate-50/30'):
            ui.label('Pesquisadores e Corpo Docente').classes('text-2xl font-bold text-emerald-900 mb-6 px-2')

            # O 'flex-wrap' garante que os cards fiquem lado a lado e desçam de linha se faltar espaço
            with ui.row().classes('w-full gap-6 flex-wrap justify-start px-2'):
                
                # --- CARD PESQUISADOR 1 ---
                with ui.card().classes('w-[350px] bg-white border border-slate-200 rounded-2xl shadow-sm hover:shadow-md transition-shadow p-6 flex flex-col gap-4'):
                    
                    # Cabeçalho: Foto/Ícone e Nome
                    with ui.row().classes('items-center gap-4 no-wrap'):
                        ui.avatar('science', size='3.5rem', color='emerald-100', text_color='emerald-700').classes('shrink-0')
                        with ui.column().classes('gap-0'):
                            ui.label('Nome do Pesquisador').classes('text-lg font-bold text-slate-800 leading-tight')
                            ui.label('Doutorado em Saúde Pública').classes('text-xs text-emerald-700 font-bold uppercase tracking-wider mt-1')
                    
                    # Mini-Currículo (Estilo Lattes)
                    ui.label(
                        'Enfermeiro(a) com atuação em humanização do parto. '
                        'Líder do Grupo de Pesquisa em Saúde Materno-Infantil. '
                        'Possui experiência na área de Neonatologia e Cuidados Paliativos...'
                    ).classes('text-sm text-slate-600 leading-relaxed')
                    
                    ui.separator().classes('bg-slate-100')
                    
                    # Última Publicação (Previsão para o futuro)
                    with ui.column().classes('gap-1 w-full bg-slate-50 p-3 rounded-lg border border-slate-100'):
                        ui.label('Última Pesquisa Publicada').classes('text-[10px] uppercase font-bold text-slate-400 tracking-wide')
                        with ui.row().classes('items-start gap-2 no-wrap'):
                            ui.icon('article', size='1rem', color='emerald-600').classes('mt-1 shrink-0')
                            ui.label('Práticas Integrativas no Trabalho de Parto (2025)').classes('text-xs text-slate-700 font-medium italic')
                        
                    # Botão de Ação
                    ui.button('Ver Currículo Lattes', icon='open_in_new').classes('w-full mt-auto bg-emerald-50 text-emerald-800 hover:bg-emerald-700 hover:text-white shadow-none border border-emerald-200 rounded-lg transition-colors')

                # --- CARD PESQUISADOR 2 ---
                with ui.card().classes('w-[350px] bg-white border border-slate-200 rounded-2xl shadow-sm hover:shadow-md transition-shadow p-6 flex flex-col gap-4'):
                    
                    with ui.row().classes('items-center gap-4 no-wrap'):
                        ui.avatar('biotech', size='3.5rem', color='emerald-100', text_color='emerald-700').classes('shrink-0')
                        with ui.column().classes('gap-0'):
                            ui.label('Nome do Pesquisador 2').classes('text-lg font-bold text-slate-800 leading-tight')
                            ui.label('Mestre em Enfermagem').classes('text-xs text-emerald-700 font-bold uppercase tracking-wider mt-1')
                    
                    ui.label(
                        'Especialista em Aleitamento Materno. Atua na linha de pesquisa de '
                        'desenvolvimento neuropsicomotor de prematuros extremos...'
                    ).classes('text-sm text-slate-600 leading-relaxed')
                    
                    ui.separator().classes('bg-slate-100')
                    
                    with ui.column().classes('gap-1 w-full bg-slate-50 p-3 rounded-lg border border-slate-100'):
                        ui.label('Última Pesquisa Publicada').classes('text-[10px] uppercase font-bold text-slate-400 tracking-wide')
                        with ui.row().classes('items-start gap-2 no-wrap'):
                            ui.icon('article', size='1rem', color='emerald-600').classes('mt-1 shrink-0')
                            ui.label('Impacto do Método Canguru no ganho de peso (2026)').classes('text-xs text-slate-700 font-medium italic')
                        
                    ui.button('Ver Currículo Lattes', icon='open_in_new').classes('w-full mt-auto bg-emerald-50 text-emerald-800 hover:bg-emerald-700 hover:text-white shadow-none border border-emerald-200 rounded-lg transition-colors')

                # Para adicionar mais pesquisadores, basta copiar o bloco "with ui.card()..." inteiro e colar logo abaixo!
       
        # ========================================================
        # ABA 5: LISTA DE PESQUISADORES
        # ========================================================
        with ui.tab_panel(tab_pesquisadores).classes('p-0 pt-2'):
            
            # 1. PREENCHA OS DADOS AQUI (Adicione quantas linhas precisar)
            dados_pesquisadores = [
                {'nome': 'Andrezza Lopes', 'formacao': 'Médica GO', 'titulacao': 'Doutora'},
                {'nome': 'Aryanne Gabriele Policarpo', 'formacao': 'Enfermeira Obstétrica', 'titulacao': 'Mestre'},
                {'nome': 'Camilla Lorraine Moura Dias', 'formacao': 'Enfermeira Neonatal', 'titulacao': 'Mestre'},
                {'nome': 'Cintia Ribeiro Santos ', 'formacao': 'Enfermeira Obstétrica', 'titulacao': 'Mestre'},
                {'nome': 'Cristiane Alessandra da Silva  ', 'formacao': 'Enfermeira Obstétrica', 'titulacao': 'Mestre'},
                {'nome': 'Danubia Mariane Barbosa Jardim de Carvalho ', 'formacao': 'Enfermeira Obstétrica', 'titulacao': 'Doutora'},
                {'nome': 'Debora Lucas Viana Goncalves ', 'formacao': 'Enfermeira Obstétrica', 'titulacao': 'Mestre'},
                {'nome': 'Elisa Lima e Silva', 'formacao': 'Enfermeira Intensivista', 'titulacao': 'Mestre'},
                {'nome': 'Flavia A F L. Silva ', 'formacao': 'Fonoaudiologa', 'titulacao': 'Doutora'},
                {'nome': 'Lorena Azevedo Correia', 'formacao': 'Terapeuta ocupacional', 'titulacao': 'Mestre'},
                {'nome': 'Lorena Oliveira Nogueira', 'formacao': 'Nutricionista', 'titulacao': 'Mestre'},
                {'nome': 'Marília A. R. Oliveira Santos', 'formacao': 'Assistente Social ', 'titulacao': 'Mestre'},
                {'nome': 'Patrícia Rodrigues Da Costa', 'formacao': 'Terapeuta Ocupacional', 'titulacao': 'Mestre'},
                {'nome': 'Regina Célia Coelho de Moraes', 'formacao': 'Nutricionista', 'titulacao': 'Mestre'},
                {'nome': 'Solange Clessêncio Ferreira Diniz', 'formacao': 'Enfermeira Obstétrica', 'titulacao': 'Doutora'},
                {'nome': 'Tatiana Coelho Lopes', 'formacao': 'Fisioterapeuta', 'titulacao': 'Pós-Doutora'},
                {'nome': 'Barbara Barroso Siqueira', 'formacao': 'Enfermeira Obstétrica', 'titulacao': 'Mestre'},
                {'nome': 'Caroline Reis ', 'formacao': 'Médica', 'titulacao': 'Mestre'},
                {'nome': 'Tânia Antunes Carvalho  ', 'formacao': 'Médica', 'titulacao': 'Mestre'},
                {'nome': 'Diego Alcântara Alves  ', 'formacao': 'Enfermeiro Obstétrico', 'titulacao': 'Mestre'},
            ]

           # Título simples, sem a barra de busca
            ui.label('Diretório de Pesquisadores do Sofia').classes('text-2xl font-bold text-emerald-900 mb-6 px-2')
            
            # 2. O SISTEMA GERA O VISUAL SOZINHO BASEADO NA LISTA ACIMA
            with ui.column().classes('w-full gap-3'):
                for pesq in dados_pesquisadores:
                    with ui.card().classes('w-full p-4 bg-white rounded-xl shadow-sm border border-emerald-100 hover:border-emerald-300 transition-colors'):
                        with ui.row().classes('w-full items-center no-wrap gap-4'):
                            
                            # Ícone do chapéu de formatura
                            ui.avatar('school', color='emerald-50', text_color='emerald-700')
                            
                            # Textos
                            with ui.column().classes('gap-0'):
                                ui.label(pesq['nome']).classes('text-base font-bold text-emerald-900')
                                ui.label(pesq['titulacao']).classes('text-xs font-bold text-emerald-700 uppercase tracking-wide')
                                ui.label(f"Formação: {pesq['formacao']}").classes('text-sm text-slate-600 mt-1')

        # ========================================================
        # ABA 6: ENTRE EM CONTATO
        # ========================================================
        with ui.tab_panel(tab_contato).classes('p-0 pt-2'):
            with ui.card().classes('w-full max-w-4xl mx-auto p-4 bg-white rounded-2xl shadow-sm border border-emerald-100 items-center text-center'):
                
                ui.label('Fale Conosco').classes('text-2xl font-bold text-emerald-900 mt-2')
                ui.label('Preencha o formulário abaixo e nossa equipe responderá em breve.').classes('text-sm text-slate-600 mb-4')
                
                # Forma nativa e à prova de falhas de colocar o iframe no NiceGUI
                ui.element('iframe').props(
                    'src="https://docs.google.com/forms/d/e/1FAIpQLScxCJl1CFOL3tOlFTLuvrXm1U0uAqubJsGBbNkgx15uML9Dqw/viewform?embedded=true" '
                    'width="100%" '
                    'height="800" '
                    'frameborder="0"'
                ).classes('w-full bg-transparent')

# Inicialização do Servidor para o Render
port = int(os.environ.get('PORT', 8080))
ui.run(port=port, host='0.0.0.0', title='Repositório Sofia', reload=False)
