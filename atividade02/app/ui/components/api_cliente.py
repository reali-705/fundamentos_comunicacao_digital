import requests

'''A função converter_texto_para_morse é responsável por enviar uma requisição POST para a API de tradução de 
texto para Morse.'''
def converter_texto_para_morse(texto: str, frequencia: int = 800):
    API_URL = "http://127.0.0.1:8000/api/tradutor/texto-para-som"
    
    ''''O payload é um dicionário que contém o texto original a ser convertido e as frequências para os 
    pontos e traços, que são enviadas como parte da requisição para a API. O valor padrão para as 
    frequências é 800 Hz, mas pode ser ajustado conforme necessário. A API deve processar esse payload e 
    retornar o código Morse correspondente.'''
    
    payload = {
        "texto_original": texto,
        "frequencia_ponto": frequencia,
        "frequencia_traco": frequencia 
    }

    '''esse bloco tenta fazer a requisição e trata erros de conexão ou erros retornados pela API, 
    levantando exceções com mensagens apropriadas. O resultado esperado é um dicionário contendo 
    o código Morse e um ID da conversão, caso a requisição seja bem-sucedida. '''

    try:
        response = requests.post(f"{API_URL}", json=payload)
        if response.status_code == 201:
            return response.json() #retorna o JSON da resposta, que deve conter o código Morse e o ID da conversão
        else:
            erro_msg = response.json().get("detail", "Erro desconhecido ao converter o texto.")
            raise Exception(erro_msg) #raise uma exceção com a mensagem de erro retornada pela API
    except requests.exceptions.ConnectionError:
        raise Exception("Não foi possível conectar à API. Verifique se o servidor está rodando.")

def iniciar_gravacao_audio():
    API_URL = f"http://127.0.0.1:8000/api/iniciar-gravacao"

    try:
        response = requests.post(API_URL, json={})
        if response.status_code == 201:
            return response.json()
        else:
            erro_msg = response.json().get("detail", "Erro desconhecido ao iniciar a gravação.")
            raise Exception(erro_msg)
    except requests.exceptions.ConnectionError:
        raise Exception("Não foi possível conectar à API. Verifique se o servidor está rodando.")
