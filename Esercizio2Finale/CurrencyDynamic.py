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
    if isinstance(r, float):
        return "Please, insert only integer values as 'r'."

    # Initializing matrix 'a'
    a = [[1] * (r+1) for _ in range(0, curr.numDenominations())]

    # Appending denominations to list of coins
    it = curr.iterDenominations(False)
    coins = []
    for denomination in it:
        if isinstance(denomination, float):
            return "Please, insert only integer values as 'denominations'."
        coins.append(denomination)

    # Constructing matrix containing the number of different ways that value r can be achieved by using denominations
    # of the given currency
    for i in range(0, curr.numDenominations()):
        for j in range(1,r+1):
            if i == 0:
                if j % coins[0] == 0:
                    a[0][j] = 1
                else:
                    a[0][j] = 0
            elif coins[i] > j:
                a[i][j] = a[i-1][j]
            else:
                a[i][j] = a[i-1][j] + a[i][j-coins[i]]

    # Constructing the list of different changes of the value r that can be achieved by using denominations of the
    # given currency
    totalCombinations = []
    for i in range(0, curr.numDenominations()):
        if coins[i] <= r:
            numCombinations = a[i][r-coins[i]]
            amount = r
            row = i
            combination = []
            count = 0
            cash = []
            while numCombinations > 0:
                amount = amount - coins[row]
                combination.append(coins[row])
                if amount == 0:
                    if combination not in totalCombinations:
                        totalCombinations.append(combination)
                        numCombinations = numCombinations - 1
                        combination = []
                        amount = r
                        row = i
                        count = 0
                    else:
                        # removing the coins that are not part of the current row
                        for c in range(len(combination)-1, 0, -1):
                            if combination[c] != coins[i]:
                                combination.pop(c)
                        amount = r
                        row = i
                        # removing the coins that are part of the current row but for which an analysis has already been made
                        if len(combination) > 1:
                            combination.pop(len(combination) - 1)
                        else:
                            row = row - 1
                        for am in range(0, len(combination)):
                            amount = amount - combination[am]
                        row = row - 1
                elif amount < 0:
                    if row - 1 < 0:
                        # removing the coins that are not part of the current row
                        for c in range(len(combination) - 1, 0, -1):
                            if combination[c] != coins[i]:
                                combination.pop(c)
                        amount = r
                        row = i
                        # removing the coins that are part of the current row but for which an analysis has already been made
                        if len(combination) > 1:
                            combination.pop(len(combination) - 1)
                        else:
                            row = row - 1
                        for am in range(0, len(combination)):
                            amount = amount - combination[am]
                        row = row - 1
                    else:
                        cash.append(coins[row])
                        if cash[0] == cash[len(cash)-1]:
                            count = count + 1
                        else:
                            count = 1
                        for c in range(0, count):
                            combination.pop(len(combination) - 1)
                        amount = r
                        for am in range(0, len(combination)):
                            amount = amount - combination[am]
                        row = row - 1
        else:
            break

    return a[-1][-1], totalCombinations
