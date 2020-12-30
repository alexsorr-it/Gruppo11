from Esercizio2Intracorso.Currency import Currency


def differentWays(curr, r):
    """
    :param curr: currency object
    :param r: amount to achieve using denominations of currency object
    :return: tuple containing, as first parameter, the number of different ways that value r can be achieved by using
             denominations of the given currency; as second parameter, the list of different changes of the value r that
             can be achieved by using denominations of the given currency
    """

    # According to what was communicated, we have assumed that both denominations and r are integers (this is equivalent
    # to saying that instead of having the quantity r and the denominations of a coin defined in units of the same, we
    # have defined them in cents of the same). In other words, we can't have float values
    if not isinstance(r, int):
        return "Please, insert only integer values as 'r'."

    if not isinstance(curr, Currency):
        return "Please, insert a Currency object as 'curr'."

    if r < 0:
        return "Please, insert only positive integer values as 'r'."

    # Initializing matrix 'a'
    a = [[0] * (r+1) for _ in range(0, curr.numDenominations()+1)]
    for _ in range(0, curr.numDenominations()+1):
        a[_][0] = 1

    # Appending denominations to list of coins
    it = curr.iterDenominations(False)
    coins = []
    for denomination in it:
        if not isinstance(denomination, int):
            return "Please, insert only integer values as 'denominations'."
        coins.append(denomination)

    if r < coins[0]:
        return 0, ""

    # Constructing matrix containing the number of different ways that value r can be achieved by using denominations
    # of the given currency
    for i in range(1, curr.numDenominations()+1):
        for j in range(1, r+1):
            if i == 1:
                if j % coins[0] == 0:
                    a[1][j] = 1
                else:
                    a[1][j] = 0
            elif coins[i-1] > j:
                a[i][j] = a[i-1][j]
            else:
                a[i][j] = a[i-1][j] + a[i][j-coins[i-1]]
    return a[-1][-1], differentCombinations(coins, len(coins)-1, r, [], [], a)

def differentCombinations(coins, row, r, combination, totalCombinations, matrix):
    """
    :param coins: list of denominations
    :param row: index of row in matrix
    :param r: index of column in matrix
    :param combination: list of single combination of denominations
    :param totalCombinations: list of all combinations of denominations
    :param matrix: matrix containing number of combinations
    :return: list of total combinations
    """

    # When reaching column with index 0, add the combination found to total combinations.
    if r == 0:
        if len(totalCombinations) < 1000:  # Stop when you found 1000 combinations.
            totalCombinations.append(combination)
        return

    # If the matrix cell with row "row" and column "r" contains a value >=1, then there is at least one way to find
    # the combination on the previous rows. Moreover, we need a copy of "combination" because at each recursion we add
    # to "totalCombinations" every single coin that contributes to the creation of the combination
    if matrix[row][r] >= 1:
        differentCombinations(coins, row - 1, r, combination[:], totalCombinations, matrix)

    # If the difference "r - coins[row - 1]" is a positive number (or at least 0), and if the matrix cell with row "row"
    # and column "r - coins[row - 1]" contains a value >=1, then there is at least one way to find the combination on
    # the same row.
    if r >= coins[row - 1]:
        if matrix[row][r - coins[row - 1]] >= 1:
            combination.append(coins[row - 1])
            differentCombinations(coins, row, r - coins[row - 1], combination, totalCombinations, matrix)

    return totalCombinations
