import random


def generate_token(length=30, chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    rand = random.SystemRandom()
    return ''.join(rand.choice(chars) for _ in range(length))
