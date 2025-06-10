from typing import List
from poker import Player, Deck, Card
from collections import Counter



class InvalidActionError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class GameEngine:
    def __init__(self, players: List[Player], deck: Deck,
                 small_blind: int = 25, big_blind: int = 50):
        self.players = players
        self.deck = deck
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = 0

    def play_round(self) :
        self.pot = 0

        # 1. Blindy
        self.collect_blinds()

        # 2. Rozdanie kart
        self.deck.shuffle()
        self.deck.deal(self.players)

        # 3. Runda zakładów
        current_bet = self.big_blind
        for player in self.players:
            print(player.cards_to_str())
            try:
                action = self.prompt_bet(player, current_bet)
                print(f"{player._Player__name_} wybiera: {action}")
            except (InvalidActionError, InsufficientFundsError) as e:
                print(str(e))

        # 4. Wymiana kart
        for player in self.players:
            print(player.cards_to_str())
            if player._Player__name_ != "BOT":
                try:
                    raw = input(f"{player._Player__name_}, podaj indeksy kart do wymiany (np. 0 2 4): ")
                    indices = list(map(int, raw.strip().split()))
                    new_hand = self.exchange_cards(player.get_player_hand(), indices)
                    player._Player__hand_ = new_hand
                except (ValueError, IndexError):
                    print("Nieprawidłowe indeksy. Pomijam wymianę.")
            else:
                # Przykładowa wymiana losowych kart dla bota
                import random
                indices = random.sample(range(5), k=random.randint(0, 3))
                new_hand = self.exchange_cards(player.get_player_hand(), indices)
                player._Player__hand_ = new_hand

        # 5. Showdown
        """Porównuje układy graczy i wyłania zwycięzcę zgodnie z siłą układu pokerowego."""
        print("\n--- SHOWDOWN ---")
        best_player = None
        best_score = (-1, [])  # krotka (siła, tie-breakery)

        for player in self.players:
            hand = list(player.get_player_hand())
            score = self.evaluate_hand(hand)

            print(f"{player._Player__name_} ma rękę:",
                  " ".join(str(card) for card in hand),
                  f"=> układ: {self.hand_name(score[0])} ({score})")

            if score > best_score:
                best_score = score
                best_player = player

        print(f"\nZwycięzca: {best_player._Player__name_}, otrzymuje {self.pot} żetonów.")
        best_player.update_stack_amount(self.pot)
        return self.get_state()

    def evaluate_hand(self,hand: list[Card]) -> tuple:
        """
        Zwraca krotkę (siła_układu, wartości_pomocnicze), np. (4, [10, 7])
        Gdzie:
          - siła_układu: wyższa = lepszy układ
          - wartości_pomocnicze: do rozstrzygania remisu
        """
        ranks = sorted([card.rank for card in hand], reverse=True)
        suits = [card.suit for card in hand]
        count_ranks = Counter(ranks)
        rank_freq = sorted(count_ranks.items(), key=lambda x: (-x[1], -x[0]))
        counts = [cnt for val, cnt in rank_freq]
        values = [val for val, cnt in rank_freq]

        is_flush = len(set(suits)) == 1
        is_straight = all(ranks[i] - 1 == ranks[i + 1] for i in range(4))


        if is_flush and (is_straight):
            return (8, [max(ranks)])  # poker
        elif counts == [4, 1]:
            return (7, values)  # kareta
        elif counts == [3, 2]:
            return (6, values)  # full house
        elif is_flush:
            return (5, ranks)  # kolor
        elif is_straight :
            return (4,[max(ranks)])  # strit
        elif counts == [3, 1, 1]:
            return (3, values)  # trójka
        elif counts == [2, 2, 1]:
            return (2, values)  # dwie pary
        elif counts == [2, 1, 1, 1]:
            return (1, values)  # para
        else:
            return (0, ranks)  # najwyższa karta
    def collect_blinds(self):
        if len(self.players) < 2:
            print("Za mało graczy do gry.")
            return
        try:
            self.players[0].update_stack_amount( - self.small_blind)
            self.pot += self.small_blind
            self.players[1].update_stack_amount(- self.big_blind)
            self.pot += self.big_blind
        except IndexError:
            print("Nie udało się zebrać blindów.")

    def prompt_bet(self, player: Player, current_bet: int) -> str:
        print(f"{player._Player__name_}, obecna stawka: {current_bet}, twój stack: {player.get_stack_amount()}")
        action = input("Wybierz akcję (check, call, raise, fold): ").lower()

        if action == "fold":
            self.players.remove(player)
            return action
        elif action == "check":
            return action
        elif action == "call":
            if player.get_stack_amount() < current_bet:
                raise InsufficientFundsError("Brak środków na call.")
            player._Player__stack_ -= current_bet
            self.pot += current_bet
            return action
        elif action == "raise":
            raise_amount = int(input("Podaj kwotę podbicia: "))
            if player.get_stack_amount() < raise_amount:
                raise InsufficientFundsError("Brak środków na raise.")
            player._Player__stack_ -= raise_amount
            self.pot += raise_amount
            return action
        else:
            raise InvalidActionError("Nieznana akcja.")

    def exchange_cards(self, hand: List[Card], indices: List[int]) -> List[Card]:
        new_cards = []
        hand = list(hand)
        for idx in indices:
            if idx < 0 or idx > 4:
                raise IndexError("Indeks karty poza zakresem.")
            old = hand[idx]
            new_card = self.deck.cards.pop()
            new_cards.append(new_card)
            hand[idx] = new_card
            self.deck.cards.insert(0, old)  # odkładamy na spód talii
        return hand
    def hand_name(self, hand_strength: int) -> str:
        names = {
            0: "Wysoka karta",
            1: "Para",
            2: "Dwie pary",
            3: "Trójka",
            4: "Strit",
            5: "Kolor",
            6: "Full House",
            7: "Kareta",
            8: "Poker"
        }
        return names.get(hand_strength, "Nieznany układ")
    def showdown(self) -> Player:
        # Na razie losowy wybór zwycięzcy
        import random
        return random.choice(self.players)

    def get_state(self) -> dict:
        return {
            "players": [
                {
                    "name": player._Player__name_,
                    "stack": player.get_stack_amount(),
                    "hand": [(card.rank, card.suit) for card in player.get_player_hand()]
                }
                for player in self.players
            ],
            "deck": [(card.rank, card.suit) for card in self.deck.cards],
            "pot": self.pot
        }

    def set_state(self, state: dict):
        # Przywrócenie graczy
        self.players = []
        for player_data in state["players"]:
            player = Player(player_data["name"], player_data["stack"])
            hand_cards = [Card(rank, suit) for rank, suit in player_data["hand"]]
            player._Player__hand_ = hand_cards
            self.players.append(player)

        # Przywrócenie talii
        self.deck.cards = [Card(rank, suit) for rank, suit in state["deck"]]

        # Przywrócenie puli
        self.pot = state["pot"]
players=[Player(100,"p1"),Player(100,"p2")]
d=Deck()
a=GameEngine(players,d)
a.play_round()
print(players[0].cards_to_str())