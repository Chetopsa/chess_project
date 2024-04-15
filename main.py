
import chess
import math
import pygame
import sys
import time

GUI_MODE = True

def alphabeta_search(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move
    infinity = math.inf
    def max_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)

# draw the board in gui mode
def draw_board(screen, board):
    colors = [pygame.Color("white"), pygame.Color("grey")]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            color = colors[((r+c)%2)]
            if selected_square != None and selected_square // 8 == r and selected_square % 8 == c:
                pygame.draw.rect(screen, (255,50,50), pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def draw_pieces(screen, board):
    for r in range(0, 8):
        for c in range(0, 8):
            squareIndex=r*8+c
            square = chess.SQUARES[squareIndex]
            piece = board.piece_at(square)
            if piece:
                img = pygame.image.load(piece_images[piece.symbol()])
                img = pygame.transform.scale(img, PIECE_SIZE)
                screen.blit(img, (c * SQUARE_SIZE, r * SQUARE_SIZE))
board = chess.Board()
if(GUI_MODE):
    piece_images = {
        'K': './pieces-basic-png/white-king.png',
        'k': './pieces-basic-png/black-king.png',
        'Q': './pieces-basic-png/white-queen.png',
        'q': './pieces-basic-png/black-queen.png',
        'B': './pieces-basic-png/white-bishop.png',
        'b': './pieces-basic-png/black-bishop.png',
        'R': './pieces-basic-png/white-rook.png',
        'r': './pieces-basic-png/black-rook.png',
        'N': './pieces-basic-png/white-knight.png',
        'n': './pieces-basic-png/black-knight.png',
        'P': './pieces-basic-png/white-pawn.png',
        'p': './pieces-basic-png/black-pawn.png'
    }
    SQUARE_SIZE = 60
    PIECE_SIZE = (SQUARE_SIZE - 4, SQUARE_SIZE - 4)
    BOARD_SIZE = 8
    pygame.init() 
    screen = pygame.display.set_mode((SQUARE_SIZE*BOARD_SIZE, SQUARE_SIZE*BOARD_SIZE))
    pygame.display.set_caption('CHESS')

def end_game():
    if board.is_stalemate():
        print("game ends in a tie")
        return True
    elif board.is_checkmate():
        print("checkmate")
        return True
    return False
def promotion_popup(screen):
    chosen = False
    font = pygame.font.Font(None, 36)
    popup_rect = pygame.Rect(150, 100, 300, 200)
    options = ['Queen: press q', 'Rook: press r', 'Bishop: press b', 'Knight: press k']
    option_rects = []

    pygame.draw.rect(screen, (200,200,200), popup_rect)
    for index, option in enumerate(options):
        option_rect = pygame.Rect(150, 150 + 30 * index, 300, 30)
        option_rects.append(option_rect)
        text = font.render(option, True, (0,0,0))
        screen.blit(text, (option_rect.x + 10, option_rect.y + 5))
    ret = ''
    while(not (ret == 5 or ret == 4 or ret == 2 or ret == 3)):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    return 0
                if event.key == pygame.K_q:
                    ret = 5
                elif event.key == pygame.K_r:
                    ret = 4
                elif event.key == pygame.K_k:
                    ret = 2
                elif event.key == pygame.K_b:
                    ret = 3
        pygame.display.flip()
    return ret

def attempt_promotion(white_turn, piece, selected_square, square):
    if white_turn and piece == 'P' and square // 8 == 7 or not white_turn and piece == 'p' and square // 8 == 0:
        print("hey")
        promo_piece = promotion_popup(screen)
        move = chess.Move(selected_square, square, promo_piece)
        if move in board.legal_moves:
            board.push(move)
            return True
    return False

        
def attempt_move(white_turn, selected_square, square):
    piece = board.piece_at(selected_square).symbol()
    if (white_turn and piece.isupper()) or ((not white_turn) and piece.islower()):
        if(attempt_promotion(white_turn, piece, selected_square, square)):
            return True
        move = chess.Move(selected_square, square)
        print(board.legal_moves)
        if move in board.legal_moves:
            board.push(move)
            return True
    return False
# main loop
running = True
white_turn = True
selected_square = None

while running:
    if GUI_MODE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                print(row, col)
                square = chess.square(col,row)
                if selected_square == None:
                    if board.piece_at(square):
                        selected_square = square
                else:
                    if(attempt_move(white_turn, selected_square, square)):
                        print("valid_move")
                        white_turn = not white_turn
                        pygame.display.set_caption("WHITE TURN" if white_turn else "BLACK TURN")
                        selected_square = None
                    else:
                        print("try again")
                        selected_square = None
    
        draw_board(screen, board)
        draw_pieces(screen, board)
        pygame.display.flip()
    else:
        print(board.unicode())
        time.sleep(10000)
    if end_game():
        running = False
if GUI_MODE:
    pygame.quit()
# print(board.legal_moves)  
# chess.Move.from_uci("a8a1") in board.legal_moves
# print(board)

#do end game stuff and logging
