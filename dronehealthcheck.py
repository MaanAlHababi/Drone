def checkHealth(self):
    if self.healthbar.value == 0:
        # print("GAME OVER")
        self.game_ongoing = False
        self.losingmenu_widget.opacity = 1