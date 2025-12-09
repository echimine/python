import sys
import random
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QMessageBox,
)


class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(600, 600)

        # Joueur
        self.player_radius = 15
        self.player_pos = QPointF(100, 100)
        self.player_color = QColor("white")

        # Cible
        self.target_radius = 20
        self.target_pos = QPointF(450, 450)

        # Mouvement
        self.speed = 200.0  # pixels par seconde
        self.vx = 0.0
        self.vy = 0.0
        self.moving = False
        self.step_duration_ms = 1000  # 1 seconde par défaut
        self.elapsed_ms = 0

        # Timer de mise à jour
        self.dt_ms = 16  # ~60 FPS
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(self.dt_ms)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    # --- Interface avec la fenêtre principale ---

    def set_step_duration(self, seconds: float):
        """Changer la durée d'un déplacement (1 ou 2 secondes)."""
        self.step_duration_ms = float(seconds * 1000)

    # --- Gestion clavier ---

    def keyPressEvent(self, event):
        if self.moving:
            # On ignore les touches tant qu'un déplacement est en cours
            return

        key = event.key()
        # On veut ZQSD ou flèches
        if key == Qt.Key_Z or key == Qt.Key_Up:
            self.vx, self.vy = 0, -self.speed
        elif key == Qt.Key_S or key == Qt.Key_Down:
            self.vx, self.vy = 0, self.speed
        elif key == Qt.Key_Q or key == Qt.Key_Left:
            self.vx, self.vy = -self.speed, 0
        elif key == Qt.Key_D or key == Qt.Key_Right:
            self.vx, self.vy = self.speed, 0
        else:
            super().keyPressEvent(event)
            return

        # Lancer le déplacement
        self.moving = True
        self.elapsed_ms = 0

    # --- Logique du jeu ---

    def update_game(self):
        if self.moving:
            dt_s = self.dt_ms / 1000.0
            self.elapsed_ms += self.dt_ms

            # Met à jour la position
            new_x = self.player_pos.x() + self.vx * dt_s
            new_y = self.player_pos.y() + self.vy * dt_s

            # Gérer les bords de la fenêtre
            new_x = max(self.player_radius, min(self.width() - self.player_radius, new_x))
            new_y = max(self.player_radius, min(self.height() - self.player_radius, new_y))

            self.player_pos = QPointF(new_x, new_y)

            # Fin de l'impulsion
            if self.elapsed_ms >= self.step_duration_ms:
                self.moving = False
                self.vx = 0.0
                self.vy = 0.0
                self.elapsed_ms = 0

        # Met à jour la couleur en fonction de la zone
        self.update_player_color()

        # Vérifie si la cible est atteinte
        self.check_target()

        # Redessine
        self.update()

    def update_player_color(self):
        w = self.width()
        h = self.height()
        x = self.player_pos.x()
        y = self.player_pos.y()

        # 4 zones : on coupe en 2 verticalement et horizontalement
        left = x < w / 2
        top = y < h / 2

        if top and left:
            self.player_color = QColor("#ff5555")  # rouge
        elif top and not left:
            self.player_color = QColor("#55ff55")  # vert
        elif not top and left:
            self.player_color = QColor("#5555ff")  # bleu
        else:
            self.player_color = QColor("#ffaa00")  # orange

    def check_target(self):
        dx = self.player_pos.x() - self.target_pos.x()
        dy = self.player_pos.y() - self.target_pos.y()
        dist_sq = dx * dx + dy * dy
        radius_sum = self.player_radius + self.target_radius

        if dist_sq <= radius_sum * radius_sum:
            # Cible atteinte
            QMessageBox.information(self, "Bravo", "Cible atteinte !")
            self.spawn_new_target()

    def spawn_new_target(self):
        margin = 50
        x = random.randint(margin, self.width() - margin)
        y = random.randint(margin, self.height() - margin)
        self.target_pos = QPointF(x, y)

    # --- Dessin ---

    def paintEvent(self, event):
        painter = QPainter(self)

        # Dessiner les zones
        w = self.width()
        h = self.height()

        # Zone haut-gauche
        painter.setBrush(QBrush(QColor(40, 40, 40)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, w // 2, h // 2)

        # Zone haut-droite
        painter.setBrush(QBrush(QColor(60, 60, 60)))
        painter.drawRect(w // 2, 0, w // 2, h // 2)

        # Zone bas-gauche
        painter.setBrush(QBrush(QColor(80, 80, 80)))
        painter.drawRect(0, h // 2, w // 2, h // 2)

        # Zone bas-droite
        painter.setBrush(QBrush(QColor(100, 100, 100)))
        painter.drawRect(w // 2, h // 2, w // 2, h // 2)

        # Dessiner la cible
        painter.setBrush(QBrush(QColor("#ffff00")))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(
            self.target_pos,
            self.target_radius,
            self.target_radius,
        )

        # Dessiner le joueur
        painter.setBrush(QBrush(self.player_color))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(
            self.player_pos,
            self.player_radius,
            self.player_radius,
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Petit jeu 2D - PyQt5")
        self.game_widget = GameWidget(self)

        # Choix de la durée (1 ou 2 secondes)
        control_bar = QHBoxLayout()
        label = QLabel("Durée du déplacement :")
        self.duration_combo = QComboBox()
        self.duration_combo.addItem("0.25 seconde", 0.25)
        self.duration_combo.addItem("0.5 seconde", 0.5)
        self.duration_combo.addItem("1 seconde", 1)
        self.duration_combo.addItem("2 secondes", 2)
        self.duration_combo.currentIndexChanged.connect(self.on_duration_changed)

        control_bar.addWidget(label)
        control_bar.addWidget(self.duration_combo)
        control_bar.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(control_bar)
        main_layout.addWidget(self.game_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.resize(600, 650)

    def on_duration_changed(self, index):
        seconds = self.duration_combo.currentData()
        self.game_widget.set_step_duration(seconds)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()