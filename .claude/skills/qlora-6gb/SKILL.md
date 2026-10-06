---
name: qlora-6gb
description: Use antes de qualquer fine-tuning de LLM neste laboratório — decide se treinar é a resposta, escolhe modelo que cabe em 8 GB de VRAM (RTX 4060 desde 04/10/2026; a pasta mantém o nome antigo "6gb"), define a receita QLoRA (NF4 + LoRA + gradient checkpointing), o formato do dataset, a avaliação antes/depois obrigatória e o caminho do adapter até o Ollama (merge, GGUF, Modelfile gerado, teste de concordância).
---

# QLoRA em 8 GB (RTX 4060 Laptop, 32 GB RAM)

> **Nome da pasta é histórico.** A skill nasceu como `qlora-6gb` na RTX 4050 de 6 GB (máquina
> antiga, até 10/09/2026). Desde 04/10/2026 o lab roda na RTX 4060 Laptop de **8 GB** e a receita
> abaixo é para 8 GB. O nome ficou para não quebrar referência (agente `llm-tuner`, CLAUDE.md).

## Estado medido (06/10/2026)
- **Nenhum treino rodou ainda**, nem na máquina antiga nem nesta. Todo número de VRAM e tempo
  abaixo é **estimativa** até virar linha no `experiments/log.md`.
- A venv nova (Python 3.12) está **sem** a stack de LLM: `torch`, `transformers`, `peft`,
  `bitsandbytes`, `datasets`, `accelerate` não importam (conferido com `importlib` em 06/10). A
  instalação cu126 do log de 10/09 foi na máquina antiga. Rodar `.\setup.ps1 -Llm` antes do 1º
  treino e conferir `cuda=True` com `python scripts\check_env.py`.

## Antes de treinar: a pergunta que evita 90% dos treinos inúteis
Fine-tuning ensina **forma** (formato de saída, estilo, vocabulário do domínio, seguir um
esquema). Não ensina **fatos** de forma confiável (fato muda; RAG ou contexto no prompt fazem
melhor). Então:
1. Escrever 10 exemplos do que se quer.
2. Testar few-shot no modelo base via Ollama (`qwen3:8b` com 3-5 exemplos no prompt).
3. Se acertar ≥ 80%, **não treinar**. Registrar no log e usar o prompt.
4. Se não, montar dataset e treinar. A prova do passo 2 vai na linha do log.

## O que cabe na 4060 de 8 GB

QLoRA, seq 1024, batch 1, grad_accum 8, gradient checkpointing ligado.

| Modelo | VRAM (est.) | Época com 500 ex (est.) | Veredito |
|---|---|---|---|
| Qwen2.5-1.5B-Instruct | ~3 GB | ~10-15 min | começar aqui; o 1º treino é para medir, não para ganhar |
| Qwen2.5-3B-Instruct / Llama-3.2-3B | ~5 GB | ~25-40 min | **cabe com folga** (era o limite na 4050) |
| Qwen3-4B-Instruct-2507 | ~6-7 GB | ~40-60 min | **novo teto confortável**; medir antes de confiar |
| 7-8B (Qwen2.5-7B, Llama 3.1 8B, Mistral 7B) | ~7-8 GB **só** com `--max-len 512 --r 8` | horas | **experimento**, não receita: encosta no teto e no Windows transborda (abaixo) |

Tudo nesta tabela é **estimativa** (conta de pesos NF4 + embeddings + ativações), nada foi medido
nesta máquina. O script imprime o pico de VRAM reservada no fim; a primeira rodada de cada
tamanho substitui o "~" da tabela por um número medido. Se faltar memória:
`--max-len 512` → `--r 8` → modelo menor, nessa ordem. Nunca "tentar de novo igual".

Notas por modelo:
- **Llama-3.2** não tem token de pad: o script faz pad=eos e avisa. O
  `DataCollatorForLanguageModeling` mascara o pad no label, então **o EOS também sai do label**
  e o modelo pode não aprender a parar. Qwen2.5 e Qwen3 têm pad próprio e não caem nisso.
- **Phi-3/3.5** (3,8B) usa `qkv_proj` e `gate_up_proj` fundidos: os `target_modules` do script
  só pegariam `o_proj` e `down_proj`, em silêncio. Não usar sem ajustar a lista.
- 7-8B: inferência no Ollama funciona bem (qwen3:8b, 5,6 GB, 100% GPU, medido 04/10). Treinar
  é outra conta: pesos NF4 (~5 GB) + LoRA + otimizador + ativações.

