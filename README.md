# vid-o-jonas

Petite vidéo animée (64 s, 8 scènes × 8 s, 1920×1080) : **« Jonas : obéir même quand c'est difficile »**.

| # | Scène | Texte |
|---|-------|-------|
| 1 | Ciel bleu, soleil | Jonas : obéir même quand c'est difficile |
| 2 | Jonas entend Dieu (rayons de lumière) | Dieu dit : « Va à Ninive ! » |
| 3 | Jonas a peur, part en bateau dans l'autre sens | Jonas désobéit et s'enfuit. |
| 4 | Tempête, vagues, bateau qui se balance | Une grande tempête arrive ! |
| 5 | Jonas tombe à la mer, un gros poisson l'avale | Un énorme poisson avale Jonas. |
| 6 | Dans le ventre du poisson, mains jointes | Jonas prie et demande pardon. |
| 7 | Le poisson le dépose sur la plage, il marche vers la ville | Cette fois, Jonas obéit. |
| 8 | La ville en fête, des cœurs | « Si vous m'aimez, gardez mes commandements. » Jean 14.15 |

## Fichiers

- `jonas.mp4` — la vidéo finale (H.264, 30 i/s, sans son).
- `jonas.html` — l'animation (canvas), jouable directement dans un navigateur ; chaque image est une fonction du temps `renderFrame(t)`.
- `render.js` — régénère la vidéo à partir de `jonas.html` (Playwright + ffmpeg).

## Régénérer la vidéo

```bash
node render.js jonas.mp4 30
```

Images de contrôle (4 par scène) : `node render.js --stills dossier`.
