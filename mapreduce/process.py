import sys
import re
import numpy as np

sys.path.append('../')
import similarity


def process(p, pn, qs, qsn, idfs_questions, idfs_paragraphs):
    paragraphs = similarity.splitParagraphsWindow(p)
    s_p, _, _ = similarity.prepare_paragraph(p, similarity.stop_words_sim2, False)
    qs_filtered = []
    qsn_filtered = []
    for i in range(len(qs)):
        t_q = [e.lower().replace('ё', 'е') for e in re.findall("\w+", qs[i], re.UNICODE)]
        s_q = set(t_q)
        if len(s_q & s_p - set(similarity.stop_words_nltk)) > 0:
            qs_filtered.append(qs[i])
            qsn_filtered.append(qsn[i])

    sys.stderr.write(str(len(paragraphs)) + ' ' + str(len(qs_filtered)) + '\n')
    sim = np.array(similarity.calcSim1_list(qs_filtered, p, similarity.stop_words_sim2, idfs_questions, idfs_paragraphs,
                                            isCut=False))

    qs_filtered2 = []
    qsn_filtered2 = []
    for i in np.argsort(sim)[::-1][:min(250, len(sim))]:
        qs_filtered2.append(qs_filtered[i])
        qsn_filtered2.append(qsn_filtered[i])

    sim = np.zeros(len(qs_filtered2))
    for i, paragraph in enumerate(paragraphs):
        sys.stderr.write(str(i) + ' ')
        sys.stderr.flush()
        tsim = similarity.calcSim1_list(qs_filtered2, paragraph, similarity.stop_words_sim2, idfs_questions,
                                        idfs_paragraphs, isCut=False)
        sim = np.maximum(sim, tsim)
    sys.stderr.write('\n')
    out = []
    for i in np.argsort(sim)[::-1][:min(250, len(sim))]:
        out.append(pn + '\t' + qsn_filtered2[i] + '\t' + str(sim[i]) + '\n')
        #sys.stdout.write(pn + '\t' + qsn_filtered2[i] + '\t' + str(sim[i]) + '\n')
    return out
