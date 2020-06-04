import html
import re
import jieba
from pypinyin import pinyin

data_path = 'species.csv'

input_texts = []
input_reverse = []
target_texts = []
target_processed = []
pairs = []
with open(data_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        input_text, target_text = line.split('\t')

        input_text = re.sub(r'\([^)]*\)', '', input_text.strip())
        input_text = re.sub(r'subsp\. (\w)+', '', input_text)

        target_text = html.unescape(target_text)
        target_text = re.sub(r'\([^)]*\)', '', target_text.strip())

        if len(target_text) > 1 and not re.findall(r'[A-Za-z]', target_text):
            target_text_py = ' '.join([item for sublist in pinyin(target_text) for item in sublist])
            target_text_processed = ' '.join(jieba.cut(target_text, HMM=False))
            if [input_text, target_text_py] not in pairs:
                pairs.append([input_text, target_text_py])
                input_texts.append(input_text)
                target_texts.append(target_text)
                if ' ' in input_text:
                    names = input_text.split(' ')
                    input_reverse.append(' '.join(names[::-1]).strip())
                else:
                    input_reverse.append(input_text)
                target_processed.append(target_text_processed)

with open('input.txt', 'w') as i:
    i.write('\n'.join(input_texts))

with open('target.txt', 'w') as t:
    t.write('\n'.join(target_texts))

with open('input_reverse.txt', 'w') as r:
    r.write('\n'.join(input_reverse))

with open('target_processed.txt', 'w') as p:
    p.write('\n'.join(target_processed))
