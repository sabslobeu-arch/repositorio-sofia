import os
from nicegui import ui, app

# Configuração global de fundo (tom claro esverdeado suave)
ui.query('body').style('background-color: #f0fdf4;')

# --- CABEÇALHO ---
with ui.row().classes('w-full items-center justify-between bg-white px-8 py-4 shadow-sm border-b border-emerald-100'):
    with ui.row().classes('items-center gap-4'):
        ui.label('Repositório Sofia').classes('text-lg font-bold text-emerald-800 tracking-tight')
    ui.badge('Online', color='green').classes('text-xs px-3 py-1')

# --- ÁREA PRINCIPAL (COM A IMAGEM GRANDE E BUSCA) ---
with ui.column().classes('w-full items-center justify-center py-12 px-4 gap-6'):
    
    # Imagem grande em destaque (URL corrigida para o formato Raw do GitHub)
    ui.image('https://raw.githubusercontent.com/sabslobeu-arch/repositorio-sofia/main/logo-sofia.png').classes('w-96 max-w-lg h-auto object-contain rounded-xl shadow-md')
    
    # Título de boas-vindas
    ui.label('Repositório Científico Sofia Feldman').classes('text-2xl font-bold text-emerald-950 text-center')
    
    # Caixa de Pesquisa em Destaque
    with ui.card().classes('w-full max-w-2xl p-6 bg-white shadow-lg rounded-2xl border border-emerald-100 gap-4'):
        ui.label('Pesquisar na Base de Conhecimento').classes('font-semibold text-emerald-800 text-sm')
        
        with ui.row().classes('w-full items-center gap-2'):
            search_input = ui.input(placeholder='Digite termos clínicos, DOI ou palavras-chave...').classes('flex-grow')
            ui.button('Buscar', on_click=lambda: ui.notify(f'Buscando por: {search_input.value}')).classes('bg-emerald-700 text-white hover:bg-emerald-800')

# --- ABA 1: BUSCA ---
        with ui.tab_panel(tab_busca).classes('p-0 pt-4'):
            with ui.column().classes('w-full gap-6'):
                
                # --------------------------------------------------------
                # 1. BLOCO DE PESQUISA UNIFICADO
                # --------------------------------------------------------
                with ui.card().classes('w-full p-6 bg-white rounded-2xl shadow-sm border border-emerald-100 gap-4'):
                    
                    # Linha Principal de Busca
                    with ui.row().classes('w-full items-center gap-3 no-wrap'):
                        busca_input = ui.input(placeholder='Busca por título, resumo ou operadores booleanos...').classes('flex-grow border-none text-base')
                        
                        ui.button(icon='search').classes('bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl px-6 shadow-sm')
                        
                        # Lógica para mostrar/esconder filtros
                        def toggle_filtros():
                            area_filtros.visible = not area_filtros.visible
                            btn_avancada.props(f'icon={"expand_less" if area_filtros.visible else "tune"}')

                        btn_avancada = ui.button('Busca Avançada', icon='tune', on_click=toggle_filtros).classes('bg-emerald-50 text-emerald-900 hover:bg-emerald-100 rounded-xl px-4 shadow-none border border-emerald-200')

                    # Área de Filtros e Facetas (Inicia Oculta)
                    with ui.column().classes('w-full mt-2 p-5 bg-emerald-50/50 rounded-xl border border-emerald-100 gap-4') as area_filtros:
                        area_filtros.visible = False # Esconde ao iniciar
                        
                        ui.label('Filtros e Facetas').classes('text-sm font-bold text-emerald-900 uppercase tracking-wider')
                        
                        with ui.row().classes('w-full gap-4'):
                            descritor = ui.input(label='Descritor MeSH/DeCS', placeholder='Ex: Neoplasias').classes('flex-grow')
                            tipo_doc = ui.select(label='Tipo de Documento', options=['Todos', 'Artigo Original', 'Revisão Sistemática'], value='Todos').classes('w-1/3')
                        
                        with ui.row().classes('w-full justify-end gap-3 mt-2'):
                            ui.button('Limpar', on_click=lambda: [descritor.set_value(''), tipo_doc.set_value('Todos')]).classes('bg-white text-slate-600 hover:bg-slate-100 rounded-lg px-4 border border-slate-200 shadow-none')
                            ui.button('Aplicar Filtros', icon='filter_list').classes('bg-emerald-700 hover:bg-emerald-800 text-white font-medium rounded-lg px-6 shadow-sm')

                # --------------------------------------------------------
                # 2. ÁREA DE RESULTADOS
                # --------------------------------------------------------
                with ui.column().classes('w-full gap-4 mt-2'):
                    ui.label('Acervo Recente').classes('text-lg font-bold text-emerald-900 ml-2')
                    
                    # Card de Exemplo Estilizado
                    with ui.card().classes('w-full p-6 bg-white rounded-2xl shadow-sm border border-emerald-100 border-l-4 border-l-emerald-600 gap-2 hover:bg-slate-50 transition-colors cursor-pointer'):
                        ui.label('Avaliação de estratégias de busca em bases de dados biomédicas').classes('text-lg font-bold text-slate-900')
                        ui.label('Autores: Silva, M. et al. • Ano: 2026 • DOI: 10.1016/j.jbi.2026.100').classes('text-xs text-slate-400 font-medium')
                        ui.label('Resumo descritivo focado na clareza visual e na legibilidade dos metadados extraídos automaticamente do artigo científico.').classes('text-sm text-slate-600 leading-relaxed mb-2')
                        
                        with ui.row().classes('gap-2'):
                            ui.badge('MeSH: Information Retrieval', color='green').classes('text-xs')
                            ui.badge('Evidence-Based Practice', color='green').classes('text-xs')

        # --- ABA 2: SUBMISSÃO ---
        with ui.tab_panel(tab_submissao).classes('p-0 pt-4'):
            with ui.card().classes('w-full max-w-3xl mx-auto p-8 bg-white rounded-2xl shadow-sm border border-emerald-100 gap-4'):
                ui.label('Cadastrar Novo Documento').classes('text-xl font-bold text-emerald-900')
                ui.label('Insira o DOI para recuperação automática ou preencha manualmente os campos.').classes('text-xs text-slate-500 mb-2')
                
                with ui.row().classes('w-full items-end gap-3'):
                    ui.input(label='DOI do Artigo', placeholder='10.xxxx/...').classes('flex-grow')
                    ui.button('Buscar DOI', icon='cloud_download').classes('bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl')

                ui.input(label='Título').classes('w-full')
                ui.input(label='Autores').classes('w-full')
                ui.textarea(label='Resumo').classes('w-full')
                
                ui.upload(label='Arraste o arquivo PDF aqui ou clique para selecionar').classes('w-full border-2 border-dashed border-emerald-200 rounded-2xl p-4')
                
                ui.button('Salvar no Repositório', icon='save').classes('w-full bg-emerald-700 hover:bg-emerald-800 text-white font-medium rounded-xl py-3 mt-2')

# Inicialização do Servidor para o Render
port = int(os.environ.get('PORT', 8080))
ui.run(port=port, host='0.0.0.0', title='Repositório Sofia', reload=False)
