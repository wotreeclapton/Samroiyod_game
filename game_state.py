'''
	SAMROIYOD GAME STATE CLASS developed by Mr Steven J walden
		Nov. 2024
		SAMROIYOD, PRACHUAP KIRI KHAN, THAILAND
	[See License.txt file]
'''

class GameState:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        """Handle events specific to this state."""
        pass

    def update(self):
        """Update logic specific to this state."""
        pass

    def draw(self):
        """Render content specific to this state."""
        pass
