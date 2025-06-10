import json
import os
from datetime import datetime
from typing import List, Dict, Any
from uuid import uuid4

import os
import json
from datetime import datetime
from typing import List, Dict
from poker import Player
from uuid import uuid4


class session_manager:
    def __init__(self, game_id: str, log_dir: str = "data"):
        self.game_id = game_id
        self.log_dir = os.path.join(log_dir, f"session_{game_id}")
        self.ensure_log_dir_exists()

    def ensure_log_dir_exists(self):
        os.makedirs(self.log_dir, exist_ok=True)

    def log_round(self, players: List[Player], winner: Player, pot: int):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.log_dir, f"session_{self.game_id}.txt")
        with open(filename, 'w') as f:
            f.write(f"Game ID: {self.game_id}\n")
            f.write("Players:\n")
            for player in players:
                f.write(f"  {player.get_name()}: Chips = {player.get_stack_amount()}, Hand = {player.get_player_hand()}\n")
            f.write(f"Winner: {winner.get_name()}\n")
            f.write(f"Pot: {pot}\n")

    def log_state(self, state: Dict):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.log_dir, f"session_{self.game_id}_state_{now}.json")
        with open(filename, 'w') as f:
            json.dump({"game_id": self.game_id, "timestamp": now, "state": state}, f, indent=2)

    def log_summary(self, players: List[Player]):
        filename = os.path.join(self.log_dir, f"session_{self.game_id}_summary.txt")
        with open(filename, 'w') as f:
            f.write(f"Game ID: {self.game_id}\n")
            f.write("Final Summary:\n")
            for player in players:
                f.write(f"  {player.get_name()}: Final Chips = {player.get_stack_amount()}\n")
