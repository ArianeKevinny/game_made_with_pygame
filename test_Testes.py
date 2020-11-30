from MyPlayer import Player
from Blocks import Block
from functions import first_block
import pytest

@pytest.fixture
def obj_player():
    return Player("galinha")

@pytest.fixture
def obj_blocks():
    return Block("forest")

# Teste de caixa preta
def test_check_player_x(obj_player):
    # Checar posição X do personagem
    assert obj_player.player_x == 100


def test_check_player_y(obj_player):
    # Checar posição Y do personagem
    assert obj_player.original_y <= obj_player.player_y <= obj_player.original_y + 130


def test_check_player_lives(obj_player):
    # Checar vidas do personagens
    assert 0 <= obj_player.lives <= 3


def test_check_player_num_stars(obj_player):
    # Checar número de estrelas dos personagens
    assert 0 <= obj_player.num_stars <= 3


def test_check_player_nivel(obj_player):
    # Checar nível
    assert 1 <= obj_player.nivel <= 3


def test_check_player_state(obj_player):
    # Checar estado
    assert obj_player.state in ["still", "jumping", "falling", "dead"]


def test_check_blocks_num(obj_blocks):
    # Checar número de blocos
    assert 2 <= obj_blocks.num_blocks <= 8 or obj_blocks.num_blocks == 25

def test_check_blocks_pos_x(obj_blocks):
    for i in range(len(obj_blocks.pos_t)):
        # Checar posição X dos blocos superiores
        assert obj_blocks.pos_t[i][0] == 600 + (i * 40)
        # Checar posição X dos blocos inferiores
        assert obj_blocks.pos_t[i][0] == 600 + (i * 40)

def test_check_blocks_pos_y(obj_blocks):
    for i in range(len(obj_blocks.pos_t)):
        # Checar posição Y dos blocos superiores
        assert obj_blocks.pos_t[i][1] == 400
        # Checar posição Y dos blocos inferiores
        assert obj_blocks.pos_t[i][1] == 400

def test_first_block():
    positions = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600, 640, 680, 720, 760, 800, 840, 880, 920, 960]
    b = first_block("forest")
    for i in range(b.num_blocks):
        assert b.pos_t[i][0] == positions[i]
        assert b.pos_b[i][0] == positions[i]