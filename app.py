import os
from nicegui import ui

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
        tab_submissao = ui.tab('Nova Submissão', icon='upload_file').classes('rounded-lg transition')
        tab_programas = ui.tab('Programas da Pós', icon='school').classes('rounded-lg transition')
        tab_equipe = ui.tab('Equipe de Ensino', icon='groups').classes('rounded-lg transition')
        tab_pesquisadores = ui.tab('Pesquisadores', icon='recent_actors').classes('rounded-lg transition')
        tab_contato = ui.tab('Contato', icon='mail').classes('rounded-lg transition')

    with ui.tab_panels(tabs, value=tab_busca).classes('w-full bg-transparent p-0'):
        
        # ========================================================
        # ABA 1: ACERVO E BUSCA
        # ========================================================
        with ui.tab_panel(tab_busca).classes('p-0 pt-2'):
            with ui.column().classes('w-full gap-6'):
                
                # BARRA DE PESQUISA UNIFICADA
                with ui.card().classes('w-full p-2 bg-white rounded-2xl shadow-md border border-emerald-100'):
                    
                    with ui.row().classes('w-full items-center no-wrap'):
                        # Input principal
                        busca_input = ui.input(placeholder='Digite termos clínicos, DOI ou palavras-chave...').classes('flex-grow px-2').props('borderless')
                        
                        # Lógica para mostrar/esconder filtros
                        def toggle_filtros():
                            area_filtros.visible = not area_filtros.visible
                            btn_avancada.props(f'icon={"expand_less" if area_filtros.visible else "tune"}')

                        btn_avancada = ui.button('Avançada', icon='tune', on_click=toggle_filtros).classes('bg-emerald-50 text-emerald-900 hover:bg-emerald-100 rounded-xl px-4 shadow-none border border-emerald-200 mr-2')
                        
                        ui.button(icon='search', on_click=lambda: ui.notify(f'Buscando por: {busca_input.value}')).classes('bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl px-6 shadow-sm')

                    # Gaveta de Filtros e Busca Combinada (Oculta até clicar em Avançada)
                    with ui.column().classes('w-full mt-2 p-5 bg-emerald-50/50 rounded-xl border border-emerald-100 gap-4') as area_filtros:
                        area_filtros.visible = False 
                        
                        # --- 1. BUSCA COMBINADA (BOOLEANA) ---
                        ui.label('Busca Combinada (Operadores Booleanos)').classes('text-sm font-bold text-emerald-900 uppercase tracking-wider')
                        
                        with ui.row().classes('w-full gap-3 items-center'):
                            operador = ui.select(options=['AND (E)', 'OR (Ou)', 'NOT (Não)'], value='AND (E)', label='Operador').classes('w-32').props('outlined dense')
                            termo_combinado = ui.input(label='Termo adicional', placeholder='Digite o termo para combinar...').classes('flex-grow').props('outlined dense')
                            campo_combinado = ui.select(options=['Todos os campos', 'Título', 'Resumo', 'Pesquisador'], value='Todos os campos', label='Pesquisar em').classes('w-48').props('outlined dense')

                        ui.separator().classes('my-1 border-emerald-200/50')
                        
                        # --- 2. FILTROS ESPECÍFICOS ---
                        ui.label('Filtros Específicos').classes('text-sm font-bold text-emerald-900 uppercase tracking-wider')
                        
                        # Linha 1 de filtros
                        with ui.row().classes('w-full gap-4'):
                            filtro_titulo = ui.input(label='Título', placeholder='Palavras no título...').classes('flex-grow').props('outlined dense')
                            filtro_resumo = ui.input(label='Resumo', placeholder='Palavras no resumo...').classes('flex-grow').props('outlined dense')
                            palavras_chave = ui.input(label='Palavras-chave', placeholder='Ex: neonatologia...').classes('w-1/4').props('outlined dense')
                            
                        # Linha 2 de filtros
                        with ui.row().classes('w-full gap-4 mt-2'):
                            filtro_pesquisador = ui.input(label='Pesquisador', placeholder='Nome do autor...').classes('flex-grow').props('outlined dense')
                            programas_pos = ui.select(
                                label='Programa da Pós', 
                                options=['Todos', 'Residência Médica', 'Residência Multiprofissional', 'Mestrado Profissional', 'Especialização'], 
                                value='Todos'
                            ).classes('w-1/3').props('outlined dense')
                            filtro_ano = ui.input(label='Ano', placeholder='Ex: 2026').classes('w-32').props('outlined dense')
                        
                        with ui.row().classes('w-full justify-end gap-3 mt-2'):
                            def limpar_filtros():
                                operador.set_value('AND (E)')
                                termo_combinado.set_value('')
                                campo_combinado.set_value('Todos os campos')
                                filtro_titulo.set_value('')
                                filtro_resumo.set_value('')
                                palavras_chave.set_value('')
                                filtro_pesquisador.set_value('')
                                programas_pos.set_value('Todos')
                                filtro_ano.set_value('')

                            ui.button('Limpar Filtros', on_click=limpar_filtros).classes('bg-white text-slate-600 hover:bg-slate-100 rounded-lg px-4 border border-slate-200 shadow-none')
                            ui.button('Aplicar Busca Avançada', icon='search').classes('bg-emerald-700 hover:bg-emerald-800 text-white font-medium rounded-lg px-6 shadow-sm')

                # ÁREA DE RESULTADOS
                with ui.column().classes('w-full gap-4 mt-2'):
                    ui.label('Acervo Recente').classes('text-lg font-bold text-emerald-900 ml-2')
                    
                    with ui.card().classes('w-full p-6 bg-white rounded-2xl shadow-sm border border-emerald-100 border-l-4 border-l-emerald-600 gap-2 hover:bg-slate-50 transition-colors cursor-pointer'):
                        ui.label('Avaliação de estratégias de busca em bases de dados biomédicas').classes('text-lg font-bold text-slate-900')
                        ui.label('Autores: Silva, M. et al. • Ano: 2026 • DOI: 10.1016/j.jbi.2026.100').classes('text-xs text-slate-400 font-medium')
                        ui.label('Resumo descritivo focado na clareza visual e na legibilidade dos metadados extraídos automaticamente do artigo científico.').classes('text-sm text-slate-600 leading-relaxed mb-2')
                        
                        with ui.row().classes('gap-2'):
                            ui.badge('MeSH: Information Retrieval', color='green').classes('text-xs')
                            ui.badge('Evidence-Based Practice', color='green').classes('text-xs')

        # ========================================================
        # ABA 2: NOVA SUBMISSÃO
        # ========================================================
        with ui.tab_panel(tab_submissao).classes('p-0 pt-2'):
            with ui.card().classes('w-full max-w-3xl mx-auto p-8 bg-white rounded-2xl shadow-sm border border-emerald-100 gap-4'):
                ui.label('Cadastrar Novo Documento').classes('text-xl font-bold text-emerald-900')
                ui.label('Insira o DOI para recuperação automática ou preencha manualmente os campos.').classes('text-xs text-slate-500 mb-2')
                
                with ui.row().classes('w-full items-end gap-3'):
                    ui.input(label='DOI do Artigo', placeholder='10.xxxx/...').classes('flex-grow').props('outlined dense')
                    ui.button('Buscar DOI', icon='cloud_download').classes('bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl shadow-sm')

                ui.input(label='Título').classes('w-full').props('outlined dense')
                ui.input(label='Autores').classes('w-full').props('outlined dense')
                ui.textarea(label='Resumo').classes('w-full').props('outlined dense')
                
                ui.upload(label='Arraste o arquivo PDF aqui ou clique para selecionar').classes('w-full border-2 border-dashed border-emerald-200 rounded-2xl p-4 bg-emerald-50/30')
                
                ui.button('Salvar no Repositório', icon='save').classes('w-full bg-emerald-700 hover:bg-emerald-800 text-white font-medium rounded-xl py-3 mt-4 shadow-sm')

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
        with ui.tab_panel(tab_equipe).classes('p-0 pt-2'):
            with ui.card().classes('w-full p-8 bg-white rounded-2xl shadow-sm border border-emerald-100 text-center'):
                ui.icon('groups', size='4rem', color='emerald').classes('mx-auto mb-4')
                ui.label('Equipe de Ensino').classes('text-2xl font-bold text-emerald-900')
                ui.label('Página em desenvolvimento. Em breve conheceremos o corpo docente.').classes('text-slate-500 mt-2')

        # ========================================================
        # ABA 5: LISTA DE PESQUISADORES
        # ========================================================
        with ui.tab_panel(tab_pesquisadores).classes('p-0 pt-2'):
            with ui.card().classes('w-full p-8 bg-white rounded-2xl shadow-sm border border-emerald-100 text-center'):
                ui.icon('recent_actors', size='4rem', color='emerald').classes('mx-auto mb-4')
                ui.label('Lista de Pesquisadores').classes('text-2xl font-bold text-emerald-900')
                ui.label('Página em desenvolvimento. Em breve o diretório de pesquisadores ativos.').classes('text-slate-500 mt-2')

        
        # ========================================================
        # ABA 6: ENTRE EM CONTATO
        # ========================================================
        with ui.tab_panel(tab_contato).classes('p-0 pt-2'):
            with ui.card().classes('w-full max-w-4xl mx-auto p-4 bg-white rounded-2xl shadow-sm border border-emerald-100 items-center text-center'):
                
                ui.label('Fale Conosco').classes('text-2xl font-bold text-emerald-900 mt-2')
                ui.label('Preencha o formulário abaixo e nossa equipe responderá em breve.').classes('text-sm text-slate-600 mb-4')
                
                # Iframe com o width em 100% para ser responsivo
                codigo_iframe = '''
                <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScxCJl1CFOL3tOlFTLuvrXm1U0uAqubJsGBbNkgx15uML9Dqw/viewform?embedded=true" 
                        width="100%" 
                        height="760" 
                        frameborder="0" 
                        marginheight="0" 
                        marginwidth="0">
                    Carregando formulário...
                </iframe>
                '''
                ui.html(codigo_iframe).classes('w-full')

# Inicialização do Servidor para o Render
port = int(os.environ.get('PORT', 8080))
ui.run(port=port, host='0.0.0.0', title='Repositório Sofia', reload=False)
