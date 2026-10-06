---
name: ollama-api
description: Use ao chamar um modelo local do Ollama por código (chat, tool-calling, parâmetros, escolha de modelo) ou ao decidir qual dos modelos baixados serve para a tarefa. Explica o que é o /api/chat, como tool_calls funcionam e os limites da RTX 4060 de 8 GB (máquina atual desde 04/10/2026).
---

# API do Ollama (local)

## O básico
- Servidor em `http://localhost:11434` (app do Ollama na bandeja ou `ollama serve`).
- `GET /api/tags` lista modelos. `POST /api/chat` conversa. Cliente pronto em
  `src/lab/ollama_client.py` (`chat`, `chat_messages`, `listar_modelos`).
- Um "modelo" no Ollama = pesos quantizados (Q4_K_M na maioria) + Modelfile com template de
  chat e parâmetros padrão. `ollama show qwen3:8b` mostra.

## Qual modelo para quê

`ollama list` é a fonte de verdade. Baixados na máquina atual (05/10/2026): `qwen3:8b` e
`qwen3-coder:30b`. Os demais da tabela existiam na máquina antiga (avaliação de 10/09);
baixar com `ollama pull` antes de comparar.

| Modelo | Bom para | Evitar para | Nota |
|---|---|---|---|
| `qwen3:8b` | tool-calling, código, PT-BR razoável | — | melhor generalista local; suporta `think` |
| `llama3.1:8b` | tool-calling, texto | raciocínio longo | segundo melhor com ferramenta |
| `mistral:7b` | rápido, resumo, classificação | tool-calling complexo | mais leve dos 4 |
| `deepseek-r1:8b` | raciocínio passo a passo, matemática | tool-calling | ignora `tools`; sempre "pensa" |
| `qwen3-coder:30b` | agente pronto (Qwen Code), site/código multi-arquivo | pressa | MoE 18 GB; ctx 32k = 20 GB, 69/31 CPU/GPU; precisa da instrução de formato (ver abaixo) |
| `gemma4:31b-cloud` | qualidade alta | **dado sensível** | roda na nuvem do Ollama, não na máquina |

## Parâmetros que importam em 8 GB de VRAM (RTX 4060 Laptop, 32 GB RAM)
- `num_ctx` (janela): 8B Q4 com 8192 = 5,6 GB, **100% GPU** (medido 04/10). Com 32k =
  8,1 GB, 22/78 CPU/GPU: o que não cabe vai para a RAM e fica bem mais lento. Não pedir 32k
  "por garantia". Conferir sempre com `ollama ps` (coluna PROCESSOR).
- Log anterior a 04/10 foi medido na máquina antiga (RTX 4050 6 GB / 15,7 GB): lá o mesmo 8B
  com ctx 32k dividia 50/50 CPU/GPU. Tempo e % GPU daquela época não se comparam com os de agora.
- `temperature`: 0–0,3 para tarefa com ferramenta ou extração; 0,7+ só para texto criativo.
- `think`: qwen3 e deepseek-r1 geram raciocínio oculto antes da resposta. `think=False`
  corta o tempo em tarefa simples. Ligar só quando a taxa de acerto medir que vale.
- Com 32 GB de RAM cabem o 8B e o resto do sistema com folga; o `qwen3-coder:30b` também
  roda (parte na CPU). Dois modelos carregados ao mesmo tempo disputam os 8 GB de VRAM: o
  segundo cai para a CPU. O Ollama descarrega sozinho depois de 5 min ocioso (`keep_alive`).

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
- Resposta de ferramenta longa (>4k chars) faz o modelo perder o fio. Truncar
  (`tools.TETO_CHARS`; `listar_pasta` corta em `TETO_ITENS`).
- Modelo inventa **argumento** (`max_chars=10**9`, `timeout_s=99999`). `tools.executar` só
  repassa o que está nas `properties` do schema, avisa o que descartou, e os tetos ficam
  fixos no código: o modelo não sobe.
- `ollama run modelo` no terminal é **chat puro**: não tem ferramenta, não abre site, não cria
  arquivo. Quem age é o harness (este projeto, ou Claude Code apontado pro Ollama).

## Ollama como backend de agente pronto (medido 04–05/10, ver experiments/log.md)
- **Claude Code + `qwen3:8b`**: falha, "Prompt is too long" (o prompt do Claude Code + config
  do usuário passa de 32k; com 8 GB não cabe).
- **Qwen Code + `qwen3:8b`**: 0/2, chama ferramenta inexistente e entra em loop.
- **Qwen Code + `qwen3-coder:30b`**: 0/2 sem ajuste (escreve texto antes da chamada e o parser
  do Ollama não reconhece); **3/3** com a instrução de formato em `~/.qwen/QWEN.md` ("não
  escreva texto antes da chamada; comece com `<tool_call>`"). Prompt de 17–19k tokens leva
  minutos para ser lido: subir os timeouts do Qwen Code (ver log de 04/10).
- Para tarefa pequena e dado que não pode sair da máquina, o agente do lab (`lab.agent`) com
  `qwen3:8b` é o mais rápido (6–9 s/tarefa, 15/15 na bateria fácil).
