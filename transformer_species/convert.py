import html
import re
from pypinyin import pinyin, Style

data_path = 'species.csv'

input_texts = []
input_reverse = []
target_texts = []
target_py = []
with open(data_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        input_text, target_text = line.split('\t')
        target_text = re.sub(r'\([^)]*\)', '', target_text.strip())
        if target_text != '':
            input_text = re.sub(r'\([^)]*\)', '', input_text.strip())
            input_text = re.sub(r'subsp\. (\w)+', '', input_text)
            input_texts.append(input_text.strip())
            target_text = html.unescape(target_text)
            target_texts.append(target_text)
            target_py.append(' '.join([item for sublist in pinyin(target_text) for item in sublist]))
            if ' ' in input_text:
                names = input_text.split(' ')
                input_reverse.append(' '.join(names[::-1]).strip())
            else:
                input_reverse.append(input_text)

with open('input.txt', 'w') as i:
    i.write('\n'.join(input_texts))

with open('target.txt', 'w') as t:
    t.write('\n'.join(target_texts))

with open('input_reverse.txt', 'w') as r:
    r.write('\n'.join(input_reverse))

with open('target_py.txt', 'w') as p:
    p.write('\n'.join(target_py))