### Aviso do Windows: VRAM cheia não dá OOM, transborda
No Windows, o driver da NVIDIA (desde a série 536) tem a **CUDA Sysmem Fallback Policy**: quando
a VRAM acaba, em vez de OOM ele passa a alocar na **memória compartilhada** (RAM do sistema,
via PCIe). O treino continua, só que de 5 a 20 vezes mais lento (estimativa), e parece que "coube".
- Sintoma: Gerenciador de Tarefas → Desempenho → GPU → "Memória compartilhada da GPU" sobe
  durante o treino; passos por segundo despencam depois de algum tempo.
- O script avisa no fim se o pico reservado passou de 92% da VRAM total (`aviso_vram`).
- Para preferir OOM honesto a lentidão silenciosa: Painel de Controle NVIDIA → Gerenciar
  configurações 3D → Configurações do programa → `python.exe` da venv → "CUDA - Sysmem Fallback
  Policy" = **Prefer No Sysmem Fallback**. Recomendado para os experimentos de 7-8B.
- 32 GB de RAM tornam esse transbordo *possível* sem travar a máquina, o que é justamente por
  que ele passa despercebido.

## As peças (uma frase cada, pra explicar na entrega)
- **Quantização NF4 (bitsandbytes)**: pesos do modelo base guardados em 4 bits ("NormalFloat",
  com níveis distribuídos como uma normal, que é como pesos se distribuem); corta a memória em
  ~4× com perda pequena de qualidade. `bnb_4bit_use_double_quant` quantiza também as constantes
  de escala e economiza mais um pouco.
- **LoRA (rank r)**: congela o modelo e treina, em cada camada de atenção/MLP, duas matrizes
  pequenas (d×r e r×d) cujo produto é a "correção" do peso. r=16 é o padrão; r=8 se faltar VRAM;
  r=32 se o dataset for grande e a tarefa difícil. `lora_alpha = 2r` é convenção segura.
- **QLoRA** = base em NF4 + LoRA em fp16. O adapter final tem dezenas de MB e se aplica sobre
  o base original.
- **Gradient checkpointing**: não guarda as ativações do forward; recomputa no backward.
  ~30% mais lento, ~50% menos VRAM. Obrigatório aqui.
- **`paged_adamw_8bit`**: otimizador com estado em 8 bits e paginado para a RAM quando aperta.
- **lr 2e-4 cosine com warmup 3%**: sobe o lr linearmente nos primeiros 3% dos passos (evita
  estragar o modelo no começo) e depois desce em curva de cosseno até ~0; padrão do paper do
  QLoRA, funciona para quase tudo.

## Dataset
- JSONL, uma linha por exemplo: `{"instruction": ..., "input": ... (opcional), "output": ...}`.
- 200-500 exemplos **revisados**. Volume não compensa exemplo errado.
- Separar o eval **antes** de treinar: 10% ou 30 exemplos, o que for maior. Nunca avaliar no treino.
- Sem dado pessoal (nome, e-mail, telefone, documento). Regra 4 do CLAUDE.md.
- O formato do texto de treino é `### Instrução:` / `### Entrada:` / `### Resposta:`, definido
  pelas constantes `CAB_INSTRUCAO`, `CAB_ENTRADA`, `CAB_RESPOSTA` em `src/lab/finetune/qlora.py`.
  É a fonte única: treino, `comparar.py` e o Modelfile do Ollama derivam dali. Ver "A armadilha
  do template" abaixo.

## Comandos
```powershell
.\setup.ps1 -Llm                                  # uma vez (~3 GB); a venv 3.12 ainda NÃO tem
python -m lab.finetune.qlora --data data\processed\treino.jsonl --dry-run
python -m lab.finetune.qlora --data data\processed\treino.jsonl --out outputs\lora-v1
python -m lab.finetune.comparar --adapter outputs\lora-v1 --eval data\processed\eval.jsonl
```
O fim do treino imprime a linha do log já com modelo, r, épocas, lr, seq, n treino, loss
final, VRAM pico e minutos; completar n eval, baseline (few-shot) e conclusão.

## Ler o treino
- Loss caindo suave até ~0,5-1,0 e estabilizando: saudável.
- Loss ~0 na 1ª época: decorou. Menos épocas, mais dados, ou dropout maior.
- Loss parada: lr, formato do prompt (não bate com o template do modelo) ou dado ruim.
- Antes/depois idêntico: o adapter não pegou; conferir se `target_modules` bate com a
  arquitetura (`model.print_trainable_parameters()` deve mostrar > 0,3%).
- Resposta que não para (repete `### Instrução:` ou segue escrevendo): EOS não foi aprendido;
  ver nota do pad=eos acima.
- Treino que "cabe" mas anda devagar demais: transbordo para memória compartilhada (acima).

