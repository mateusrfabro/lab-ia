---
name: ollama-api
description: Use ao chamar um modelo local do Ollama por código (chat, tool-calling, parâmetros, escolha de modelo) ou ao decidir qual dos modelos baixados serve para a tarefa. Explica o que é o /api/chat, como tool_calls funcionam e os limites da RTX 4050 de 6 GB.
---

# API do Ollama (local)

## O básico
- Servidor em `http://localhost:11434` (app do Ollama na bandeja ou `ollama serve`).
- `GET /api/tags` lista modelos. `POST /api/chat` conversa. Cliente pronto em
  `src/lab/ollama_client.py` (`chat`, `chat_messages`, `listar_modelos`).
- Um "modelo" no Ollama = pesos quantizados (Q4_K_M na maioria) + Modelfile com template de
  chat e parâmetros padrão. `ollama show qwen3:8b` mostra.

## Qual modelo para quê (medido em 10/09/2026, `ollama list`)

| Modelo | Bom para | Evitar para | Nota |
|---|---|---|---|
| `qwen3:8b` | tool-calling, código, PT-BR razoável | — | melhor generalista local; suporta `think` |
| `llama3.1:8b` | tool-calling, texto | raciocínio longo | segundo melhor com ferramenta |
| `mistral:7b` | rápido, resumo, classificação | tool-calling complexo | mais leve dos 4 |
| `deepseek-r1:8b` | raciocínio passo a passo, matemática | tool-calling | ignora `tools`; sempre "pensa" |
| `gemma4:31b-cloud` | qualidade alta | **dado sensível** | roda na nuvem do Ollama, não na máquina |

## Parâmetros que importam em 6 GB de VRAM
- `num_ctx` (janela): 8192 é seguro com 8B Q4. 16k já derrama para a RAM e fica 3-5× mais
  lento. Não pedir 32k "por garantia".
- `temperature`: 0–0,3 para tarefa com ferramenta ou extração; 0,7+ só para texto criativo.
- `think`: qwen3 e deepseek-r1 geram raciocínio oculto antes da resposta. `think=False`
  corta o tempo em tarefa simples. Ligar só quando a taxa de acerto medir que vale.
- Só **um** modelo 8B carregado por vez (RAM de 15,7 GB). O Ollama descarrega sozinho depois
  de 5 min ocioso (`keep_alive`).

## Tool-calling: o que acontece de verdade
1. Você manda `tools=[{"type":"function","function":{"name","description","parameters"}}]`.
2. O modelo responde com `message.tool_calls = [{"function":{"name","arguments"}}]` em vez
   de texto.
3. **Você** executa a função e devolve `{"role":"tool","content": resultado, "tool_name": nome}`.
4. Chama o modelo de novo com o histórico. Repete até ele responder sem `tool_calls`.
Isso é o loop de `src/lab/agent/run.py`. O modelo nunca executa nada; ele só pede.

## Armadilhas vistas
- `arguments` às vezes vem como **string JSON** em vez de objeto. `run.py` já trata.
- Modelo 8B inventa nome de ferramenta que não existe. `tools.executar` devolve
  "(ferramenta desconhecida)" e o loop segue; não quebrar.
- Descrição de ferramenta longa piora o acerto. Uma frase por ferramenta.
- Resposta de ferramenta longa (>4k chars) faz o modelo perder o fio. Truncar.
- `ollama run modelo` no terminal é **chat puro**: não tem ferramenta, não abre site, não cria
  arquivo. Quem age é o harness (este projeto, ou Claude Code apontado pro Ollama).

## Ollama como backend do Claude Code
`~/.ollama/config.json` mostra integração `claude` com `qwen3:8b` já configurada (03/09).
Funciona, mas o modelo de 8B erra muito em edição de código multi-arquivo. Usar para tarefa
pequena e dado que não pode sair da máquina; para o resto, Claude.
