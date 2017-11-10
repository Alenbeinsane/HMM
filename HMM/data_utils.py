# -*- coding:utf-8 -*-
import sys
import codecs


class DataProcess(object):
    def __init__(self, origin_data=None, convert_data=False, probability_op=None):

        start_dic = {}
        count_dic = {}
        trans_dic = {}
        emit_dic = {}
        state_list = ['B', 'M', 'E', 'S']
        for state in state_list:
            start_dic[state] = 0.0
            count_dic[state] = 0
            emit_dic[state] = {}
            trans_dic[state] = {}
            for state_T in state_list:
                trans_dic[state][state_T] = 0.0

        if convert_data:
            self.convert_origin_data(origin_data,
                                     start_dic, count_dic, trans_dic, emit_dic,
                                     probability_op)

    def convert_origin_data(self, fp, start_dic, count_dic, trans_dic, emit_dic, probability_op):
        """
        :param fp: origin data file path
        :param start_dic: 初始计数
        :param count_dic: 计数
        :param trans_dic: 转移计数
        :param emit_dic: 发射计数
        :param probability_op: 初始概率（隐状态）,转移概率（隐状态）,发射概率（隐状态表现为显状态的概率）
        :return:
        """
        char_set = set()
        count = -1
        fp = codecs.open(fp, 'r', encoding='utf8')
        for line in fp:
            count += 1
            line = line.strip()
            if not line:
                continue
            char_list = []
            for char in line:
                if char == ' ':
                    continue
                char_list.append(char)

            char_set = char_set | set(char_list)

            words = line.split(' ')
            line_state = []
            for word in words:
                line_state.extend(self.str2tag(word))
            if len(char_list) != len(line_state):
                print(count, line.encode("utf8", "ignore"))
            else:
                for i in range(len(line_state)):
                    if i == 0:
                        # Pi_dic记录句子第一个字的状态，用于计算初始状态概率
                        start_dic[line_state[0]] += 1
                        count_dic[line_state[0]] += 1
                    else:
                        trans_dic[line_state[i-1]][line_state[i]] += 1
                        count_dic[line_state[i]] += 1
                        if char_list[i] not in emit_dic[line_state[i]]:
                            emit_dic[line_state[i]][char_list[i]] = 0.0
                        else:
                            emit_dic[line_state[i]][char_list[i]] += 1
        probability = codecs.open(probability_op, 'w', encoding='utf8')
        probability.write('total_unique_chars: ' + str(len(char_set)) + '\n')
        for key in start_dic:
            start_dic[key] = start_dic[key] * 1.0 / count
        print >> probability, start_dic
        for key in trans_dic:
            for key_T in trans_dic[key]:
                trans_dic[key][key_T] = trans_dic[key][key_T] / count_dic[key]
        print >>probability, trans_dic
        for key in emit_dic:
            for char in emit_dic[key]:
                emit_dic[key][char] = emit_dic[key][char] / count_dic[key]
        print >> probability, emit_dic
        probability.close()
        fp.close()

    @staticmethod
    def str2tag(input_str):
        """
        convert a string to a tag sequence
        A --> 'S'
        AB --> 'BE'
        ABC --> 'BME'
        :param input_str:
        :return: output_str
        """
        output_str = []
        if len(input_str) == 1:
            output_str = ['S']
        elif len(input_str) == 2:
            output_str = ['B', 'E']
        else:
            middle_num = len(input_str) - 2
            middle_list = ['M'] * middle_num
            output_str.append('B')
            output_str.extend(middle_list)
            output_str.append('E')
        return output_str


