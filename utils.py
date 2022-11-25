import re


def getTestCases(text: str):
    reti, reto = [], []
    oneCase = text.split('\n')
    for i in range(len(oneCase)):
        case = oneCase[i]
        I, O = [], []
        inputdata = True
        inputline, outputline = '', ''
        w = True
        for _ in range(len(case)):
            if case[_] == '[':
                inputdata = True
                w = True
                continue
            elif case[_] == '{':
                inputdata = False
                w = True
                continue
            elif case[_] in [']', '}']:
                w = False
            else:
                if w:
                    if inputdata:
                        inputline += case[_]
                    else:
                        outputline += case[_]
        # print(inputline, outputline)
        I = re.split('[ ,]', inputline)
        O = re.split('[ ,]', outputline)
        for _ in range(len(I)):
            if len(I[_]) > 0 and I[_] in '0123456789':
                I[_] = int(I[_])

        for _ in range(len(O)):
            if len(O[_]) > 0 and O[_] in '0123456789':
                O[_] = int(O[_])

        # print("ok", I, O)

        reti.append(I)
        reto.append(O)
    # print(reti, reto)
    return reti, reto
