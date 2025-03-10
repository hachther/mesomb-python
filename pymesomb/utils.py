import random
import re
import string


class RandomGenerator:
    """ """
    @staticmethod
    def nonce(length=40):
        """

        Args:
          length:  (Default value = 40)

        Returns:

        """
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))


def detect_operator(phone, country='CM'):
    """Detect the operator of a phone number in a country (only cameroon is supported for now)

    Args:
      phone: 
      country:  (Default value = 'CM')

    Returns:

    """
    OPERATOR_REGEX = {
        'MTN': r'^(237)?(67|65[0-4]|68[0-3])',
        'ORANGE': r'^(237)?(69|65[5-9])',
        'NEXTTEL': r'^(237)?(66)',
        'YOOMEE': r'^(237)?(242)',
        'CAMTEL': r'^(237)?(233|222|243|62)',
        'MESOMB': r'^7',
    }
    for operator, regex in OPERATOR_REGEX.items():
        if re.match(regex, phone):
            return operator
