# Drawing Turtle

Projeto que transforma uma imagem em um desenho feito pela tartaruga do ROS2 (turtlesim).

O pipeline processa a imagem usando só numpy para extrair o contorno e exporta as coordenadas para um nó ROS2 que comanda a tartaruga ponto a ponto.

A explicação detalhada de cada etapa está no `principal.ipynb`.

## Vídeo

[Link do vídeo explicativo](https://youtu.be/Nskzss0gGVQ)

## Como executar

**1. Processar a imagem**

Execute todas as células do `principal.ipynb`. Isso gera `pontos.npy` e `img_shape.npy`.

**2. Iniciar o turtlesim**

```bash
ros2 run turtlesim turtlesim_node
```

**3. Rodar o nó de desenho**

```bash
colcon build --packages-select drawing_turtle && source install/setup.bash
ros2 run drawing_turtle caneta
```
