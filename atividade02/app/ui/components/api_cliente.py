import requests

def converter_texto_para_morse(texto: str, frequencia: int = 800):
    # Esta função faz uma requisição POST para a API de tradução de texto para Morse e retorna o resultado.
    API_URL = "http://127.0.0.1:8000/api/tradutor/texto-para-som"
    payload = {
        "texto_original": texto,
        "frequencia": frequencia
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

