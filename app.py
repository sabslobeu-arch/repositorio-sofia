import os
from nicegui import ui, app

# Configuração global de fundo (tom claro esverdeado suave)
ui.query('body').style('background-color: #f0fdf4;')

# --- CABEÇALHO ---
with ui.row().classes('w-full items-center justify-between bg-white px-8 py-4 shadow-sm border-b border-emerald-100'):
    with ui.row().classes('items-center gap-4'):
        # Mantemos um ícone discreto ou o nome no topo
        ui.label('Repositório Sofia').classes('text-lg font-bold text-emerald-800 tracking-tight')
    ui.badge('Online', color='green').classes('text-xs px-3 py-1')

# --- ÁREA PRINCIPAL (COM A IMAGEM GRANDE E BUSCA) ---
with ui.column().classes('w-full items-center justify-center py-12 px-4 gap-6'):
    
    # Imagem grande em destaque (substitua pelo seu link Raw do GitHub)
    ui.image('https://github.com/sabslobeu-arch/repositorio-sofia/blob/main/logo-sofia.png').classes('w-96 max-w-lg h-auto object-contain rounded-xl shadow-md')
    
    # Título de boas-vindas
    ui.label('Biblioteca Virtual de Evidências Médicas').classes('text-2xl font-bold text-emerald-950 text-center')
    
    # Caixa de Pesquisa em Destaque
    with ui.card().classes('w-full max-w-2xl p-6 bg-white shadow-lg rounded-2xl border border-emerald-100 gap-4'):
        ui.label('Pesquisar na Base de Conhecimento').classes('font-semibold text-emerald-800 text-sm')
        
        with ui.row().classes('w-full items-center gap-2'):
            search_input = ui.input(placeholder='Digite termos clínicos, DOI ou palavras-chave...').classes('flex-grow')
            ui.button('Buscar', on_click=lambda: ui.notify(f'Buscando por: {search_input.value}')).classes('bg-emerald-700 text-white hover:bg-emerald-800')

 
    # --- CONTEÚDO PRINCIPAL COM ABAS ESTILIZADAS ---
    with ui.column().classes('w-full max-w-7xl mx-auto p-6 gap-6'):
        
        with ui.tabs().classes('w-full bg-white rounded-xl shadow-sm p-1 text-slate-700') as tabs:
            tab_busca = ui.tab('Acervo & Busca', icon='search').classes('rounded-lg transition')
            tab_submissao = ui.tab('Nova Submissão', icon='upload_file').classes('rounded-lg transition')

        with ui.tab_panels(tabs, value=tab_busca).classes('w-full bg-transparent'):
            
            # --- ABA 1: BUSCA ---
            with ui.tab_panel(tab_busca).classes('p-0 pt-4'):
                with ui.row().classes('w-full gap-6'):
                    
                    # Filtros (Esquerda)
                    with ui.card().classes('w-1/4 p-6 bg-white rounded-2xl shadow-sm border border-slate-100 gap-4'):
                        ui.label('Filtros e Facetas').classes('text-base font-bold text-slate-800')
                        ui.separator()
                        ui.input(label='Descritor MeSH/DeCS', placeholder='Ex: Neoplasias').classes('w-full')
                        ui.select(label='Tipo de Documento', options=['Todos', 'Artigo Original', 'Revisão Sistemática'], value='Todos').classes('w-full')
                        ui.button('Aplicar Filtros', icon='filter_list').classes('w-full bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl shadow-sm')

                    # Resultados (Direita)
                    with ui.column().classes('w-3/4 gap-4'):
                        with ui.row().classes('w-full items-center gap-3 bg-white p-4 rounded-2xl shadow-sm border border-slate-100'):
                            ui.input(placeholder='Busca avançada por título, resumo ou operadores booleanos...').classes('flex-grow border-none')
                            ui.button(icon='search').classes('bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-5')
                        
                        # Card de Exemplo Estilizado
                        with ui.card().classes('w-full p-6 bg-white rounded-2xl shadow-sm border border-slate-100 border-l-4 border-l-blue-600 gap-2'):
                            ui.label('Avaliação de estratégias de busca em bases de dados biomédicas').classes('text-lg font-bold text-slate-900')
                            ui.label('Autores: Silva, M. et al. • Ano: 2026 • DOI: 10.1016/j.jbi.2026.100').classes('text-xs text-slate-400 font-medium')
                            ui.label('Resumo descritivo focado na clareza visual e na legibilidade dos metadados extraídos automaticamente do artigo científico.').classes('text-sm text-slate-600 leading-relaxed mb-2')
                            
                            with ui.row().classes('gap-2'):
                                ui.badge('MeSH: Information Retrieval', color='blue').classes('text-xs')
                                ui.badge('Evidence-Based Practice', color='green').classes('text-xs')

            # --- ABA 2: SUBMISSÃO ---
            with ui.tab_panel(tab_submissao).classes('p-0 pt-4'):
                with ui.card().classes('w-full max-w-3xl mx-auto p-8 bg-white rounded-2xl shadow-sm border border-slate-100 gap-4'):
                    ui.label('Cadastrar Novo Documento').classes('text-xl font-bold text-slate-800')
                    ui.label('Insira o DOI para recuperação automática ou preencha manualmente os campos.').classes('text-xs text-slate-500 mb-2')
                    
                    with ui.row().classes('w-full items-end gap-3'):
                        ui.input(label='DOI do Artigo', placeholder='10.xxxx/...').classes('flex-grow')
                        ui.button('Buscar DOI', icon='cloud_download').classes('bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl')

                    ui.input(label='Título').classes('w-full')
                    ui.input(label='Autores').classes('w-full')
                    ui.textarea(label='Resumo').classes('w-full')
                    
                    ui.upload(label='Arraste o arquivo PDF aqui ou clique para selecionar').classes('w-full border-2 border-dashed border-slate-200 rounded-2xl p-4')
                    
                    ui.button('Salvar no Repositório', icon='save').classes('w-full bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl py-3 mt-2')

main()
port = int(os.environ.get('PORT', 8080))

ui.run(port=port, host='0.0.0.0', title='Repositório', reload=False)
