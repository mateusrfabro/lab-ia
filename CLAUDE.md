# lab-ia — laboratório de modelos de IA locais

## O que é este projeto

Laboratório PESSOAL do Mateus (analista de dados, iGaming, Super Nova) para **rodar, ajustar e
treinar modelos na própria máquina**. Três trilhas, cada uma com sua pasta em `src/lab/`:

| Trilha | Pasta | O que é | Estado (10/09/2026) |
|---|---|---|---|
| **A. Agente local** | `src/lab/agent/` | modelo do Ollama + loop de ferramentas (ler/escrever arquivo, listar pasta, rodar Python) | esqueleto pronto e testado |
| **B. Fine-tuning** | `src/lab/finetune/` | QLoRA em modelo de 1,5B–3B, cabe em 6 GB de VRAM | stack instalada (torch cu126, cuda=True); treino real ainda não rodado, falta dataset |
| **C. ML tabular** | `src/lab/tabular/` | churn / risco / propensão com sklearn, XGBoost, LightGBM (CPU) | esqueleto pronto e testado |

Não é o play4tune. Aqui não tem regra de tenant, banco do jogador nem EC2. **Mas dado do P4T
que entrar aqui segue as regras de lá** (ver "Dados" abaixo).

## Máquina (medido em 10/09/2026 — reconferir com `python scripts/check_env.py`)

| Item | Valor | Implicação |
|---|---|---|
| GPU | NVIDIA RTX 4050 Laptop, **6 GB VRAM**, driver 573.22 | inferência 8B Q4 ok (parte na CPU); QLoRA só até ~3B |
| RAM | 15,7 GB | não abrir dois modelos 8B ao mesmo tempo |
| CPU | i5-13420H | ML tabular roda bem aqui |
| Disco | 74 GB livres (10/09) | cada modelo 8B ≈ 5 GB; torch+CUDA ≈ 3 GB |
| Python | 3.12.10 (venv em `.venv/`) | |
| Docker | 29.4.1 | |

## Modelos já baixados (Ollama, `~/.ollama/models`, ~19 GB)

`ollama list` é a fonte de verdade. Em 10/09: `qwen3:8b`, `deepseek-r1:8b`, `llama3.1:8b`,
`mistral:7b` (locais) e `gemma4:31b-cloud` (**roda na nuvem do Ollama, não é local** — não usar
para dado sensível). API em `http://localhost:11434`. Os pesos ficam FORA deste repo, no
`~/.ollama`; nunca copiar pra cá.

**Para tarefa com ferramenta (trilha A) o melhor dos 4 é o `qwen3:8b`** (suporte nativo a
tool-calling). `deepseek-r1` é de raciocínio, ruim com ferramentas. `mistral:7b` é o mais rápido.

## Regras deste projeto

1. **Venv sempre.** `.\.venv\Scripts\Activate.ps1` (PowerShell) antes de qualquer `python`.
   Instalação: `.\setup.ps1` (base) e `.\setup.ps1 -Llm` (torch CUDA + transformers + peft).
2. **Nada de peso de modelo nem dado no git.** `data/`, `outputs/`, `*.gguf`, `*.safetensors`,
   `*.pt`, checkpoints — tudo no `.gitignore`. Se um arquivo passar de 10 MB, ele não é código.
3. **Todo experimento vira uma linha em `experiments/log.md`** (data, trilha, modelo, dado,
   métrica, baseline, conclusão em 1 frase). Skill `experimento-log`. Experimento sem linha não existiu.
4. **Dados:** anonimizados antes de entrar em `data/raw/` (sem nome, e-mail, telefone, documento,
   IP). Extração do P4T roda **no analítico** (`supernova_db`) usando o conector do repo do
   play4tune, nunca daqui e nunca no `supernova_bet`. Dado real de jogador **não vai** para
   modelo cloud (`*-cloud`) nem para API externa.
5. **Métrica de ML sempre com baseline burro ao lado** (maioria / média / regra simples).
   AUC 0,80 sem baseline não diz nada. Skill `ml-tabular-baseline` tem o checklist de leakage.
6. **Fine-tuning:** antes de treinar, provar que o prompt puro não resolve (few-shot no mesmo
   modelo). Treino é o último recurso, não o primeiro. Skill `qlora-6gb`.
7. **Honestidade sobre capacidade:** modelo 8B local erra muito em uso de ferramenta. Registrar
   taxa de acerto medida, não impressão. "Funcionou uma vez" não é resultado.
8. **Explicar enquanto faz.** O objetivo do Mateus é construir entendimento (o que é LoRA, por
   que quantizar, o que é leakage). Cada entrega traz o "porquê", não só o "como".

## Agentes (`.claude/agents/`)

| Agente | Use quando |
|---|---|
| `ml-engineer` | trilha C: features, validação, leakage, métrica, calibração |
| `llm-tuner` | trilha B: dataset de instrução, QLoRA, avaliação antes/depois |
| `agent-builder` | trilha A: loop de ferramentas, prompts de sistema, tool schema, avaliação de tarefas |
| `revisor-experimento` | antes de registrar conclusão: checa baseline, leakage, tamanho de amostra, se o número aguenta |

**Não cole este CLAUDE.md no prompt.** Cada agente já tem um bloco "Antes de começar" que
manda ler este arquivo, as linhas da trilha dele em `experiments/log.md` e o fonte relevante —
por leitura, não por cópia (cópia envelhece quando este arquivo muda). O subagente não herda
nada: nem o `~/.claude/CLAUDE.md`, nem o histórico da conversa que o invocou.

No prompt de invocação vai só o que **não está no disco**: a tarefa concreta, o critério de
aceite (o número que conta como pronto) e a restrição da sessão (RAM livre, modelo, prazo).

## Skills (`.claude/skills/`)

`ollama-api` (chamar modelo, tool-calling, parâmetros) · `qlora-6gb` (receita que cabe na
VRAM) · `ml-tabular-baseline` (split, leakage, métrica, baseline) · `experimento-log` (formato
da linha do log).

## Comandos do dia a dia

```powershell
.\.venv\Scripts\Activate.ps1
python scripts\check_env.py                                    # GPU, torch, ollama, modelos
python -m lab.agent.run "crie data\teste.txt com 3 linhas"      # trilha A
python -m lab.tabular.baseline data\processed\x.csv --target y  # trilha C
python -m lab.finetune.qlora --help                             # trilha B
python -m pytest -q                                             # testes (não precisam de GPU)
```

## Memória

Memória do Claude para este projeto em
`C:\Users\NITRO\.claude\projects\C--Users-NITRO-Projects-lab-ia\memory\MEMORY.md`.
Memória global cross-projeto em `C:\Users\NITRO\.claude\memory-global\GLOBAL.md` — ler a seção
**Universal** no início de trabalho não-trivial; a seção iGaming só se o dado for do P4T.
