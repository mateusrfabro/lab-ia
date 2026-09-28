---
name: qlora-6gb
description: Use antes de qualquer fine-tuning de LLM neste laboratório — decide se treinar é a resposta, escolhe modelo que cabe em 6 GB de VRAM, define a receita QLoRA (NF4 + LoRA + gradient checkpointing), o formato do dataset e a avaliação antes/depois obrigatória.
---

# QLoRA em 6 GB (RTX 4050 Laptop)

## Antes de treinar: a pergunta que evita 90% dos treinos inúteis
Fine-tuning ensina **forma** (formato de saída, estilo, vocabulário do domínio, seguir um
esquema). Não ensina **fatos** de forma confiável (fato muda; RAG ou contexto no prompt fazem
melhor). Então:
1. Escrever 10 exemplos do que se quer.
2. Testar few-shot no modelo base via Ollama (`qwen3:8b` com 3-5 exemplos no prompt).
3. Se acertar ≥ 80%, **não treinar**. Registrar no log e usar o prompt.
4. Se não, montar dataset e treinar. A prova do passo 2 vai na linha do log.

## O que cabe na 4050

| Modelo | VRAM QLoRA seq 1024 | Época com 500 ex | Veredito |
|---|---|---|---|
| Qwen2.5-1.5B-Instruct | ~3 GB | ~10-15 min | começar aqui |
| Qwen2.5-3B-Instruct / Llama-3.2-3B | ~5 GB | ~25-40 min | limite confortável |
| 7-8B (Mistral, Llama 3.1, Qwen3) | > 6 GB | horas ou OOM | não aqui |

Estimativas; medir com `torch.cuda.max_memory_allocated()` (o script imprime). Se der OOM:
`--max-len 512` → `--r 8` → modelo menor, nessa ordem.

## As peças (uma frase cada, pra explicar na entrega)
- **Quantização NF4 (bitsandbytes)**: pesos do modelo base guardados em 4 bits; corta a
  memória em ~4× com perda pequena de qualidade. `bnb_4bit_use_double_quant` economiza mais
  um pouco.
- **LoRA (rank r)**: congela o modelo e treina, em cada camada de atenção/MLP, duas matrizes
  pequenas cujo produto é a "correção". r=16 é o padrão; r=8 se faltar VRAM; r=32 se o
  dataset for grande e a tarefa difícil. `lora_alpha = 2r` é convenção segura.
- **QLoRA** = base em NF4 + LoRA em fp16. O adapter final tem dezenas de MB e se aplica sobre
  o base original.
- **Gradient checkpointing**: não guarda as ativações do forward; recomputa no backward.
  ~30% mais lento, ~50% menos VRAM. Obrigatório aqui.
- **`paged_adamw_8bit`**: otimizador com estado em 8 bits e paginado para a RAM quando aperta.
- **lr 2e-4 cosine com warmup 3%**: padrão do paper do QLoRA; funciona para quase tudo.

## Dataset
- JSONL, uma linha por exemplo: `{"instruction": ..., "input": ... (opcional), "output": ...}`.
- 200-500 exemplos **revisados**. Volume não compensa exemplo errado.
- Separar 10% (mínimo 30) para avaliação **antes** de treinar. Nunca avaliar no treino.
- Sem dado pessoal (nome, e-mail, telefone, documento). Regra 4 do CLAUDE.md.
- Para chat de verdade (multi-turno), usar `tokenizer.apply_chat_template` em vez do formato
  `### Instrução` do script; o script é o mínimo didático.

## Comandos
```powershell
.\setup.ps1 -Llm                                  # uma vez (~3 GB)
python -m lab.finetune.qlora --data data\processed\treino.jsonl --dry-run
python -m lab.finetune.qlora --data data\processed\treino.jsonl --out outputs\lora-v1
python -m lab.finetune.comparar --adapter outputs\lora-v1 --eval data\processed\eval.jsonl
```

## Ler o treino
- Loss caindo suave até ~0,5-1,0 e estabilizando: saudável.
- Loss ~0 na 1ª época: decorou. Menos épocas, mais dados, ou dropout maior.
- Loss parada: lr, formato do prompt (não bate com o template do modelo) ou dado ruim.
- Antes/depois idêntico: o adapter não pegou; conferir se `target_modules` bate com a
  arquitetura (`model.print_trainable_parameters()` deve mostrar > 0,3%).

## Usar o adapter no Ollama depois
Possível: mesclar adapter no base (`model.merge_and_unload()`), exportar para GGUF com
`llama.cpp` (`convert_hf_to_gguf.py`), quantizar, criar Modelfile. É um passo separado; só
fazer depois que o antes/depois provar ganho.
