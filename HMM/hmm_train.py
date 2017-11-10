# -*- coding:utf-8 -*-
import codecs
import jieba
from data_utils import DataProcess

origin_data_path = '../../data/HMM/origin_data'
probability_op = '../../data/HMM/probability'

dp = DataProcess(origin_data=origin_data_path, convert_data=False, probability_op=probability_op)

def cut(sentence, fp):

    probability = load_probability(fp)
    prob, pos_list = viterbi(sentence, ('B', 'M', 'E', 'S'), probability)
    return (prob, pos_list)


def viterbi(observe_seq, states, probability):
    v = [{}]
    path = {}
    start_p = probability[0]
    trans_p = probability[1]
    emit_p = probability[2]
    for y in states:
        v[0][y] = start_p[y] * emit_p[y].get(observe_seq[0], 0)
        path[y] = [y]
    for t in range(1, len(observe_seq)):
        v.append({})
        newpath = {}
        for y in states:
            (prob, state) = max(
                [(v[t - 1][y0] * trans_p[y0].get(y, 0) * emit_p[y].get(observe_seq[t], 0), y0) for y0 in states if
                 v[t - 1][y0] > 0])
            v[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath
    (prob, state) = max([(v[len(observe_seq) - 1][y], y) for y in states])
    return (prob, path[state])


def load_probability(fp):
    fp = codecs.open(fp, 'r')
    start_prob = {}
    trans_prob = {}
    emit_prob = {}
    count = -1
    for line in fp:
        count += 1
        if count == 1:
            start_prob = eval(line)
        if count == 2:
            trans_prob = eval(line)
        if count == 3:
            emit_prob = eval(line)

    return [start_prob, trans_prob, emit_prob]


def main():
    test_str = u'帮我约个生日晚上两点二十二分从林伟民塑像出发的滴滴专车'
    prob, pos_list = cut(test_str, probability_op)
    out_str = ''
    for i, j in zip(test_str, pos_list):
        if j == 'E':
            out_str += i + '##'
        if j == 'S':
            out_str += i + '##'
        if j == 'B':
            out_str += i
        if j == 'M':
            out_str += i
    print out_str
    for i, j in zip(out_str.split('##'), jieba.cut(test_str)):
        print i


if __name__ == '__main__':
    main()
