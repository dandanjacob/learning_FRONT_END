import os
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph, END
from dotenv import load_dotenv, find_dotenv


class LangGraphChatbot:
    def __init__(self):
        # Carregar variáveis de ambiente
        _ = load_dotenv(find_dotenv())

        # Configurar o modelo de linguagem (ChatGPT)
        self.chat_model = ChatOpenAI(model="gpt-4", temperature=0.7)

        # Criar o grafo
        self.graph = self._create_workflow()

    def _create_workflow(self):
        # Criando o grafo
        workflow = Graph()

        # Adicionando nós
        workflow.add_node("saudacao", self.saudacao)
        workflow.add_node("responder", self.responder_pergunta)
        workflow.add_node("despedida", self.despedida)
        workflow.add_node("esperar_entrada", self.esperar_entrada)

        # Definindo o nó inicial
        workflow.set_entry_point("saudacao")

        # Ajustando o fluxo após a saudação
        workflow.add_edge("saudacao", "esperar_entrada")

        # Adicionando arestas condicionais
        workflow.add_conditional_edges(
            "esperar_entrada",  # Agora a decisão ocorre após esperar a entrada do usuário
            self.decidir_proximo_passo,
            {"responder": "responder", "despedida": "despedida"},
        )

        workflow.add_edge(
            "responder", "esperar_entrada"
        )  # Após responder, volta para esperar a entrada

        # Adicionando aresta final
        workflow.add_edge("despedida", END)

        # Compilar o grafo
        return workflow.compile()

    # Funções dos nós
    def saudacao(self, estado):
        estado["mensagem"] = "Olá! Como posso ajudar você hoje?"
        print("Bot:", estado["mensagem"])
        return estado

    def responder_pergunta(self, estado):
        # Usar o ChatGPT para gerar uma resposta
        resposta = self.chat_model.invoke(
            estado["input"]
        )  # Substituído predict por invoke
        estado["mensagem"] = resposta.content  # Acessar o conteúdo da resposta
        print("Bot:", estado["mensagem"])
        return estado

    def despedida(self, estado):
        estado["mensagem"] = "Até logo! Foi um prazer ajudar."
        print("Bot:", estado["mensagem"])
        return estado

    # Função para decidir o próximo nó
    def decidir_proximo_passo(self, estado):
        texto = estado["input"]
        if "tchau" in texto.lower():
            return "despedida"  # Vai direto para o nó de despedida
        else:
            return "responder"

    # Função para esperar a entrada do usuário
    def esperar_entrada(self, estado):
        estado["input"] = input("Você: ")
        # print("Você: ", estado["input"])
        return estado

    # Função para interagir com o bot
    def interagir_com_bot(self):
        estado = {"input": ""}
        while True:
            resultado = self.graph.invoke(estado)
            if resultado.get("mensagem") == "Até logo! Foi um prazer ajudar.":
                break
            estado = {"input": ""}


def main():
    # Inicializar o chatbot
    chatbot = LangGraphChatbot()

    # Iniciar a interação com o bot
    chatbot.interagir_com_bot()


if __name__ == "__main__":
    main()

'''
e tenho esse arquivo main.py:
'''python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chat import LangGraphChatbot  # Importar a classe do chatbot

# Inicialize o FastAPI
app = FastAPI()

# Inicialize o seu chatbot
chatbot = LangGraphChatbot()


# Modelo de entrada para a API
class ChatInput(BaseModel):
    message: str


# Rota para enviar mensagens ao chatbot
@app.post("/chat/")
async def chat(input: ChatInput):
    try:
        # Processe a mensagem com o chatbot
        response = chatbot.interagir_com_bot(input.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Rota de saúde para verificar se a API está funcionando
@app.get("/health")
async def health():
    return {"status": "ok"}