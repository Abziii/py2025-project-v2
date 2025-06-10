from uuid import uuid4
from time import sleep
from poker import *
from gameEngine import *
from src.fileops.session_manager import  session_manager
# 1. Utwórz grę i logger
game_id = str(uuid4())[:8]
logger = session_manager(game_id)

# 2. Stwórz GameEngine z dwoma graczami
players = [
    Player(1000,"Alice" , ["AH", "KH"]),
    Player(500,"Bob" , ["8C", "8D"])
]
engine = GameEngine(players,Deck())

# 3. Rozegraj 1. rundę
result1 = engine.play_round()
logger.log_round(result1["players"], result1["winner"], result1["pot"])

# 4. Zapisz stan gry po rundzie 1
state1 = engine.get_state()
logger.log_state(state1)

# 5. Symuluj zakończenie i nową instancję silnika
sleep(1)  # Żeby timestampy się różniły
engine2 = GameEngine([])  # Pusta instancja
engine2.set_state(state1)  # Wczytujemy stan gry

# 6. Rozegraj 2. rundę na bazie poprzedniego stanu
result2 = engine2.play_round()
logger.log_round(result2["players"], result2["winner"], result2["pot"])

# 7. Logowanie końcowe
logger.log_summary(result2["players"])