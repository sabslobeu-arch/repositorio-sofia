import sys
from pathlib import Path
from nicegui import ui

# Configura diretório de dados local/pen-drive
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

DB_PATH = BASE_DIR / "dados_repositorio.db"
PDF_DIR = BASE_DIR / "uploads_pdf"
PDF_DIR.mkdir(exist_ok=True)

# Interface da Aplicação
ui.label('Repositório Científico Portátil').classes('text-2xl font-bold mb-4')
ui.label(f'Diretório de dados: {BASE_DIR}').classes('text-sm text-gray-500 mb-4')

ui.input(label='Informe o DOI').classes('w-full mb-2')
ui.button('Salvar no Repositório', on_click=lambda: ui.notify('Salvo com sucesso!')).classes('bg-blue-600 text-white')

# Executa a aplicação
ui.run(
    title='Repositório Científico',
    port=8080,
    native=False, # Deixe False para rodar na web (Replit/Railway) ou True para pen-drive
    reload=False
)
