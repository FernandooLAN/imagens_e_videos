Alunos:
- André Yudji Silva Okimoto
- Guilherme Dias Correa
- Fernando Lucas Almeida Nascimento

## 1.  Pré-processamento 

As imagens antes de serem passadas para os descritores são quantizadas e particionadas.
Utilizamos uma **quantização com 64** cores e um particionamento em dois. A separação cria uma partição com o retângulo central da imagem e uma com o resto da imagem, que seria basicamente a borda. 

## 2. Descritores

Como solicitado no trabalho, usamos o histograma local e o BIC. 
- Histograma local: Gera um histograma com 64 bins para cada partição, totalizando um vetor de características final de tamanho 128 
- BIC: Gera 2 histogramas (borda e interior) de 64 bins para cada partição, totalizando um vetor de características final de tamanho 256

## (Detecção de cena, caso queira falar)

O `scene_detctor.py` analisa um frame a cada segundo de vídeo. Comparando um histograma artificial (vetores de  128 e 256 posições com valor 0)  na primeira iteração e guardando o valor dos histograma atual para a próxima iteração. Se a comparação dos histogramas com o dLog for maior que o valor de threshold passado então o frame é interpretado como uma nova cena e salvo.
## Acurácia

A função calcula baseado nos frames detectados e nos frames de referencia. Recebe ambas as listas de numero de frames e opcionalmente o frame rate do video, importante para calcular o espaço temporal de um segundo a mais ou a menos ao redor de um frame detectado. 
Cada frame que seja identificado como dentro da faixa de tolerância ao redor da referencia é contado como um verdadeiro positivo. A acurácia no final é a quantidade de verdadeiros positivos dividido pela quantidade de frames de referencia.