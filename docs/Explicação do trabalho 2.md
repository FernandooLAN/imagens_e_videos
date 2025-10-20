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

## Acurácia