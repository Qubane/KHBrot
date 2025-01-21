import num2words
import numpy as np
from PIL import Image
from string import whitespace, punctuation


BOARD_SIZE: int = 1024
ITERATION_LIMIT: int = 64
SENTENCE: str = "This sentence has {num1} vowels and {num2} consonants"


def count_letters(string: str) -> tuple[int, int]:
    """
    Counts vowels and consonants
    :param string: string
    :return: vowels, consonants
    """

    vowels = (string.count("a") +
              string.count("e") +
              string.count("i") +
              string.count("o") +
              string.count("u"))
    other = 0
    for char in whitespace + punctuation:
        other += string.count(char)
    return vowels, len(string) - vowels - other


def iterate_pos(x: int, y: int) -> float:
    """
    Iterate position
    :param x: pos x
    :param y: pos y
    :return: 0 - 1 float
    """

    for i in range(ITERATION_LIMIT):
        sentence = SENTENCE.format(num1=num2words.num2words(x), num2=num2words.num2words(y))
        vowels, consonants = count_letters(sentence)
        if vowels == x and consonants == y:
            return i / ITERATION_LIMIT
        x, y = vowels, consonants
    return 1


def main():
    img = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.float32)
    min_, max_ = 255, 0
    for y in range(BOARD_SIZE):
        print(f"Done: {y/BOARD_SIZE*100:.2f}%")
        for x in range(BOARD_SIZE):
            iters = iterate_pos(x, y)
            min_, max_ = min(min_, iters), max(max_, iters)
            img[y][x] = iters
    img = np.ndarray.astype((img - min_) / (max_ - min_) * 255, dtype=np.uint8)

    Image.fromarray(img).save("img.png")


if __name__ == '__main__':
    main()
