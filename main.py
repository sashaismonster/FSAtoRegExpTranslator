# Translator from FSA to Regular Expression
# Python v 3.8 is used

handle = open("input.txt", "r")
out = open("output.txt", "w")


# error messages for print depending on case
def err_out(case, to_print=""):
    out.write("Error:\n")
    if case == 0:
        out.write("E0: Input file is malformed")
    elif case == 1:
        out.write("E1: A state '" + to_print + "' is not in the set of states")
    elif case == 2:
        out.write("E2: Some states are disjoint")
    elif case == 3:
        out.write("E3: A transition '" + to_print + "' is not represented in the alphabet")
    elif case == 4:
        out.write("E4: Initial state is not defined")
    elif case == 5:
        out.write("E5: FSA is nondeterministic")
    exit(0)


# additional function to determine connectivity - BFS
def bfs(s):
    global marked
    marked = {a: False for a in states}

    marked[s] = True
    queue = [s]
    while queue:
        v = queue.pop(0)
        try:
            for w in complete[v]:
                if not (marked[w]):
                    queue.append(w)
                    marked[w] = True
        except KeyError:
            continue


def solve(R_prev, R_now):
    for k in range(n - 1):
        for i in range(n):
            for j in range(n):
                to_put = '(' + R_prev[i][k] + ')(' + R_prev[k][k] + ')*(' + R_prev[k][j] + ')|(' + R_prev[i][j] + ')'
                R_now[i][j] = to_put
        R_now, R_prev = R_prev, R_now

    ans = ''

    for ind in fin_index:
        ans += '(' + R_prev[init_index][n-1] + ')(' + R_prev[n-1][n-1] + ')*(' + R_prev[n-1][ind] + ')|(' + R_prev[init_index][ind] + ')' + '|'

    ans = ans[:-1]
    if len(ans) == 0:
        ans = '{}'
    return ans


# parsing input file and checking for malformation
tmp = handle.readline()
if tmp[0:8] == "states=[" and tmp[-2] == ']':
    states = tmp[8:-2].split(',')
    n = len(states)
    if n < 1:
        err_out(0)
else:
    err_out(0)

tmp = handle.readline()
if tmp[0:7] == "alpha=[" and tmp[-2] == ']':
    alpha = tmp[7:-2].split(',')
    if len(alpha) < 1:
        err_out(0)
else:
    err_out(0)

tmp = handle.readline()
if tmp[0:9] == "initial=[" and tmp[-2] == ']' and not (',' in tmp):
    init_st = tmp[9:-2]
    if init_st == '':
        err_out(4)  # E4: Initial state is not defined
    if not (init_st in states):
        err_out(1, init_st)  # E1: Initial state is not in the set of states
    init_index = states.index(init_st)
else:
    err_out(0)

tmp = handle.readline()
fin_index = []
if tmp[0:11] == "accepting=[" and tmp[-2] == ']':
    fin_st = tmp[11:-2].split(',')
    if fin_st[0] != '':
        for it in fin_st:
            fin_index.append(states.index(it))

    if len(fin_st) < 1:
        err_out(0)
else:
    err_out(0)

matrix = []
for i in range(len(states)):
    matrix.append([])
    for j in range(len(states)):
        matrix[i].append('{}')

tmp = handle.readline()
if tmp[0:7] == "trans=[" and tmp[-1] == ']':
    trans = (tmp[7:-1].split(','))
    complete = []
    for line in trans:
        state1 = line.split('>')[0]
        word = line.split('>')[1]
        state2 = line.split('>')[2]
        if [state1, word] in complete:
            err_out(5)  # E5: FSA is nondeterministic
        else:
            complete.append([state1, word])
        if len(state1) == 0 or len(state2) == 0 or len(word) == 0:
            err_out(0)
        if not (word in alpha):
            err_out(3, word)  # E3: A transition is not represented in the alphabet
        id1 = states.index(state1)
        id2 = states.index(state2)
        if matrix[id1][id2] == '{}':
            matrix[id1][id2] = word
        else:
            matrix[id1][id2] += '|' + word

else:
    err_out(0)

# E2 checking
complete = {}
for line in trans:
    state1 = line.split('>')[0]
    state2 = line.split('>')[2]
    try:
        temp = complete[state1]
        temp.append(state2)
        complete[state1] = temp
    except KeyError:
        complete[state1] = [state2]

list_of_states = []
for state in states:
    bfs(state)
    isConnected = True
    for item in marked:
        if not marked[item]:
            isConnected = False
    list_of_states.append(isConnected)
if not (True in list_of_states):
    err_out(2)  # E2: Some states are disjoint

R = []                         # initial state, -1 step
for i in range(n):
    R.append([])
    for j in range(n):
        tmp = matrix[i][j]
        if i == j:
            if tmp == '{}':
                tmp = 'eps'
            else:
                tmp += '|eps'
        R[i].append(tmp)

out.write(solve(R, matrix))






