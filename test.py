import itertools
import random

# Fonction pour générer un plateau de jeu initial
def generate_board(size):
    board = [[0 for _ in range(size)] for _ in range(size)]
    numbers = list(range(1, size * size))
    random.shuffle(numbers)
    for i in range(size):
        for j in range(size):
            board[i][j] = 0 if i == size - 1 and j == size - 1 else numbers.pop()
    return board

# Fonction pour afficher le plateau de jeu
def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))

# Fonction pour vérifier si le joueur a gagné
def check_win(board):
    size = len(board)
    for current_number, (i, j) in enumerate(itertools.product(range(size), range(size)), start=1):
        if i == size - 1 and j == size - 1:
            if board[i][j] != 0:
                return False
        elif board[i][j] != current_number:
            return False
    return True

# Fonction pour déplacer une pièce
def move_piece(board, piece):
    size = len(board)
    empty_row, empty_col = 0, 0

    # Trouver la position de la case vide
    for i, j in itertools.product(range(size), range(size)):
        if board[i][j] == 0:
            empty_row, empty_col = i, j

    # Vérifier si le déplacement est valide
    if (
        piece[0] < 0
        or piece[0] >= size
        or piece[1] < 0
        or piece[1] >= size
        or (abs(piece[0] - empty_row) + abs(piece[1] - empty_col) != 1)
    ):
        return False

    # Échanger la pièce avec la case vide
    board[empty_row][empty_col], board[piece[0]][piece[1]] = board[piece[0]][piece[1]], board[empty_row][empty_col]
    return True

# Fonction principale
def main():
    size = 3  # Taille du plateau de jeu (3x3)
    board = generate_board(size)
    print("Bienvenue dans le jeu de taquin !")
    print_board(board)

    while not check_win(board):
        try:
            row, col = map(int, input("Entrez les coordonnées de la pièce à déplacer (ligne colonne) : ").split())
            if move_piece(board, (row, col)):
                print_board(board)
            else:
                print("Mouvement invalide. Réessayez.")
        except (ValueError, IndexError):
            print("Coordonnées invalides. Réessayez.")

    print("Félicitations, vous avez gagné !")

if __name__ == "__main__":
    main()
