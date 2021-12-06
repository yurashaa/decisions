from prettytable import PrettyTable
from simplex import Simplex

def read_lines():
    lines = []
    with open("v7.txt", "r") as f:
        rows = f.readlines()
        for row in rows:
            to_add = row.replace('\n', '')
            lines.append([int(numeric_string) for numeric_string in to_add.split(' ')])

    return lines


def get_matrix_table(matrix):
    if len(matrix) < 1: return ''

    x = PrettyTable()
    fields = ['']
    for i in range(len(matrix[0])):
        fields.append("B" + str(i + 1))

    x.field_names = fields
    for i in range(len(matrix)):
        x.add_row(['A' + str(i + 1)] + matrix[i])
    return x


def check_saddle_point(minA, maxB):
    maxFromMatrixA = minA[max(minA, key = minA.get)]
    minFromMatrixB = maxB[min(maxB, key = maxB.get)]
    return [maxFromMatrixA, minFromMatrixB]


def check_rows(firstRow, secondRow):
    equalElements = 0
    for i in range(len(firstRow)):
        if firstRow[i] < secondRow[i]: return 0
        if firstRow[i] == secondRow[i]: equalElements += equalElements

    return 0 if equalElements == len(firstRow) else 1


def check_dominant_rows(matrix):
    matrixAfterExcludingRows = []
    deletedRows = []

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j: continue
            result = check_rows(matrix[i], matrix[j])
            if result != 0 and j not in deletedRows:
                deletedRows.append(j)
                print("Стретегія А" + str(i + 1), "домінуюча над стратегією А" + str(j + 1), "тому забираємо рядок", j + 1)

    for i in range(len(matrix)):
        if i in deletedRows: continue
        matrixAfterExcludingRows.append(matrix[i])

    return matrixAfterExcludingRows


def check_dominant_columns(matrix):
    matrixAfterExcludingColumns = []
    deletedColumns = []
    transposedMatrix = [list(x) for x in zip(*matrix)]

    for i in range(len(transposedMatrix)):
        for j in range(len(transposedMatrix)):
            if i == j: continue
            result = check_rows(transposedMatrix[j], transposedMatrix[i])
            if result != 0 and j not in deletedColumns:
                deletedColumns.append(j)
                print("Стретегія В" + str(i + 1), "домінуюча над стратегією В" + str(j + 1), "тому забираємо стовпчик", j + 1)
    
    for i in range(len(matrix)):
        matrixAfterExcludingColumns.append([])
        for j in range(len(matrix[i])):
            if j in deletedColumns: continue
            matrixAfterExcludingColumns[i].append(matrix[i][j])

    return matrixAfterExcludingColumns


matrix = read_lines()

print("Вхідні дані")
print(get_matrix_table(matrix))

print("Перевірка матриці на наявність сідлової точки")
x = PrettyTable()
fields = ['']
for i in range(len(matrix)):
    fields.append("B" + str(i + 1))

fields.append('a = min(Ai)')
x.field_names = fields

minA = {}
maxB = {}

for i in range(len(matrix)):
    minA[i] = min(matrix[i])
    x.add_row(['A' + str(i + 1)] + matrix[i] + [str(minA[i])])
    for j in range(len(matrix[i])):
        if j not in maxB or maxB[j] < matrix[i][j]:
            maxB[j] = matrix[i][j]

x.add_row(['b = max(Bi)'] + [maxB[element] for element in maxB] + [''])
print(x)

[maxFromMatrixA, minFromMatrixB] = check_saddle_point(minA, maxB)
if maxFromMatrixA == minFromMatrixB:
    print("Сідлова точка присутня!")
else:
    print("a = max(min(Ai)) =", maxFromMatrixA)
    print("b = min(max(Bi)) =", minFromMatrixB)
    print("Сідлова точка відсутня, так як a != b")
    print("Ціна гри знаходиться в межах:", maxFromMatrixA, "<= y <=", minFromMatrixB) 


