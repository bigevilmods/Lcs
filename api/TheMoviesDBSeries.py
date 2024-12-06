import json
import requests

# Configuração da API TMDB
API_KEY = "39bf687cd808abe9fbae74dd81f4a967"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movie_data(movie_id):
    """
    Busca informações sobre um filme ou série pelo ID no TMDB.
    
    :param movie_id: ID do filme ou série no TMDB.
    :return: Dicionário com os dados do filme/série ou None em caso de erro.
    """
    url = f"{BASE_URL}/tv/{movie_id}"
    params = {"api_key": API_KEY, "language": "pt-BR"}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Formata os dados no formato necessário
        movie_data = {
            "id": data.get("id", "N/A"),
            "mimeType": "MP4",  # Definido como padrão
            "category": "series",  # Categoria padrão
            "title": data.get("title", "N/A"),
            "tag": ", ".join(genre['name'] for genre in data.get("genres", [])),
            "poster": f"https://image.tmdb.org/t/p/w500{data.get('poster_path', '')}" if data.get('poster_path') else "N/A",
            "description": data.get("overview", "Sem descrição disponível")
        }
        return movie_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados do filme/série (ID: {movie_id}): {e}")
        return None

def salvar_json(data, filename="api.json"):
    """
    Salva os dados em um arquivo JSON.
    
    :param data: Dicionário com os dados a serem salvos.
    :param filename: Nome do arquivo JSON.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Dados salvos com sucesso em '{filename}'!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

if __name__ == "__main__":
    # Carrega o JSON existente ou inicializa
    try:
        with open("api.json", "r", encoding="utf-8") as file:
            dados_existentes = json.load(file)
    except FileNotFoundError:
        dados_existentes = {"content": []}
        print("Nenhum arquivo JSON encontrado. Criando um novo.")

    while True:
        print("\n--- Busca de Filmes ou Séries no TMDB ---")
        movie_id = input("Digite o ID do filme ou série (ou 'sair' para finalizar): ").strip()

        if movie_id.lower() == "sair":
            print("Finalizando o script. Até logo!")
            break

        # Busca dados do filme/série
        movie_data = fetch_movie_data(movie_id)
        if movie_data:
            # Adiciona os dados ao JSON existente
            dados_existentes["content"].append(movie_data)

            # Salva os dados atualizados
            salvar_json(dados_existentes)
        else:
            print(f"Não foi possível buscar dados para o ID: {movie_id}")
