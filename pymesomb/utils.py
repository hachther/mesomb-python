import random
import string


class RandomGenerator:
    @staticmethod
    def nonce(length=40):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))
