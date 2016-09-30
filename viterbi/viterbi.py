import sys

def extractSystemInfo(content):
    b = []
    a = []
    #extract states
    states = content[0].split()
    obsers = dict([value, it] for it,value in enumerate(content[1].split()))

    numStates = len(states)

    #extract b matrix
    for i in range(2, numStates+2):
        b.append([float(val) for val in content[i].split()])

    #extract a matrix
    for j in range(i+1, i+1+numStates+2):
        a.append([float(val) for val in content[j].split()])
    return b,a, states, obsers

def printTrace(backTrac, end, seqLen, states, result):
    result.append(states[end])
    for i in range(seqLen-1, 0, -1):
        result.insert(0, states[backTrac[i][end]])
        end = backTrac[i][end]
    return result

def viterbi(b, a, testingSeq, states, obsers, use_endTransition):
    num_sts = len(states)
    seqLen = len(testingSeq)
    viterb = []
    backTrac = []
    #initialization
    backTrac.append([])
    viterb.append([])
    for i in range(0, num_sts):
        viterb[0].append(a[0][i+1] * b[i][obsers[testingSeq[0]]])
        backTrac[0].append(-1)

    #recursion
    for ob in range(1, seqLen):
        viterb.append([])
        backTrac.append([])
        for state in range(0, num_sts):
            allIncoming = [viterb[ob-1][k] * a[k+1][state+1] * b[state][obsers[testingSeq[ob]]] for k in range(num_sts)]
            maxVal = max(allIncoming)
            viterb[ob].append(maxVal)
            backTrac[ob].append(allIncoming.index(maxVal))

    #termination
    if use_endTransition:
        allOutgoing = [viterb[ob][k] * a[k+1][num_sts+1] for k in range(num_sts)] #using the end state transition
    else:
        allOutgoing = [viterb[ob][k] for k in range(num_sts)] #not using the end state transition
    
    maxFinal = max(allOutgoing)
    maxFinalIndex = allOutgoing.index(maxFinal)
    
    result = []
    result = printTrace(backTrac, maxFinalIndex, seqLen, states, result)
    
    print (("Most probable state sequence for the given observation sequence is {}").format(result))
    return


with open(sys.argv[1]) as f:
    lines = [line for line in f.readlines() if line[0] != '#'] #collecing all lines excluding the comments

(b,a, states, obsers) = extractSystemInfo(lines)

testingSeq = [i for i in str(sys.argv[2])]
viterbi(b, a, testingSeq, states, obsers, 'false') #change the last argument to true if the transition probability of the all_states -> end state is non zero 
