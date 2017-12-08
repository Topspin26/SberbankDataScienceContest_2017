
class RanksFeatures:
    def __init__(self, paragraph_filename, question_filename, qp_sim_filename):
        self.paragraph_filename = paragraph_filename
        self.question_filename = question_filename
        self.qp_sim_filename = qp_sim_filename
        self.readData()
        self.readSim()

    def readData(self):
        self.pp = dict()
        self.pnum2p = dict()
        with open(self.paragraph_filename, encoding='utf-8') as fin:
            for line in fin:
                tokens = line.strip().split('\t')
                self.pp[int(tokens[0][1:])] = [tokens[1], tokens[2]]
                self.pnum2p[int(tokens[0][1:])] = tokens[1]

        self.qq = dict()
        self.qnum2q = dict()
        with open(self.question_filename, encoding='utf-8') as fin:
            for line in fin:
                tokens = line.strip().split('\t')
                self.qq[int(tokens[0][1:])] = [tokens[1], tokens[2]]
                self.qnum2q[int(tokens[0][1:])] = tokens[1]

    def readSim(self):
        self.rows = []
        self.cols = []
        self.vals = []
        self.p2q = dict()
        self.q2p = dict()
        with open(self.qp_sim_filename, encoding='utf-8') as fin:
            for line in fin:
                tokens = line.strip().split('\t')
                pn = int(tokens[0][1:])
                qn = int(tokens[1][1:])
                self.rows.append(pn)
                self.cols.append(qn)
                self.vals.append(float(tokens[2]))
                if pn not in self.p2q:
                    self.p2q[pn] = []
                self.p2q[pn].append([qn, float(tokens[2])])
                if qn not in self.q2p:
                    self.q2p[qn] = []
                self.q2p[qn].append([pn, float(tokens[2])])

    def buildRankFeatures(self):
        self.max_psim = dict()
        self.max2_psim = dict()
        self.max5_psim = dict()
        self.max10_psim = dict()
        self.max20_psim = dict()
        self.qrank_for_p = dict()
        self.min_qrank = dict()
        for pn in self.p2q:
            zz = sorted(self.p2q[pn], key=lambda x: -x[1])
            self.max_psim[self.pnum2p[pn]] = zz[0][1]
            self.max5_psim[self.pnum2p[pn]] = zz[1][1]
            self.max2_psim[self.pnum2p[pn]] = zz[4][1]
            self.max10_psim[self.pnum2p[pn]] = zz[9][1]
            self.max20_psim[self.pnum2p[pn]] = zz[19][1]
            for i in range(len(zz)):
                self.qrank_for_p[self.pnum2p[pn] + '\t' + self.qnum2q[zz[i][0]]] = i + 1
                if self.qnum2q[zz[i][0]] not in self.min_qrank:
                    self.min_qrank[self.qnum2q[zz[i][0]]] = i + 1
                else:
                    self.min_qrank[self.qnum2q[zz[i][0]]] = min(self.min_qrank[self.qnum2q[zz[i][0]]], i + 1)

        self.max_qsim = dict()
        self.max2_qsim = dict()
        self.max5_qsim = dict()
        self.max10_qsim = dict()
        self.max20_qsim = dict()
        self.len_qsim = dict()
        self.e_qsim = dict()
        self.disp_qsim = dict()
        self.prank_for_q = dict()
        for qn in self.q2p:
            zz = sorted(self.q2p[qn], key=lambda x: -x[1])
            self.max_qsim[self.qnum2q[qn]] = zz[0][1]
            self.max2_qsim[self.qnum2q[qn]] = zz[1][1] if len(zz) >= 2 else 0
            self.max5_qsim[self.qnum2q[qn]] = zz[4][1] if len(zz) >= 5 else 0
            self.max10_qsim[self.qnum2q[qn]] = zz[9][1] if len(zz) >= 10 else 0
            self.max20_qsim[self.qnum2q[qn]] = zz[19][1] if len(zz) >= 20 else 0
            self.len_qsim[self.qnum2q[qn]] = len(zz)
            self.e_qsim[self.qnum2q[qn]] = 0
            for i in range(len(zz)):
                self.prank_for_q[self.pnum2p[zz[i][0]] + '\t' + self.qnum2q[qn]] = i + 1
                self.e_qsim[self.qnum2q[qn]] += zz[i][1] / len(zz)
            self.disp_qsim[self.qnum2q[qn]] = 0
            for i in range(len(zz)):
                self.disp_qsim[self.qnum2q[qn]] += (zz[i][1] - self.e_qsim[self.qnum2q[qn]])**2 / len(zz)

        self.qrank1_for_p = dict()
        for pn in self.p2q:
            zz = sorted(self.p2q[pn], key=lambda x: -x[1])
            k = 0
            for i in range(len(zz)):
                self.qrank1_for_p[self.pnum2p[pn] + '\t' + self.qnum2q[zz[i][0]]] = k + 1
                if self.prank_for_q[self.pnum2p[pn] + '\t' + self.qnum2q[zz[i][0]]] == 1:
                    k += 1


