from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()

            return dados
    except IOError as e:
        print(f"Erro: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def analisar_transacao(lista_transacoes):
    print("1.Executando a análise de transação")

    prompt_sistema = """
        Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou deve ser "Aprovada".
        Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovada".

        Cada nova transação deve ser inserida dentro da lista do JSON.

        # Possíveis indicações de fraude
        - Transações com valores muito discrepantes
        - Transações que ocorrem em locais muito distantes um do outro

        Adote o formato de resposta abaixo para compor sua resposta.

        # Formato de Saída
        {
            "transacoes": [
                {
                    "id": "id",
                    "tipo": "crédito ou débito",
                    "estabelecimento": "nome do estabelecimento",
                    "horario": "horário da transação",
                    "valor": "R$XX,XX",
                    "nome_produto": "nome do produto",
                    "localização": "cidade - estado (País)",
                    "status": ""
                },
            ]
        }
    """

    lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": f"Consider o CSV abaixo, onde cada linha é uma transação diferente: {lista_transacoes}. Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)"
        }
    ]

    resposta = cliente.chat.completions.create(
        messages = lista_mensagens,
        model = modelo,
        temperature = 0
    )

    conteudo = resposta.choices[0].message.content.replace("'", '"')
    
    print("\nConteúdo:", conteudo)
    
    json_resultado = json.loads(conteudo)

    print("\nJSON:", json_resultado)

    print("Finalizou a análise de transação")

    return json_resultado

def gerar_parecer(transacao):
    print("2. Gerando parecer")

    prompt_sistema = f"""
        Para a seguinte transação, forneça um parecer, apenas se o status dela for de "Possível Fraude". 
        Indique no parecer uma justificativa para que você indentifique uma fraude.

        Transação: {transacao}.

        ## Formato de Saída
        "id": "id",
        "tipo": "crédito ou débito",
        "estabelecimento": "nome do estabelecimento",
        "horario": "horário da transação",
        "valor": "R$XX,XX",
        "nome_produto": "nome do produto",
        "localização": "cidade - estado (País)",
        "status": ""
        "parecer": "Colocar Não Aplicável se o status for Aprovado"
    """

    lista_mensagens = [
        {
            "role": "user",
            "content": prompt_sistema
        }
    ]

    resposta = cliente.chat.completions.create(
        messages = lista_mensagens,
        model = modelo
    )

    conteudo = resposta.choices[0].message.content

    print("Finalizou a geração do parecer")

    return conteudo

def gerar_recomendacao(parecer):
    print("3. Gerando recomendação")

    prompt_sistema = f"""
        Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes da transação: {parecer}.

        As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-Fraude", "Realizar Verificação Manual".

        Elas devem ser escrita no formato técnico

        Inclua também uma classificação do tipo de fraude se aplicável.
    """

    lista_mensagens = [
        {
            "role": "user",
            "content": prompt_sistema
        }
    ]

    resposta = cliente.chat.completions.create(
        messages = lista_mensagens,
        model = modelo
    )

    conteudo = resposta.choices[0].message.content

    print("Finalizou a geração de recomendação")

    return conteudo

def identificar_responsavel(perfil_usuario, lista_de_usuarios):
    print("4. Identificando usuário responsável")

    prompt_sistema = f"""
        Você é um assistente de segurança de dados e prevenção contra fraudes.
        Considere o seguinte perfil: {perfil_usuario}
        Recomende qual dos colaboradores da empresa é o mais indicado para ser notificado, de acordo com o seu cargo e atribuições

        #### Lista de Colaboradores
        {lista_de_usuarios}

        A saída deve ser apenas o nome do usuário e o contato. 
    """

    resposta = cliente.chat.completions.create(
        model = modelo,
        messages =[
            {
                "role": "system",
                "content": prompt_sistema
            }
        ]
    )

    conteudo = resposta.choices[0].message.content

    return conteudo

lista_de_transacoes = carrega("transacoes.csv")

transacoes_analisadas = analisar_transacao(lista_de_transacoes)

for uma_transacao in transacoes_analisadas["transacoes"]:
    if uma_transacao["status"] == "Possível Fraude":
        um_parecer = gerar_parecer(uma_transacao)
        recomendacao = gerar_recomendacao(um_parecer)
        id_transacao = uma_transacao["id"]
        produto_transacao = uma_transacao["nome_produto"]
        status_transacao = uma_transacao["status"]

        salva(f"transacao-{id_transacao}-{produto_transacao}-{status_transacao}.txt", recomendacao)