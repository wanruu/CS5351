import numpy as np
np.seterr(divide='ignore',invalid='ignore')

"""
testcase: ([int]:每一行的覆盖次数, int: 运行是否正确)
testset: [testcase]
"""


def get_paras(testset):
    # Separate success/fail coverage according to label
    success_cov = np.array([cov for cov, label in testset if label == 1])  # [[int]]
    fail_cov = np.array([cov for cov, label in testset if label == 0])
    # print(success_cov.shape, fail_cov.shape)
    
    # Calculate 4 parameters
    line_num = len(testset[0][0]) # the number of lines in the code
    Ncf, Nuf, Ncs, Nus = [], [], [], []
    for line_idx in range(line_num):
        Ncf.append(np.sum(success_cov[:,line_idx]))
        Ncs.append(np.sum(fail_cov[:,line_idx]))
        Nuf.append(success_cov.shape[0] - Ncf[-1])
        Nus.append(fail_cov.shape[0] - Ncs[-1])
        # if line_idx == 1:
        #     print(success_cov[:,line_idx], fail_cov[:,line_idx])
        #     print(Ncf[-1], Nuf[-1], Ncs[-1], Nus[-1])

    return np.array(Ncf), np.array(Nuf), np.array(Ncs), np.array(Nus)



def dstar(testset):
    Ncf, Nuf, Ncs, _ = get_paras(testset)
    return (Ncf * Ncf) / (Ncs + Nuf)


def ochiai(testset):
    Ncf, Nuf, Ncs, _ = get_paras(testset)
    return Ncf / np.sqrt((Ncf + Nuf) * (Ncf + Ncs))


def barinel(testset):
    Ncf, _, Ncs, _ = get_paras(testset)
    return 1 - Ncs / (Ncs + Ncf)


if __name__ == "__main__":
    path = "../zzh-data/Code_Line_Corr/Experimental Data/"
    filename = "gzip-bug-2009-09-26-a1d3d4019d-f17cbd13a1/"
    with open(path+filename+"covMatrix.txt", encoding="utf-16") as f:
        cov = [[int(item) for item in line.split(" ") if item] for line in f.read().splitlines()]
    with open(path+filename+"error.txt") as f:
        label = [int(line) for line in f.read().splitlines()]
    n = min(len(cov), len(label))
    testset = [(cov[idx], label[idx]) for idx in range(n)]
    # print("dstar", dstar(testset))
    # print("ochiai", ochiai(testset))
    res = barinel(testset)
    print(res[109])
    # res = -np.sort(-res)
    # print("barinel", res)



