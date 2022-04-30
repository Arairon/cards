hand = ['c14', 's7','c12',"h6"]
trump = 'c13'
def cardSort(cards):
    trump = 'h13'
    order = {'s': 4, 'c': 3, 'h': 2, 'd': 1, trump[0]: 5}
    return sorted(cards, key=lambda item: (int(order.get(item[0], 100)), item[1:]), reverse=True)
print(cardSort(hand))