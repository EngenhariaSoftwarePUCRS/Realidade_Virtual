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
2. Crie e ative um ambiente usando o arquivo `requirements.txt` com os pacotes necessários:
```bash
conda create --name virtual_env --file requirements.txt
conda activate virtual_env
```
3. Verifique se a câmera está funcionando corretamente.

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
conda create --name virtual_env --file requirements.txt
conda activate virtual_env
```
4. Execute o script `main.py`.
```bash
python main.py
```
5. A aplicação abrirá o feed da webcam e renderizará os objetos 3D na tela. Use os gestos das mãos para interagir com os cubos.
6. Divirta-se!

## Gestos de Controle

- **Pegar o Cubo**: Feche a mão próximo ao cubo para pegá-lo.
- **Mover o Cubo**: Mova a mão fechada para transladar o cubo.
- **Rotacionar o Cubo**: Faça o gesto de "pinça" (polegar e indicador juntos) para rotacionar o cubo.

## Encerramento

- Pressione a tecla `q` para encerrar o programa.
- Ou pressione `Ctrl + C` no terminal para finalizar a execução.

## Notas

- Este projeto utiliza **OpenGL** com **Pygame** para renderização e **MediaPipe** para rastreamento de mãos.
- Certifique-se de que a câmera está funcionando corretamente e acessível pelo OpenCV.

