class Piece:
    def __init__(self, color, file, rank):
        self.color = color
        self.file = file
        self.rank = rank


class Pawn(Piece):
    ranged = False
    moves = [[0, 1]]
    attacks = [[1, -1], [1, 1]]
    symbol = 'P'


class Rook(Piece):
    ranged = True
    moves = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    attacks = moves
    symbol = 'R'


class Knight(Piece):
    ranged = False
    moves = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
    attacks = moves
    symbol = 'N'


class Bishop(Piece):
    ranged = True
    moves = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
    attacks = moves
    symbol = 'B'


class Queen(Piece):
    ranged = True
    moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    attacks = moves
    symbol = 'Q'


class King(Piece):
    ranged = False
    moves = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    attacks = moves
    symbol = 'K'


piece_initial_layout = \
    [[Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook], [Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn]]

BOARD_LENGTH = 8


class Player:
    def __init__(self, color_letter):
        self.pieces = []
        self.color_letter = color_letter
        self.in_check = False
        self.moves = {}
        self.move_list = []
        self.attacking = []


class Game:
    def display_board(self):
        for j in range(BOARD_LENGTH - 1, -1, -1):
            for i in range(BOARD_LENGTH):
                if self.board[i][j]:
                    print(f'{self.board[i][j].symbol}{self.board[i][j].color.color_letter}', end='')
                print('\t', end='')
            print()

    def in_check(self, player):
        if player == self.white:
            opponent = self.black
        else:
            opponent = self.white
        for piece in opponent.pieces:
            for attack in piece.attacks:
                attack_file = piece.file + attack[0]
                if opponent == self.white:
                    attack_rank = piece.rank + attack[1]
                else:
                    attack_rank = piece.rank - attack[1]
                while attack_file >= 0 and attack_file < BOARD_LENGTH and attack_rank >= 0 and attack_rank < BOARD_LENGTH:
                    if self.board[attack_file][attack_rank]:
                        if self.board[attack_file][attack_rank].color == player and self.board[attack_file][
                            attack_rank].__class__.__name__ == 'King':
                            return True
                        break
                    if not piece.ranged:
                        break
                    attack_file = attack_file + attack[0]
                    if opponent == self.white:
                        attack_rank = attack_rank + attack[1]
                    else:
                        attack_rank = attack_rank - attack[1]
        return False

    def move(self, piece, file, rank):
        self.premove_board = {(piece.file, piece.rank): self.board[piece.file][piece.rank],
                              (file, rank): self.board[file][rank]}
        if self.board[file][rank]:
            self.board[file][rank].color.pieces.remove(self.board[file][rank])
        self.board[piece.file][piece.rank] = None
        self.board[file][rank] = piece
        piece.file = file
        piece.rank = rank

    def unmove(self):
        for (square, piece) in self.premove_board.items():
            if piece:
                if piece in piece.color.pieces:
                    piece.file = square[0]
                    piece.rank = square[1]
                else:
                    piece.color.pieces.append(piece)
            self.board[square[0]][square[1]] = piece

    def valid(self, player, piece, file, rank, special=False):
        valid_move = True
        if not special:
            self.move(piece, file, rank)
            if self.in_check(player):
                print(f'A move of {piece.__class__.__name__} to {file, rank} would place {player.color_letter} in check.')
                valid_move = False
        self.unmove()
        return valid_move

    def determine_moves(self, player):
        for piece in player.moves:
            player.moves[piece].clear()
        player.move_list.clear()
        for piece in player.pieces:
            current_file = piece.file
            current_rank = piece.rank
            for move in piece.moves:
                move_file = piece.file + move[0]
                if player == self.white:
                    move_rank = piece.rank + move[1]
                else:
                    move_rank = piece.rank - move[1]
                while move_file >= 0 and move_file < BOARD_LENGTH and move_rank >= 0 and move_rank < BOARD_LENGTH:
                    if self.board[move_file][move_rank]:
                        other_piece = self.board[move_file][move_rank]
                        if other_piece.color != player:
                            if piece.__class__.__name__ != 'Pawn':
                                if self.valid(player, piece, move_file, move_rank):
                                    player.moves[piece].append((move_file, move_rank))
                        break
                    else:
                        if self.valid(player, piece, move_file, move_rank):
                            player.moves[piece].append((move_file, move_rank))
                        if piece.__class__.__name__ == 'Pawn':
                            if piece.color == self.white and piece.rank == 1 and not self.board[piece.file][
                                3] and self.valid(player, piece, piece.file, 3):
                                player.moves[piece].append((piece.file, 3))
                            elif piece.color == self.black and piece.rank == 6 and not self.board[piece.file][
                                4] and self.valid(player, piece, piece.file, 4):
                                player.moves[piece].append((piece.file, 4))
                        if not piece.ranged:
                            break
                        move_file = move_file + move[0]
                        if player == self.white:
                            move_rank = move_rank + move[1]
                        else:
                            move_rank = move_rank - move[1]
            if piece.__class__ == 'Pawn':
                for attack in piece.attacks:
                    attack_file = piece.file + attack[0]
                    if attack_file >= 0 and attack_file < BOARD_LENGTH:
                        if player == self.white:
                            attack_rank = piece.rank + attack[1]
                        else:
                            attack_rank = piece.rank - attack[1]
                        if attack_rank >= 0 and attack_rank < BOARD_LENGTH and self.board[attack_file][attack_rank] and \
                                self.board[attack_file][attack_rank].color != player.color and self.valid(player, piece,
                                                                                                          attack_file,
                                                                                                          attack_rank):
                            player.moves[piece].append((attack_file, attack_rank))
        for piece in player.moves:
            for move in player.moves[piece]:
                player.move_list.append((piece, move))

    def play(self):
        self.display_board()
        print('Determining moves.')
        self.determine_moves(self.turn)
        print('Determined moves.')
        if self.turn.move_list:
            if self.turn.in_check:
                print('Check!')
            if self.turn == self.white:
                print('White to move.')
            else:
                print('Black to move.')
            print('Possible moves:')
            number = 0
            for (number, move) in enumerate(self.turn.move_list, start=1):
                print(f'{number}. {move[0].__class__.__name__}: {move[1]}')
            print('Enter the number of the move you choose.')
            number = int(input()) - 1
            self.move(self.turn.move_list[number][0], self.turn.move_list[number][1][0], self.turn.move_list[number][1][1])
            if self.turn == self.white:
                self.turn = self.black
            else:
                self.turn = self.white
            if self.in_check(self.turn):
                self.turn.in_check = True
            self.play()
        else:
            if self.turn.in_check:
                print('Checkmate!')
                if self.turn == self.white:
                    print('Black wins!')
                else:
                    print('White wins!')
            else:
                print("Stalemate! It's a draw!")

    def place(self):
        for i in range(len(piece_initial_layout)):
            for j in range(len(piece_initial_layout[0])):
                piece = piece_initial_layout[i][j](self.white, j, i)
                self.board[j][i] = piece
                self.white.pieces.append(piece)
                self.white.moves[piece] = []
                piece = piece_initial_layout[i][j](self.black, j, BOARD_LENGTH - 1 - i)
                self.board[j][BOARD_LENGTH - 1 - i] = piece
                self.black.pieces.append(piece)
                self.black.moves[piece] = []

    def __init__(self):
        self.board = []
        self.premove_board = {}
        self.white = Player('w')
        self.black = Player('b')
        self.turn = self.white
        for i in range(BOARD_LENGTH):
            file = []
            for j in range(BOARD_LENGTH):
                file.append(None)
            self.board.append(file)
        self.place()
        self.play()


game = Game()
