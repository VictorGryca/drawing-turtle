import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen
import numpy as np

TURTLE_SIZE = 11.08
SHIFT_X = 2.0  # ajusta para mover o desenho para a direita

class Caneta(Node):
    def __init__(self):
        super().__init__('caneta')

        self.client = self.create_client(TeleportAbsolute, 'turtle1/teleport_absolute')
        self.client_pen = self.create_client(SetPen, 'turtle1/set_pen')
        self.client.wait_for_service()
        self.client_pen.wait_for_service()

        pontos = np.load('pontos.npy')
        img_h, img_w = np.load('img_shape.npy')
        self.coords = self._para_turtle(pontos, img_h, img_w)
        self.idx = 0

        self._caneta(off=True)          # desliga antes do timer existir
        self.timer = self.create_timer(0.01, self.passo)

    def _caneta(self, off):
        req = SetPen.Request()
        req.off = 1 if off else 0
        self.client_pen.call_async(req)

    def _teleport(self, x, y):
        req = TeleportAbsolute.Request()
        req.x = float(x)
        req.y = float(y)
        req.theta = 0.0
        self.client.call_async(req)

    def _para_turtle(self, pontos, img_h, img_w):
        escala = TURTLE_SIZE / img_h
        offset_x = (TURTLE_SIZE/2 - img_w/2 * escala)
        offset_y = (TURTLE_SIZE - img_h * escala) / 2

        x = pontos[:, 1] * escala + offset_x + SHIFT_X
        y = TURTLE_SIZE - (pontos[:, 0] * escala + offset_y)
        return list(zip(x.tolist(), y.tolist()))

    def passo(self):
        if self.idx == 0:
            self._teleport(*self.coords[0])
        elif self.idx == 1:
            self._caneta(off=False)
        else:
            i = self.idx - 2
            if i >= len(self.coords):
                self.timer.cancel()
                self.get_logger().info('Desenho concluido')
                return
            self._teleport(*self.coords[i])

        self.idx += 1


def main(args=None):
    rclpy.init(args=args)
    node = Caneta()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
