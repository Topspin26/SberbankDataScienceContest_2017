import os
import zlib
import common_zlib

def run_language_tool(df_all_questions, colname='question', suff='', pathToLanguageTool='LanguageTool-3.9'):
    if not os.path.exists('data/lt'):
        os.mkdir('data/lt')

    filename = 'data/lt/df_all_questions_checked' + suff + '.txt'
    common_zlib.from_zlib(filename)

    if os.path.exists(filename):
        rules = []
        for e in range(len(df_all_questions[colname])):
            rules.append([])
        last = 0
        kk = 0
        with open(filename, encoding='utf-8') as fin:
            for line in fin:
                if line.find('Line') != -1 and line.find('Rule ID:') != -1:
                    # print(line.strip(), int(line.split('Line ')[1].split(',')[0]), line.split('Rule ID: ')[1].strip())
                    cur = 5000 * kk + int(line.split('Line ')[1].split(',')[0]) - 1
                    if cur < last:
                        kk += 1
                        cur += 5000
                    rules[cur].append(line.split('Rule ID: ')[1].strip().replace('[', '(').replace(']', ')'))
                    last = cur
        print(len(rules))
        df_all_questions['lt' + suff] = [' '.join([r + suff for r in rules[i]]) for i in range(len(rules))]

        common_zlib.to_zlib(filename)

    else:
        with open(filename, 'w', encoding='utf-8') as fout:
            k = 0
            ik = 0
            fout0 = open(pathToLanguageTool + '/tmp.txt', 'w', encoding='utf-8')
            for e in df_all_questions[colname]:
                k += 1
                fout0.write(e + '\n')
                if k % 5000 == 0:
                    ik += 1
                    print(ik)
                    fout0.close()
                    os.system('java -Dfile.encoding=UTF-8 -jar {}/languagetool-commandline.jar -l ru {}/tmp.txt > {}/tmp_out.txt'.\
                              format(pathToLanguageTool, pathToLanguageTool, pathToLanguageTool))
                    with open(pathToLanguageTool + '/tmp_out.txt', encoding='utf-8') as fin:
                        for line in fin:
                            fout.write(line)
                    k = 0
                    fout0 = open(pathToLanguageTool + '/tmp.txt', 'w', encoding='utf-8')
            if k != 0:
                fout0.close()
                os.system('java -Dfile.encoding=UTF-8 -jar {}/languagetool-commandline.jar -l ru {}/tmp.txt > {}/tmp_out.txt'.\
                    format(pathToLanguageTool, pathToLanguageTool, pathToLanguageTool))
                with open(pathToLanguageTool + '/tmp_out.txt', encoding='utf-8') as fin:
                    for line in fin:
                        fout.write(line)

        common_zlib.rm_zlib(filename)

        run_language_tool(df_all_questions, colname=colname, suff=suff)