## Do adapter ao Ollama

Só depois que o antes/depois (`comparar`) provar ganho no eval. O adapter LoRA sozinho não roda
no Ollama de forma confiável para qualquer arquitetura; o caminho seguro é fundir, converter,
quantizar e importar. Os arquivos ficam em `outputs\` (no `.gitignore`); se o treino usou dado
de jogador, **nada disto sai da máquina**: sem `ollama push`, sem upload ao Hugging Face.

1. **Merge em fp16, não sobre NF4.** Carregar o base em fp16 (sem `BitsAndBytesConfig`), aplicar
   o adapter e fundir:
   ```python
   base = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float16, device_map="cpu")
   m = PeftModel.from_pretrained(base, "outputs/lora-v1").merge_and_unload()
   m.save_pretrained("outputs/merged-v1", safe_serialization=True)
   AutoTokenizer.from_pretrained("outputs/lora-v1").save_pretrained("outputs/merged-v1")
   ```
   Por quê: fundir sobre o modelo em NF4 soma a correção LoRA (pequena, fp16) a pesos que serão
   arredondados de volta para 4 bits, e boa parte da correção some no arredondamento. Em fp16 a
   soma é exata. `device_map="cpu"` porque um 3B em fp16 são ~6 GB e um 4B ~8 GB: não cabem com
   folga na GPU, e com 32 GB de RAM a CPU dá conta (é uma operação de minutos, não de treino).
   Ressalva: o adapter foi treinado olhando o base *quantizado*; o modelo fundido em fp16 não é
   numericamente idêntico ao que o `comparar` avaliou. O teste de concordância (passo 6) mede isso.
2. **Converter para GGUF em venv separada.** O `convert_hf_to_gguf.py` vem do repositório do
   `llama.cpp` e fixa as próprias versões de `torch` (CPU), `transformers`, `numpy` e `gguf`, que
   brigam com a venv do lab (torch cu126). Por isso: clonar o `llama.cpp` fora deste repo, numa
   tag fixa, e criar uma venv só para ele (`py -3.12 -m venv`, depois
   `pip install -r requirements\requirements-convert_hf_to_gguf.txt`).
   ```powershell
   python convert_hf_to_gguf.py C:\...\lab-ia\outputs\merged-v1 --outtype f16 --outfile C:\...\lab-ia\outputs\gguf\lora-v1-f16.gguf
   ```
   GGUF é o formato de arquivo único (pesos + tokenizer + metadados) que o llama.cpp e o Ollama leem.
3. **Quantizar com `llama-quantize`** (binário do release Windows do llama.cpp, ou compilado).
   Gerar as duas versões, porque o teste de concordância compara as duas:
   ```powershell
   llama-quantize outputs\gguf\lora-v1-f16.gguf outputs\gguf\lora-v1-q8_0.gguf Q8_0
   llama-quantize outputs\gguf\lora-v1-f16.gguf outputs\gguf\lora-v1-q4_k_m.gguf Q4_K_M
   ```
   Q8_0 = 8 bits, quase sem perda, referência de que a conversão está certa. Q4_K_M = 4 bits
   com blocos de escala ("K-quants"), o formato dos modelos do Ollama; é o que vai para uso.
4. **Modelfile: gerado, nunca escrito à mão.**
   ```powershell
   python -m lab.finetune.qlora --modelfile outputs\gguf\lora-v1-q8_0.gguf   --adapter outputs\lora-v1
   python -m lab.finetune.qlora --modelfile outputs\gguf\lora-v1-q4_k_m.gguf --adapter outputs\lora-v1
   ```
   Grava `lora-v1-q8_0.Modelfile` e `lora-v1-q4_k_m.Modelfile` ao lado dos GGUF, com `FROM`,
   `TEMPLATE` e `stop` derivados do formato do treino e o `eos_token` lido do adapter.
5. **Importar:** `ollama create lora-v1-q8 -f outputs\gguf\lora-v1-q8_0.Modelfile` (idem q4).
   O Ollama copia o GGUF para `~/.ollama/models`: o disco paga duas vezes; apagar o GGUF de
   `outputs\` depois, se quiser, porque ele é regenerável.
6. **Teste de concordância peft × GGUF** antes de usar o modelo do Ollama para qualquer coisa:
   - Mesmo `eval.jsonl` do `comparar`, temperatura 0, `seed` fixa, mesmo limite de tokens
     (`num_predict` = `max_new_tokens` do comparar, 200).
   - Referência: base + adapter via peft (o que o `comparar` gera, `do_sample=False`).
   - Rodar no Ollama, para Q8_0 e Q4_K_M, de **dois jeitos**:
     a. `raw: true` com `prompt = formatar_prompt(ex)` → testa só os pesos (conversão e quantização);
     b. normal com `prompt = prompt_ollama(ex)` → testa também o TEMPLATE.
   - Leitura:
     - (a) ≠ (b) em **qualquer** exemplo = template errado. Com greedy e o mesmo texto de
       entrada, os dois têm de ser idênticos; aqui o critério é 100%, não "quase".
     - Q8_0 (a) muito diferente do peft = conversão ou merge errado (tokenizer, EOS, arquitetura).
     - Q4_K_M pior que Q8_0 na métrica da tarefa = custo da quantização; decidir se aceita.
   - Critério proposto (**estimativa**, calibrar na 1ª rodada): métrica da tarefa no Q8_0 até
     ~2 pontos do peft; Q4_K_M até ~5 pontos. Concordância exata de texto com o peft **não** é
     esperada em 100% (o peft roda sobre base NF4, o GGUF sobre o merge fp16), por isso o
     critério é a métrica, não o texto.
   - Chamada mínima (Ollama em `http://localhost:11434`):
     ```python
     body = {"model": "lora-v1-q8", "prompt": formatar_prompt(ex), "raw": True, "stream": False,
             "options": {"temperature": 0, "seed": 42, "num_predict": 200}}
     # POST /api/generate ; versão (b): "prompt": prompt_ollama(ex), sem "raw"
     ```
   - Registrar a rodada no log (modelo, quantização, n eval, métrica peft / Q8_0 / Q4_K_M,
     concordância a=b).

