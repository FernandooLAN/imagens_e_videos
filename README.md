# imagens_e_videos

Drive com os vídeos já baixados: https://drive.google.com/drive/folders/1PwNbgRQ2Jv7ZdjegVozcmlFZLUxugH7J?usp=sharing

alguns links

Game of Thrones - Batalha dos Bastardos: https://www.youtube.com/watch?v=zrfBcB_2itU

Persona 3 Reload - Opening Movie: https://www.youtube.com/watch?v=_Ii358BBjkU

Hunter X Hunter - Uvogin Requiem: https://www.youtube.com/watch?v=MrWiIeCtf5U

Reporter da Record confunde Forza 6 com teste para motorista de Trump - https://www.youtube.com/watch?v=3S68nlL3y98

Trailer revelação de Pokemon X Y - https://www.youtube.com/watch?v=IfclgYT7h-A

Primeiro trailer do Minecraft - https://www.youtube.com/watch?v=MmB9b5njVbA 

6 Mind Blowing New Nature Documentaries | Only on Netflix - https://youtu.be/DBqcdkgnT1E?si=V-xKvk37ciqLAg_8

The Legend of Korra ~ Official Trailer 720p HD (Corrected Speed) - https://youtu.be/54srZLuYfb0?si=s3hpjWIG_hLU7ssN
 
I Want It That Way | Brooklyn Nine-Nine - https://youtu.be/HlBYdiXdUa8?si=1zlHwhi7FsXWULoE

LEVI vs. TITÃ BESTIAL (DUBLADO) - https://www.youtube.com/watch?v=hpMZhZ23j0c

---

`docs` -> Diretório contendo PDFs do nosso trabalho, incluindo explicação do workflow e decisões tomadas, além de PDFs mostrando os resultados nos vídeos selecionados.

`manual` -> Diretório de arquivos txt que possuem os frames de referências feitos manualmente para os vídeos.

`src` -> Diretório contendo todos os códigos python do trabalho

---

## Como testar?

1. Crie um diretório `quadros` e três diretórios dentro dele, `ref`, `histLoc` e `bic`
```bash
mkdir -p quadros/{ref,histLoc,bic}
```

2. Entre no diretório `src`
```bash
cd src
```

3. Rode o arquivo `scene_detector.py` (é preciso das bibliotecas `cv2` e `numpy`) no seguinte formato
```
python3 scene_detector.py <path do vídeo> <path do arquivo de frames manual> <valor do threshold>
```

--- 

## PDFs importantes