class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        deposit_dict = {'amount': amount, 'description': description}
        self.ledger.append(deposit_dict)

    def withdraw(self, amount, description='') -> bool:
        if self.ledger:
            current_balance = self.ledger[0].get('amount', 0)

            if not self.check_funds(amount):
                return False

            deposit_dict = {'amount': -amount,
                            'description': description}
            self.ledger.append(deposit_dict)
            return True

    def get_balance(self) -> float:
        if self.ledger:
            balance = 0
            for item in self.ledger:
                balance += item['amount']

            return balance

    def transfer(self, amount, category_obj) -> bool:
        if not self.check_funds(amount):
            return False

        success_transfer = self.withdraw(
            amount, f'Transfer to {category_obj.name}')
        if not success_transfer:
            return False

        category_obj.deposit(amount, f'Transfer from {self.name}')
        return True

    def check_funds(self, amount):
        if self.ledger:
            current_balance = self.ledger[0].get('amount', 0)
            return False if amount > current_balance else True

    def __str__(self) -> str:
        final_str = ''

        fill = '*'
        size = 30
        align = '^'
        final_str += f'{self.name:{fill}{align}{size}}\n'

        fill = ' '
        size = 7
        align = '>'

        total_amount = 0
        for item in self.ledger:
            total_amount += item['amount']
            final_str += f'{item["description"][:23]:<23}{item["amount"]:{fill}{align}{size}.2f}\n'

        final_str += f'Total: {total_amount:.2f}'
        return final_str


def create_spend_chart(categories) -> str:
    withdraws_list = [get_total_withdraw(
        category.ledger) for category in categories]
    withdraws_sum = sum(withdraws_list)
    withdraws_list_percentage = [get_percentage(
        withdraws_sum, category_withdraw) for category_withdraw in withdraws_list]

    s = 'Percentage spent by category\n'
    for label in range(100, -10, -10):
        s += f'{label:>3}|'
        for percentage in withdraws_list_percentage:
            symbol = get_circle(percentage, label)
            s += symbol

        s += ' \n'

    s += '    ' + '---' * len(categories) + '-\n'

    categories_name_len = [len(category.name) for category in categories]
    longest_name_cat = max(categories_name_len)

    for i in range(longest_name_cat):
        s += '    '
        for category in categories:
            s += get_character(i, category.name)
        s += ' \n' if i < longest_name_cat-1 else ' '

    return s


def get_character(index, name):
    '''
    Returns the character in form ' F ' from `name` at given `index`, 
    otherwise returns 3 whitespaces.
    '''
    return f' {name[index]} ' if index < len(name) else '   '


def get_circle(amount, label) -> str:
    return ' o ' if amount >= label else '   '


def get_total_withdraw(ledger_list):
    total = 0
    for item in ledger_list:
        if item['amount'] < 0:
            total += abs(item['amount'])
    return total


def get_percentage(total, rate):
    '''
    Returns the percentage of `rate` in relation to `total`.
    '''
    percentage = (rate * 100) / total
    return percentage


# \n
# 100|          \n
#  90|          \n
#  80|          \n
#  70|    o     \n
#  60|    o     \n
#  50|    o     \n
#  40|    o     \n
#  30|    o     \n
#  20|    o  o  \n
#  10|    o  o  \n
#   0| o  o  o  \n
#     ----------\n
#      B  F  E  \n
#      u  o  n  \n
#      s  o  t  \n
#      i  d  e  \n
#      n     r  \n
#      e     t  \n
#      s     a  \n
#      s     i  \n
#            n  \n
#            m  \n
#            e  \n
#            n  \n
#            t


# 'Percentage spent by category\n
# 100|         \n
#  90|         \n
#  80|         \n
#  70|    o    \n
#  60|    o    \n
#  50|    o    \n
#  40|    o    \n
#  30|    o    \n
#  20|    o  o \n
#  10|    o  o \n
#   0| o  o  o \n
#    ----------\n
#      B  F  E \n
#      u  o  n \n
#      s  o  t \n
#      i  d  e \n
#      n     r \n
#      e     t \n
#      s     a \n
#      s     i \n
#            n \n
#            m \n
#            e \n
#            n \n
#            t \n