print("\nПеревірка матриці на домінуючі рядки і домінуючі стовпці:")
print("З позиції виграшу гравця А")
matrixAfterExcludingRows = check_dominant_rows(matrix)
print("Після перевірки домінуючих рядків наша матриця набула наступного вигляду: ")
print(get_matrix_table(matrixAfterExcludingRows))


print("З позиції програшу гравця В")
matrixAfterExcludingColumns = check_dominant_columns(matrixAfterExcludingRows)
print("Після перевірки домінуючих стовпчиків наша матриця набула наступного вигляду: ")
print(get_matrix_table(matrixAfterExcludingColumns))

transposedMatrix = [list(x) for x in zip(*matrixAfterExcludingColumns)]
print("\nЗнаходимо рішення гри в змішаних стратегіях")
print("Знайти мінімум функції F(x) при обмеженнях (для гравця ||)")

secondPlayersConditions = []
for i in range(len(transposedMatrix)):
    secondPlayersConditions.append('')
    for j in range(len(transposedMatrix[i])):
        secondPlayersConditions[i] += str(transposedMatrix[i][j]) + 'x_' + str(j + 1) + ' + '

for i in range(len(secondPlayersConditions)):
    print(secondPlayersConditions[i][:-2] + '>= 1')

mainCondition = 'F(x) = '
for i in range(len(matrixAfterExcludingColumns)):
    mainCondition += 'x_' + str(i + 1) + ' + '

print(mainCondition[:-2] + '--> min')

print("Знайти мінімум функції Z(y) при обмеженнях (для гравця |)")
firstPlayersConditions = []

vars_count = 0
for i in range(len(matrixAfterExcludingColumns)):
    firstPlayersConditions.append('')
    columns = len(matrixAfterExcludingColumns[i])
    for j in range(columns):
        firstPlayersConditions[i] += str(matrixAfterExcludingColumns[i][j]) + 'y_' + str(j + 1) + ' + '
        if columns > vars_count:
            vars_count = columns

conditions = ''
for i in range(len(firstPlayersConditions)):
    firstPlayersConditions[i] = firstPlayersConditions[i][:-2] + '<= 1'

mainCondition = ''
for i in range(len(transposedMatrix)):
    mainCondition += '1y_' + str(i + 1) + ' + '

mainCondition = mainCondition[:-2]

for line in firstPlayersConditions:print(line)
print('Z(y) = ' + mainCondition + '--> max')

print("\nВирішимо пряму задачу лінійного програмування симплексним методом")
print("Визначимо максимальне значення цільової функції", mainCondition + '--> max', "при настуних умовах-обмеженнях:")
print(conditions)
print("Після переведення в канонічну форму переходимо до основно алгоритму симплекс-методом")

simplexResult = Simplex(num_vars=vars_count, constraints=firstPlayersConditions, objective_function=mainCondition)
print("\nОтримуємо наступні результати:")

x_result = {}
y_result = {}
for key in simplexResult.solution:
    if 'y_' in key:
        y_result[key] = simplexResult.solution[key]
    elif 'x_' in key:
        x_result[key] = simplexResult.solution[key]

yResultCond = 'F(y) = '
yResult = 0
for i in range(vars_count):
    print('y' + str(i + 1) + ' =', y_result['y_' + str(i + 1)], end=' ')
    yResult += 1 * y_result['y_' + str(i + 1)]
    yResultCond += "1 * " + str(y_result['y_' + str(i + 1)]) + ' + '


print("\n" + yResultCond[:-2] + '= ' + str(yResult), '\n')

xResultCond = 'F(x) = '
xResult = 0
vars_count = vars_count - 1
for i in range(vars_count):
    print('x' + str(i + 1) + ' =', x_result['x_' + str(i + 1)], end=' ')
    xResult += 1 * x_result['x_' + str(i + 1)]
    xResultCond += "1 * " + str(x_result['x_' + str(i + 1)]) + ' + '


print("\n" + xResultCond[:-2] + '= ' + str(xResult))

print("\nЦіна гри буде рівна g = 1/F(x)")
print("g = 1/(" + str(xResult), ") =", str(1/xResult))
