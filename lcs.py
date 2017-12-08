H = 10010000007 ** 2
M = 100000000000000007 ** 2


def check_lists(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


def lcsn(s1, s2_list, n, h=H, m=M, isList=True):
    #    print('len s2_list', len(s2_list))

    hs = [h % m]
    for i in range(1, n):
        hs.append((hs[-1] * h) % m)
    if isList is False:
        s1 = [ord(e) for e in list(s1)]
        s2 = [ord(e) for e in list(s2_list)]
    th = 0
    s = dict()
    for i in range(n):
        th = (th + s1[i] * hs[n - i - 1]) % m
    for i in range(n, len(s1)):
        if th not in s:
            s[th] = i - n
        else:
            if check_lists(s1[s[th]:s[th] + n], s1[i - n:i]) is False:
                print('collision')
                print(s1[s[th]:s[th] + n])
                print(s1[i - n:i])
                raise
        th = ((th - (s1[i - n] * hs[-1]) % m + m) * h + hs[0] * s1[i]) % m
    # print(s1[len(s1) - n: len(s1)], th)
    if th not in s:
        s[th] = len(s1) - n
    else:
        if check_lists(s1[s[th]:s[th] + n], s1[len(s1) - n:len(s1)]) is False:
            print('collision0')
            print(s1[s[th]:s[th] + n])
            print(s1[len(s1) - n:len(s1)])
            raise

    res = []
    for j, s2 in enumerate(s2_list):
        if len(s2) < n:
            res.append(None)
            continue
        th = 0
        for i in range(n):
            th = (th + s2[i] * hs[n - i - 1]) % m
        for i in range(n, len(s2)):
            if th in s:
                if check_lists(s2[i - n: i], s1[s[th]:s[th] + n]) is False:
                    print('collision1')
                    print(s2[i - n: i])
                    print(s1[s[th]:s[th] + n])
                    raise
                res.append(s2[i - n: i])
                break
            th = ((th - (s2[i - n] * hs[-1]) % m + m) * h + hs[0] * s2[i]) % m
        if len(res) != (j + 1):
            if th in s:
                if check_lists(s2[len(s2) - n: len(s2)], s1[s[th]:s[th] + n]) is False:
                    print('collision2')
                    print(s[th])
                    print(s2)
                    print(s2[len(s2) - n: len(s2)])
                    print(s1[s[th]:s[th] + n])
                    print(check_lists(s2[len(s2) - n: len(s2)], s1[s[th]:s[th] + n]))
                    raise
                res.append(s2[len(s2) - n: len(s2)])
        if len(res) != (j + 1):
            res.append(None)
            #    print(len(s2_list), len(res))
    return res


def lcs(s1, s2, h=H, m=M, isList=True, isPrint=True):
    l = 0
    r = min(len(s1), len(s2))
    while (l < r):
        if isPrint is True:
            print(l, r)
        x = (l + r + 1) // 2
        if lcsn(s1, [s2], x, h=h, m=m, isList=isList)[0] is not None:
            l = x
        else:
            r = x - 1
    if l == 0:
        return ''
    else:
        if isPrint is True:
            print(l)
        return lcsn(s1, [s2], l, h=h, m=m, isList=True)[0]


def lcs_dict(s1, s2_dict, h=H, m=M, isList=True):
    res = dict()
    for e in s2_dict:
        res[e] = [0, '']
    s2_dict_cur = s2_dict.copy()
    x = 0
    while len(s2_dict_cur) > 0:
        x += 1
        print(x, len(s2_dict_cur))
        z = lcsn(s1, [e[1] for e in sorted(s2_dict_cur.items(), key=lambda x: x[0])], x, h=h, m=m, isList=isList)
        for i, e in enumerate(sorted(s2_dict_cur.items(), key=lambda x: x[0])):
            if z[i] is not None:
                res[e[0]][0] = x
                res[e[0]][1] = z[i]
            else:
                s2_dict_cur.pop(e[0])
    return res