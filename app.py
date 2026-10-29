import os
from nicegui import ui

# Configuração global de fundo (tom claro esverdeado suave)
ui.query('body').style('background-color: #f0fdf4;')

# --- CABEÇALHO ---
with ui.row().classes('w-full items-center justify-between bg-white px-8 py-4 shadow-sm border-b border-emerald-100'):
    with ui.row().classes('items-center gap-4'):
        ui.label('Repositório Sofia').classes('text-lg font-bold text-emerald-800 tracking-tight')
    ui.badge('Online', color='green').classes('text-xs px-3 py-1')

# --- ÁREA PRINCIPAL ---
with ui.column().classes('w-full items-center justify-center pt-10 pb-4 px-4 gap-4'):
    
    # Imagem grande em destaque
    ui.image('https://raw.githubusercontent.com/sabslobeu-arch/repositorio-sofia/main/logo-sofia.png').classes('w-72 max-w-md h-auto object-contain rounded-xl shadow-md')
    
    # Título de boas-vindas
    ui.label('Repositório Científico Sofia Feldman').classes('text-2xl font-bold text-emerald-950 text-center')

# --- CONTEÚDO PRINCIPAL COM ABAS ---
with ui.column().classes('w-full max-w-5xl mx-auto p-4 gap-6'):
    
    # Declaração das abas (Em cima)
    with ui.tabs().classes('w-full bg-white rounded-xl shadow-sm p-1 text-emerald-800') as tabs:
        tab_busca = ui.tab('Acervo & Busca', icon='search').classes('rounded-lg transition')
        tab_submissao = ui.tab('Nova Submissão', icon='upload_file').classes('rounded-lg transition')

    with ui.tab_panels(tabs, value=tab_busca).classes('w-full bg-transparent p-0'):
        
        # ========================================================
        # ABA 1: ACERVO E BUSCA
        # ========================================================
        with ui.tab_panel(tab_busca).classes('p-0 pt-2'):
            with ui.column().classes('w-full gap-6'):
                
                # 1. BARRA DE PESQUISA UNIFICADA
                # O visual de 'card' faz tudo parecer uma barra única
                with ui.card().classes('w-full p-2 bg-white rounded-2xl shadow-md border border-emerald-100'):
                    
                    with ui.row().classes('w-full items-center no-wrap'):
                        # Input sem borda ocupando o espaço todo
                        busca_input = ui.input(placeholder='Digite termos clínicos, DOI ou palavras-chave...').classes('flex-grow px-2').props('borderless')
                        
                        # Lógica para mostrar/esconder filtros
                        def toggle_filtros():
                            area_filtros.visible = not area_filtros.visible
                            btn_avancada.props(f'icon={"expand_less" if area_filtros.visible else "tune"}')

                        # Botão Avançada "embutido" ao lado da busca
                        btn_avancada = ui.button('Avançada', icon='tune', on_click=toggle_filtros).classes('bg-emerald-50 text-emerald-900 hover:bg-emerald-100 rounded-xl px-4 shadow-none border border-emerald-200 mr-2')
                        
                        # Botão Principal de Buscar
                        ui.button(icon='search', on_click=lambda: ui.notify(f'Buscando por: {busca_input.value}')).classes('bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl px-6 shadow-sm')

                    # Gaveta de Filtros (Oculta até clicar em Avançada)
                    with ui.column().classes('w-full mt-2 p-5 bg-emerald-50/50 rounded-xl border border-emerald-100 gap-4') as area_filtros:
                        area_filtros.visible = False 
                        
                        ui.label('Filtros e Facetas').classes('text-sm font-bold text-emerald-900 uppercase tracking-wider')
                        
                        with ui.row().classes('w-full gap-4'):
                            descritor = ui.input(label='Descritor MeSH/DeCS', placeholder='Ex: Neoplasias').classes('flex-grow').props('outlined dense')
                            tipo_doc = ui.select(label='Tipo de Documento', options=['Todos', 'Artigo Original', 'Revisão Sistemática', 'Diretriz'], value='Todos').classes('w-1/3').props('outlined dense')
                        
                        with ui.row().classes('w-full justify-end gap-3 mt-2'):
                            ui.button('Limpar', on_click=lambda: [descritor.set_value(''), tipo_doc.set_value('Todos')]).classes('bg-white text-slate-600 hover:bg-slate-100 rounded-lg px-4 border border-slate-200 shadow-none')
                            ui.button('Aplicar Filtros', icon='filter_list').classes('bg-emerald-700 hover:bg-emerald-800 text-white font-medium rounded-lg px-6 shadow-sm')

                # 2. ÁREA DE RESULTADOS
                with ui.column().classes('w-full gap-4 mt-2'):
                    ui.label('Acervo Recente').classes('text-lg font-bold text-emerald-900 ml-2')
                    
                    # Card de Exemplo
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

# Inicialização do Servidor para o Render
port = int(os.environ.get('PORT', 8080))
ui.run(port=port, host='0.0.0.0', title='Repositório Sofia', reload=False)
