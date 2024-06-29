import tiktoken

modelo = "gpt-4"
codificiador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificiador.encode("Você é um categorizador de produtos.")

print("Lista de Tokens: ", lista_tokens)
print("Quanto tokens temos: ", len(lista_tokens))
print (f"Custo para o modelo {modelo} é de ${(len(lista_tokens) / 1000) * 0.03}")

modelo = "gpt-3.5-turbo-1106"
codificiador = tiktoken.encoding_for_model(modelo)
lista_tokens = codificiador.encode("Você é um categorizador de produtos.")

print("Lista de Tokens: ", lista_tokens)
print("Quanto tokens temos: ", len(lista_tokens))
print (f"Custo para o modelo {modelo} é de ${(len(lista_tokens) / 1000) * 0.001}")

print(f"O custo do GPT4 é de {0.03/0.001} maior que o do GPT 3.5-turbo")