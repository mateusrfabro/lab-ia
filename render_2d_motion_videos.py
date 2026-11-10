import os
import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
base_dir = r"C:\Users\mateu\Downloads\Projeto Dudu\PACOTE_CRIATIVOS_2D_DUDU"

# ==========================================
# 1. RENDER CASA LIVRE 2D MOTION EXPLAINER
# ==========================================
img1_casa = os.path.join(base_dir, "CASA_LIVRE_2D_CENA1_IMOVEL.jpg")
img2_casa = os.path.join(base_dir, "CASA_LIVRE_2D_CENA2_SELO60DIAS.jpg")
audio_casa = os.path.join(base_dir, "LOCUCAO_2D_CASA_LIVRE.mp3")
out_casa = os.path.join(base_dir, "VIDEO_2D_CASA_LIVRE_PROPRIETARIO.mp4")

# Total audio duration ~ 29 seconds. Scene 1 = 15.0s, Scene 2 = 15.0s, xfade at 14.5s for 0.5s
filter_casa = (
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
    "zoompan=z='min(zoom+0.0006,1.20)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=450:s=1080x1920:fps=30,"
    "drawbox=y=0:color=black@0.65:width=iw:height=230:t=fill,"
    "drawtext=text='IMÓVEL PARADO?':fontcolor=yellow:fontsize=52:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.7:boxborderw=8,"
    "drawtext=text='Uma torneira aberta drenando sua renda':fontcolor=white:fontsize=34:x=(w-text_w)/2:y=130[v0];"
    
    "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
    "zoompan=z='min(zoom+0.0007,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=450:s=1080x1920:fps=30,"
    "drawbox=y=0:color=black@0.70:width=iw:height=230:t=fill,"
    "drawtext=text='LIQUIDAÇÃO EM ATÉ 60 DIAS':fontcolor=green:fontsize=48:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.7:boxborderw=8,"
    "drawtext=text='15% Adiantado à Vista + Renda Garantida':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=130,"
    "drawbox=y=ih-240:color=black@0.75:width=iw:height=240:t=fill,"
    "drawtext=text='CASA LIVRE':fontcolor=green:fontsize=54:x=(w-text_w)/2:y=h-190:box=1:boxcolor=black@0.8:boxborderw=10,"
    "drawtext=text='Toque em Saiba Mais e Simule Grátis':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=h-100[v1];"
    
    "[v0][v1]xfade=transition=fade:duration=0.5:offset=14.5[v]"
)

cmd_casa = [
    ffmpeg_exe, "-y",
    "-loop", "1", "-t", "15.0", "-i", img1_casa,
    "-loop", "1", "-t", "15.0", "-i", img2_casa,
    "-i", audio_casa,
    "-filter_complex", filter_casa,
    "-map", "[v]", "-map", "2:a",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-b:v", "3500k",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    out_casa
]

print("Rendering Casa Livre 2D Motion Video...")
res_c = subprocess.run(cmd_casa, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res_c.returncode == 0:
    print("SUCCESS Casa Livre:", out_casa)
else:
    print("ERROR Casa Livre:", res_c.stderr[-400:])

# ==========================================
# 2. RENDER MYDOLLARPILOT US 2D MOTION EXPLAINER
# ==========================================
img1_us = os.path.join(base_dir, "MYDOLLARPILOT_2D_CENA1_DECLINED.jpg")
img2_us = os.path.join(base_dir, "MYDOLLARPILOT_2D_CENA2_PREQUALIFIED.jpg")
audio_us = os.path.join(base_dir, "LOCUCAO_2D_MYDOLLARPILOT_US.mp3")
out_us = os.path.join(base_dir, "VIDEO_2D_MYDOLLARPILOT_US.mp4")

# Total audio duration ~ 23.5 seconds. Scene 1 = 12.0s, Scene 2 = 12.0s, xfade at 11.5s for 0.5s
filter_us = (
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
    "zoompan=z='min(zoom+0.0006,1.20)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=360:s=1080x1920:fps=30,"
    "drawbox=y=0:color=black@0.70:width=iw:height=240:t=fill,"
    "drawtext=text='STOP APPLYING BLIND!':fontcolor=red:fontsize=52:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.7:boxborderw=8,"
    "drawtext=text='Hard Inquiries Drop 5-10 Points Off FICO':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=130[v0];"
    
    "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
    "zoompan=z='min(zoom+0.0007,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=360:s=1080x1920:fps=30,"
    "drawbox=y=0:color=black@0.70:width=iw:height=240:t=fill,"
    "drawtext=text='SOFT-PULL PRE-QUALIFICATION':fontcolor=green:fontsize=46:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.7:boxborderw=8,"
    "drawtext=text='Guaranteed Credit-Builder & 0% Intro APR':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=130,"
    "drawbox=y=ih-250:color=black@0.75:width=iw:height=250:t=fill,"
    "drawtext=text='CHECK APPROVED CARDS':fontcolor=green:fontsize=50:x=(w-text_w)/2:y=h-195:box=1:boxcolor=black@0.8:boxborderw=10,"
    "drawtext=text='Free 30-Sec Quiz • Zero Score Damage':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=h-105[v1];"
    
    "[v0][v1]xfade=transition=fade:duration=0.5:offset=11.5[v]"
)

cmd_us = [
    ffmpeg_exe, "-y",
    "-loop", "1", "-t", "12.0", "-i", img1_us,
    "-loop", "1", "-t", "12.0", "-i", img2_us,
    "-i", audio_us,
    "-filter_complex", filter_us,
    "-map", "[v]", "-map", "2:a",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-b:v", "3500k",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    out_us
]

print("Rendering MyDollarPilot 2D Motion Video...")
res_u = subprocess.run(cmd_us, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res_u.returncode == 0:
    print("SUCCESS MyDollarPilot:", out_us)
else:
    print("ERROR MyDollarPilot:", res_u.stderr[-400:])
