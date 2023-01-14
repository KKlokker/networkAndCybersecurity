import math

def tcpDatasegments(datasegments,fails, windowSize=1):
    print("\\begin{tikzpicture}[>=stealth',font=\small\sffamily]")
    timing = 1
    print("\\tramaok{\\color{purple}SYN}{(0," + str(-round(timing,2)) + ")}")
    timing += 1
    print("\\ackok{\\color{teal}SYN ACK}{(4," + str(-round(timing,2)) + ")}")
    timing += 1
    i = 0
    while i < (datasegments):
        startTimeout = False
        ackFail = False
        nextTarget = i+windowSize
        for w in range(min(datasegments - i, windowSize)):
            if ('d' + str(i+w)) in fails:
                if not startTimeout and not ackFail:
                    nextTarget = i+w
                startTimeout = True
                print("\\tramaperduda{\\color{purple}d" + str(i+w)+"}{(0," + str(-round(timing,2)) + ")}")
            else:
                print("\\tramaok{\\color{purple} d" + str(i+w)+"}{(0," + str(-round(timing,2)) + ")}")
            timing += 1.35
            ackNumber = i+w+1
            if startTimeout:
                ackNumber = nextTarget
            if ('d' + str(i+w)) not in fails:
                if ('a' + str(i+w)) in fails:
                    print("\\ackperdut{\\color{teal} ack d" + str(ackNumber)+"}{(4," + str(-round(timing,2)) + ")}")
                    fails.remove('a'+str(i+w))
                    if not startTimeout and not ackFail:
                        nextTarget = i+w
                    startTimeout = True
                else:
                    print("\\ackok{\\color{teal} ack d" + str(ackNumber)+"}{(4," + str(-round(timing,2)) + ")}")
            else:
                fails.remove('d'+str(i+w))
            if windowSize > 1:
                timing -= 0.5

        timing += 1.35
        i = nextTarget
        if startTimeout:
            offset = 0
            if windowSize == 1:
                offset +=0.5
            print("\\timeout{(-0.5," + str(-round(timing,2)+2.15+offset) + ")}{(-0.5," + str(-round(timing,2)) +")}")
    timing += 0.5
    print("\\tramaok{\\color{purple}FIN}{(0," + str(-round(timing,2)) + ")}")
    timing += 1
    print("\\ackok{\\color{teal}ACK}{(4," + str(-round(timing,2)) + ")}")
    timing += 0.5
    print("\\ackok{\\color{teal}FIN}{(4," + str(-round(timing,2)) + ")}")
    timing += 1
    print("\\tramaok{\\color{purple}ACK}{(0," + str(-round(timing,2)) + ")}")
    timing += 2
    print("\draw[help lines,->] (4,0) node[host] {B}--(4," + str(-round(timing,2)) + ");")
    print("\draw[help lines,->] (0,0) node[host] {A}--(0," + str(-round(timing,2)) + ");")
    print("\\end{tikzpicture}")

def tcpPacakge(fileSize,MTU,fails, windowSize=1, metaPacakgeSize=20):
    print("\\begin{tikzpicture}[>=stealth',font=\small\sffamily]")
    timing = 1
    print("\\tramaok{\\color{purple}SYN " + str(metaPacakgeSize) + " bit}{(0," + str(-round(timing,2)) + ")}")
    timing += 1
    print("\\ackok{\\color{teal}SYN ACK" + str(metaPacakgeSize+1 )+ "}{(4," + str(-round(timing,2)) + ")}")
    timing += 1
    i = metaPacakgeSize*2
    numberOfPackages = 0
    while i < (fileSize+metaPacakgeSize*2):
        startTimeout = False
        ackFail = False
        nextTarget = i+windowSize*MTU
        for w in range(min(math.ceil((fileSize - i) / MTU), windowSize)):
            #print((fileSize - i) / MTU, windowSize)
            seqNumber = i+w*MTU
            segmentSize = min((fileSize - seqNumber), MTU)
            if ('d' + str(numberOfPackages)) in fails:
                if not startTimeout:
                    nextTarget = i+w*MTU
                startTimeout = True
                print("\\tramaperduda{\\color{purple}seg" + str(seqNumber)+" size " + str(segmentSize) +"}{(0," + str(-round(timing,2)) + ")}")
            else:
                print("\\tramaok{\\color{purple} seg" + str(seqNumber)+" size " + str(segmentSize) +"}{(0," + str(-round(timing,2)) + ")}")
            timing += 1.35
            if ('d' + str(numberOfPackages)) not in fails:
                if not startTimeout or ackFail:
                    ackNumber = seqNumber+1+segmentSize
                if ('a' + str(numberOfPackages)) in fails:
                    print("\\ackperdut{\\color{teal} ack d" + str(ackNumber)+" " + str(metaPacakgeSize) + "bit }{(4," + str(-round(timing,2)) + ")}")
                    fails.remove('a'+str(numberOfPackages))
                    if not startTimeout and w == min((fileSize - i) % MTU, windowSize)-1:
                        nextTarget = seqNumber
                    startTimeout = True
                    ackFail = True
                else:
                    print("\\ackok{\\color{teal} ack d" + str(ackNumber)+" " + str(metaPacakgeSize) + "bit }{(4," + str(-round(timing,2)) + ")}")
            else:
                fails.remove('d'+str(numberOfPackages))
            if windowSize > 1:
                timing -= 0.5
        numberOfPackages += 1

        timing += 1.35
        i = nextTarget
        if startTimeout:
            offset = 0
            if windowSize == 1:
                offset +=0.5
            print("\\timeout{(-0.5," + str(-round(timing,2)+2.15+offset) + ")}{(-0.5," + str(-round(timing,2)) +")}")
    timing += 0.5
    print("\\tramaok{\\color{purple}FIN" + str(metaPacakgeSize) + "}{(0," + str(-round(timing,2)) + ")}")
    timing += 1
    print("\\ackok{\\color{teal}ACK" + str(metaPacakgeSize) + "}{(4," + str(-round(timing,2)) + ")}")
    timing += 0.5
    print("\\ackok{\\color{teal}FIN" + str(metaPacakgeSize) + "}{(4," + str(-round(timing,2)) + ")}")
    timing += 1
    print("\\tramaok{\\color{purple}ACK" + str(metaPacakgeSize) + "}{(0," + str(-round(timing,2)) + ")}")
    timing += 2
    print("\draw[help lines,->] (4,0) node[host] {B}--(4," + str(-round(timing,2)) + ");")
    print("\draw[help lines,->] (0,0) node[host] {A}--(0," + str(-round(timing,2)) + ");")
    print("\\end{tikzpicture}")

#tcpPacakge(2000,250,['d1','a2'],3)        
tcpDatasegments(4, ["d1","a2"],3)