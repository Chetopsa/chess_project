import chess
import math

class Heuristic:
    '''
    first attempt did not work how I wanted it to, so just plays bad
    '''
    def hueristic_1(self, c_board, color):
        weight = 0
        attacked_squares = []
        # get pawn
        for square in c_board.pieces(chess.PAWN, c_board.turn):
            attacked_squares.append(c_board.attacks(square))
        # get Knight
        for square in c_board.pieces(chess.KNIGHT, c_board.turn):
            attacked_squares.append(c_board.attacks(square))
        # get Bishop
        for square in c_board.pieces(chess.BISHOP, c_board.turn):
            attacked_squares.append(c_board.attacks(square))
        # get Rook
        for square in c_board.pieces(chess.ROOK, c_board.turn):
            attacked_squares.append(c_board.attacks(square))
        # get QUEEN
        for square in c_board.pieces(chess.QUEEN, c_board.turn):
            attacked_squares.append(c_board.attacks(square))
        # get KING
        for square in c_board.pieces(chess.KING, c_board.turn):
            attacked_squares.append(c_board.attacks(square))

        for set in attacked_squares:
            for attacked in set:
                p_type = c_board.piece_at(attacked)
                if p_type != None:
                    p_type = p_type.symbol()
                    if p_type == 'P':
                        weight += 1
                    elif p_type == 'N':
                        weight += 3
                    elif p_type == 'B':
                        weight += 3
                    elif p_type == 'Q':
                        weight += 9
                    elif p_type == 'R':
                        weight += 5
                    elif p_type == 'K':
                        weight += 2

        defend_squares = []
        # get pawn
        for square in c_board.pieces(chess.PAWN, not c_board.turn):
            defend_squares.append(c_board.attacks(square))
        # get Knight
        for square in c_board.pieces(chess.KNIGHT, not c_board.turn):
            defend_squares.append(c_board.attacks(square))
        # get Bishop
        for square in c_board.pieces(chess.BISHOP, not c_board.turn):
            defend_squares.append(c_board.attacks(square))
        # get Rook
        for square in c_board.pieces(chess.ROOK, not c_board.turn):
            defend_squares.append(c_board.attacks(square))
        # get QUEEN
        for square in c_board.pieces(chess.QUEEN, not c_board.turn):
            defend_squares.append(c_board.attacks(square))
        # get KING
        for square in c_board.pieces(chess.KING, not c_board.turn):
            defend_squares.append(c_board.attacks(square))
        for set in defend_squares:
            for defend in set:
                p_type = c_board.piece_at(defend)
                if p_type != None:
                    p_type = p_type.symbol()
                    if p_type == 'P':
                        weight -= 1
                    elif p_type == 'N':
                        weight -= 3
                    elif p_type == 'B':
                        weight -= 3
                    elif p_type == 'R':
                        weight += 5
                    elif p_type == 'Q':
                        weight -= 9
                    elif p_type == 'K':
                        weight -= 2
        return weight

    '''
    simplplified uit just to add its board  weight and subtract the opponents and it actually is pretty good
    '''
    def count_pieces(self, c_board, color):
        weight = 0
        my_color = color
        # print(color)
        # print(c_board)
        enemy_pieces = []
        my_pieces = []
        piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
        # for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
        #     my_pieces = c_board.pieces(piece_type, my_color)
        #     enemy_pieces = c_board.pieces(piece_type, not my_color)
        if c_board.is_checkmate():
            return 10000
        if c_board.is_stalemate():
            return 0
        for square in chess.SQUARES:
                piece = c_board.piece_at(square)
                if piece:
                    piece_value = piece_values[piece.symbol().upper()]
                    if piece.color == my_color:
                        weight += piece_value
                        # print("         case white")
                    else:
                        weight -= piece_value
                        # print("          case black")
        # if my_color == True:
        #     print("white",weight)
        # else:
        #     print("   black", weight)
        return weight

    def heuristic_2(self, c_board, color):
        weight = 0
        my_color = color
        enemy_pieces = []
        my_pieces = []
        piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
        if c_board.is_checkmate():
            return 10000
        if c_board.is_stalemate():
            return 10000
        for square in chess.SQUARES:
                piece = c_board.piece_at(square)
                if piece:
                    piece_value = piece_values[piece.symbol().upper()]
                    if piece.color == my_color:
                        weight += piece_value
                    else:
                        weight -= piece_value
        
            
        return weight

