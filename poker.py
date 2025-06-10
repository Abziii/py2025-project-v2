import random


class Card:
    # słownik symboli unicode
    unicode_dict = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}

    def __init__(self, rank, suit):

        self.rank=rank
        self.suit=suit
        pass

    def get_value(self):

        return (self.rank,self.suit)


    def __str__(self):

        rank_dict={1:'A',11:'J',12:'Q',13:'K'}

        if self.rank in rank_dict:
            s="{rank} {suit}".format(rank=rank_dict[self.rank], suit=self.unicode_dict[self.suit])
        else:
            s="{rank} {suit}".format(rank=self.rank, suit=self.unicode_dict[self.suit])
        return s



class Deck():

    def __init__(self, *args):

        self.cards=list()
        for j in Card.unicode_dict:
            for i in range(1,14):
                self.cards.append(Card(i,j))




    def __str__(self):
        s=""
        for i in self.cards:
            s+="{karta}\n".format(karta=i)
        return s

    def shuffle(self):

        random.shuffle(self.cards)



    def deal(self, players):
        for i in players:
            i.reset_hand()
        for i in range(5):
            for j in players:
                j.take_card(self.cards.pop())




class Player():

    def __init__(self, money:int, name="",hand=[]):
        self.__stack_ = money
        self.__name_ = name
        self.__hand_ = hand


    def take_card(self, card):
        self.__hand_.append(card)

    def get_stack_amount(self):
        return self.__stack_
    def get_name(self):
        return self.__name_
    def update_stack_amount(self,amount:int):
        self.__stack_=max(0,self.__stack_-amount)
    def change_card(self, card, idx):
        d=self.__hand_[idx]
        self.__hand_[idx]=card
        return d
    def reset_hand(self):
        self.__hand_ = []

    def get_player_hand(self):
        return tuple(self.__hand_)

    def cards_to_str(self):

        s="karty gracza {name}\n".format(name=self.__name_)
        for i in self.__hand_:
            s+="{karta} ".format(karta=i)

        return s

#a=Card(11,'s')
#p=Player(10,"p1")

#p2=Player(10,"p2")
#b=Deck()
#b.shuffle()
#b.deal([p,p2])

#print(p.cards_to_str())

#print(p2.cards_to_str())