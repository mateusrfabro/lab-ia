import asyncio
import os
import edge_tts

dest_dir = r"C:\Users\mateu\Downloads\Projeto Dudu\PACOTE_CRIATIVOS_2D_DUDU"

casa_livre_text = (
    "Um imóvel parado... não é patrimônio seguro. "
    "É uma torneira aberta... escorrendo pelo ralo todo dia dez. "
    "Condomínio... IPTU... taxa de manutenção... "
    "Enquanto a imobiliária tradicional nem lembra que a sua chave existe, a conta continua chegando no seu nome. "
    "A Casa Livre mudou o jogo. Nós compramos e liquidamos o seu imóvel em até sessenta dias. "
    "Com quinze por cento adiantado à vista e renda garantida durante o processo. "
    "Chega de queimar dinheiro todo mês. "
    "Toque no botão abaixo e faça a simulação do seu imóvel agora."
)

mydollar_text = (
    "Stop letting traditional banks hit your credit report just to deny you. "
    "Every time you apply blind, you lose five points and get another rejection letter in the mail. "
    "What they don't tell you is that select card issuers now use soft-pull pre-qualification. "
    "That means zero score damage and instant matching. "
    "Whether you need guaranteed credit-builder cards or zero percent intro APR, "
    "our free thirty-second quiz finds what you actually qualify for. "
    "Stop guessing with your score. "
    "Tap below and check your approved matches now."
)

async def main():
    # 1. Casa Livre
    casa_comm = edge_tts.Communicate(casa_livre_text, "pt-BR-AntonioNeural", rate="-2%", pitch="-1Hz")
    casa_path = os.path.join(dest_dir, "LOCUCAO_2D_CASA_LIVRE.mp3")
    await casa_comm.save(casa_path)
    print("Saved Casa Livre Audio:", casa_path)

    # 2. MyDollarPilot US
    us_comm = edge_tts.Communicate(mydollar_text, "en-US-ChristopherNeural", rate="+10%", pitch="+0Hz")
    us_path = os.path.join(dest_dir, "LOCUCAO_2D_MYDOLLARPILOT_US.mp3")
    await us_comm.save(us_path)
    print("Saved MyDollarPilot Audio:", us_path)

asyncio.run(main())
