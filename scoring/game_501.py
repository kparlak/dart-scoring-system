class Game501():
    def __init__(self):
        self.score = 501
        self.winner = False

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def get_winner(self):
        return self.winner

    def calc_hit(self, number, ring):
        if ring == 'B' or ring == 'D':
            return number
        elif ring == 'A':
            return number * 2
        elif ring == 'C':
            return number * 3
        elif ring == 'X':
            return 25
        elif ring == 'Y':
            return 50
        else:
            return 0

    def update(self, number, ring):
        hit = self.calc_hit(number, ring)
        temp_score = self.score - hit
        if temp_score < 0:
            return self.score
        elif temp_score == 0:
            if ring == 'A':
                self.winner = True
                return temp_score
            else:
                return self.score
        else: #temp_score > 0
            return temp_score

# EOF
