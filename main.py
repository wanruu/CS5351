with open('test.py') as f:
    data=f.readlines()
Flist=[]
for line in data:
    if line[:3]=='def' and line[3]==' ':
        Flist.append(line.split('(')[0].split(' ')[1])
with open('result.py','w') as r:
    for line in data:
        r.writelines(line)
    r.writelines('\n')
    r.writelines('if __name__ == "__main__":\n')
    r.writelines('    from line_profiler import LineProfiler\n')
    r.writelines('    lp=LineProfiler()\n')
    for F in Flist:
        if F!='main':
            r.writelines('    lp.add_function('+F+')\n')
    r.writelines('    test_func=lp(main)\n')
    r.writelines('    test_func()\n')
    r.writelines('    stats=lp.get_stats()\n')
    r.writelines('    timing=stats.timings\n')
    r.writelines('    Llist=[]\n')
    r.writelines('    for stat in timing:\n')
    r.writelines('        lines=timing[stat]\n')
    r.writelines('        for line in lines:\n')
    r.writelines('            Llist.append(line[0])\n')
    r.writelines('    print(Llist)\n')
