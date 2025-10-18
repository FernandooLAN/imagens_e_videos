import cv2
import sys

nome_do_video = sys.argv[1]
registro = sys.argv[2]

video = cv2.VideoCapture(nome_do_video)

if not video.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

numero_do_frame = 0  
frames_registrados = []  
salto = int(sys.argv[3])  

while True:
    video.set(cv2.CAP_PROP_POS_FRAMES, numero_do_frame)

    ret, frame = video.read()

    if not ret:
        break

    cv2.imshow("Quadro", frame)

    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        pass
    elif key == ord('r'):
        frames_registrados.append(numero_do_frame)
    elif key == ord('e'):
        break

    numero_do_frame += salto

with open(registro, "w") as arquivo:
    conteudo = ",".join(map(str, frames_registrados))
    arquivo.write(conteudo)

video.release()
cv2.destroyAllWindows()