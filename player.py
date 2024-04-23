class Player:
    def __init__(self):
        self.player_status = 'idl'
        self.player_idx = 0
        self.player_x = 100
        self.player_y = 450
        self.player_speed = 5
        self.forward = True
        self.jump = False
        self.on_ground = True
        self.jump_speed = -16
        self.gravity = 0.8
        self.player_dead = False