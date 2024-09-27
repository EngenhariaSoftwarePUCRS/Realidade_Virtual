# Realidade Virtual - Trabalho I

**Professor:** Márcio Sarroglia Pinho  
**Aluno:** Felipe Freitas Silva  
**Data de entrega e apresentação:** 27/09/2024

## Descrição

Este projeto constrói um ambiente virtual onde dois objetos 3D (cubos) são manipulados pela mão do usuário. O movimento da mão é capturado usando a câmera do computador, e o cenário é renderizado em **OpenGL** com **Pygame**.

O usuário pode:
- Pegar um objeto fechando a mão.
- Manipular (transladar) o objeto com a mão fechada.
- Rotacionar o objeto ao fazer o gesto de "pinça" (aproximando o polegar e o indicador).

## Ferramentas

- **MediaPipe** para rastreamento de mãos.
- **OpenCV** para captura de vídeo.
- **OpenGL** com **Pygame** para renderização dos objetos 3D.
- **Conda** para gerenciamento do ambiente virtual.

## Requisitos

1. **Conda**: Certifique-se de que o **conda** está instalado.
2. Verifique se a câmera está funcionando corretamente e está acessível.

## Como Executar

1. Clone ou baixe este repositório.
```bash
git clone git@github.com:EngenhariaSoftwarePUCRS/Realidade_Virtual.git
```
2. Navegue até a pasta do projeto.
```bash
cd Realidade_Virtual/T1
```
3. Instale as dependências usando o Conda como mencionado.
```bash
conda create -n virtual_env python=3.10.14
conda activate virtual_env
conda install numpy==1.23.5
pip install -r requirements.txt
```
4. Execute o script `main.py`.
```bash
python main.py
```
5. A aplicação abrirá o feed da webcam e renderizará os objetos 3D na tela. Use os gestos das mãos para interagir com os cubos.
6. Divirta-se!

## Gestos de Controle

- **Pegar o Cubo**: Feche a mão próximo ao cubo para pegá-lo.
  - Ao fechar a mão, o "cursor" da mão ficará vermelho, indicando que foi identificada a interação.
  - Ainda, aparecerá uma mensagem no terminal indicando que o cubo foi "agarrado".
- **Mover o Cubo**: Mova a mão fechada para transladar o cubo.
  - O cubo se moverá em relação ao pulso.
- **Rotacionar o Cubo**: Faça o gesto de "pinça" (polegar e indicador juntos) para rotacionar o cubo.
  - Ao fazer o gesto, o "cursor" da mão ficará verde, indicando que foi identificada a interação.
  - Aqui também aparecerá uma mensagem no terminal indicando que o cubo foi "pego".
  - Ainda, o cubo rotacionará em relação a direção do dedo médio e o centro da palma da mão.
    - Ou seja, a rotação será feita em torno do eixo que passa pelo dedo médio e o centro da palma.
    - PS: Existem algumas limitações na rotação, devido a dificuldade de identificar a direção do dedo médio.

## Encerramento

- Pressione a tecla `q` para encerrar o programa.
- Ou pressione `Ctrl + C` no terminal para finalizar a execução.

## Notas

- O cenário é renderizado em 3D, e os objetos são manipulados em tempo real.
- O código foi testado em ambiente Windows 10 com Python 3.10.14.
- O observador do cenário é fixo, e a variação de perspectiva é feita pela movimentação dos objetos.
  - Ou seja, a câmera não se move, apenas os objetos são transladados e rotacionados.
  - Quanto mais próximo a mão estiver da câmera, maior será o objeto na tela.
  - Ao se afastar da câmera, eventualmente o programa sempre identificará a mão como fechada.
- Houveram dificuldades na captação de profundidade, na própria biblioteca MediaPipe.
  - Por isso, os objetos e o cursor parecem se mover pouco neste eixo (para "dentro" e "fora" da tela).
