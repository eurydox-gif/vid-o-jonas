"""Génère la voix off (Piper TTS, voix française) et l'assemble sur jonas.mp4.

Usage : python3 narration.py CHEMIN/fr_FR-siwis-medium.onnx [entree.mp4] [sortie.mp4]
Chaque phrase est placée au début de sa scène (scènes de 8 s).
"""
import subprocess, sys, wave
from pathlib import Path
from piper import PiperVoice, SynthesisConfig

SCENE = 8.0
# (début dans la scène en s, texte)
NARRATION = [
    (1.0, "Jonas : obéir, même quand c'est difficile."),
    (0.6, "Un jour, Dieu parla à Jonas. Il lui dit : « Va à Ninive ! »"),
    (0.6, "Mais Jonas eut peur. Il désobéit, et s'enfuit en bateau, dans l'autre sens."),
    (0.5, "Soudain, une grande tempête arrive ! Le bateau est secoué par les vagues."),
    (0.4, "Jonas tombe dans la mer… et un énorme poisson l'avale !"),
    (0.8, "Dans le ventre du poisson, Jonas prie, et demande pardon à Dieu."),
    (0.6, "Le poisson dépose Jonas sur la plage. Cette fois, Jonas obéit !"),
    (0.6, "Jésus a dit : « Si vous m'aimez, gardez mes commandements. » Jean, quatorze, quinze."),
]

def main():
    model = sys.argv[1]
    src = sys.argv[2] if len(sys.argv) > 2 else "jonas.mp4"
    out = sys.argv[3] if len(sys.argv) > 3 else "jonas_voix.mp4"
    voice = PiperVoice.load(model)
    cfg = SynthesisConfig(length_scale=1.18, noise_scale=0.6, noise_w_scale=0.7)
    d = Path("voix"); d.mkdir(exist_ok=True)
    inputs, filters = [], []
    for i, (start, text) in enumerate(NARRATION):
        f = d / f"scene{i + 1}.wav"
        with wave.open(str(f), "wb") as w:
            voice.synthesize_wav(text, w, syn_config=cfg)
        with wave.open(str(f)) as w:
            dur = w.getnframes() / w.getframerate()
        t0 = i * SCENE + start
        free = SCENE - start - 0.4
        print(f"scène {i + 1}: {dur:.2f} s (place {free:.2f} s)" + ("  ⚠ trop long" if dur > free else ""))
        inputs += ["-i", str(f)]
        filters.append(f"[{i + 1}:a]adelay={int(t0 * 1000)}:all=1,apad[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(NARRATION)))
    filters.append(f"{mix}amix=inputs={len(NARRATION)}:normalize=0,atrim=0:{SCENE * len(NARRATION)},"
                   "highpass=f=70,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-16:TP=-1.5[aout]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, *inputs,
                    "-filter_complex", ";".join(filters), "-map", "0:v", "-map", "[aout]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest",
                    "-movflags", "+faststart", out], check=True)
    print("Vidéo avec voix off :", out)

if __name__ == "__main__":
    main()