### A armadilha do template (por que o Modelfile é gerado)
O `qlora.py` treina no formato `### Instrução:\n...\n\n### Resposta:\n`. Um GGUF de Qwen carrega
nos metadados o chat template **ChatML** (`<|im_start|>user ... <|im_end|>`), e o Ollama aplica
o template do modelo quando o Modelfile não traz `TEMPLATE`. Resultado: o adapter recebe um
prompt que nunca viu, responde como o base, e o fine-tuning "não fez nada" no Ollama embora
tenha feito no peft. Nenhum erro aparece.

Decisão: **o Modelfile replica o formato do treino**, gerado pela função
`gerar_modelfile()` a partir das mesmas constantes `CAB_*` que o treino usa. Os testes em
`tests/test_finetune.py` renderizam o `TEMPLATE` do Modelfile e afirmam que sai byte a byte o
prefixo do treino; um deles troca `CAB_RESPOSTA` em tempo de teste e confere que o Modelfile
acompanha (prova que é derivado, não copiado).

Por que não migrar o treino para `apply_chat_template`: troca um acoplamento por outro menos
visível. O template do HF (Jinja, no `tokenizer_config.json`) e o do Ollama (Go template,
inferido dos metadados do GGUF ou escolhido pelo Ollama) são dois textos diferentes mantidos por
projetos diferentes; o Qwen2.5 ainda injeta um system prompt padrão quando não há mensagem de
sistema. Garantir que os dois rendam a mesma string exigiria o mesmo tipo de teste, só que
contra código de terceiros que muda de versão. Além disso mudaria o formato do texto de
treino e o `comparar.py`. Fica para quando o caso for chat multi-turno de verdade.

Consequências do formato próprio, para saber usar:
- O modelo do Ollama vira um "completador de instrução", não um chat: `TEMPLATE` usa só
  `.Prompt` e `.Response`; mensagem de sistema é ignorada e multi-turno não foi treinado.
- Para exemplo com `input`, o prompt enviado ao Ollama é `prompt_ollama(ex)` (instrução +
  `### Entrada:` + input), não só a instrução.
- O `{{ .Response }}` fica no fim do TEMPLATE de propósito: a string não termina em `\n`, então
  nenhum trim do parser do Modelfile pode comer a quebra de linha depois de `### Resposta:`.
- `stop`: `### Instrução:` (se o modelo começar um exemplo novo) e o `eos_token` do tokenizer
  (`<|im_end|>` no Qwen2.5-Instruct). Não verificado ainda se o EOS do GGUF convertido é o
  mesmo; o stop explícito cobre os dois casos.

**Pendência conhecida (fora desta skill):** `comparar.py` monta o prompt com
`_formatar({**ex, "output": ""}).rstrip()`, que tira o `\n` final: o peft é avaliado com um
prompt que termina em `### Resposta:` enquanto o treino (e o TEMPLATE) usam `### Resposta:\n`.
Corrigir trocando por `formatar_prompt(ex)` antes da 1ª avaliação, senão a referência do teste
de concordância já nasce com um caractere de diferença.
