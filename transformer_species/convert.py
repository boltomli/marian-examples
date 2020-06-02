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
            target_texts.append(html.unescape(target_text))
            if ' ' in input_text:
                names = input_text.split(' ')
                if len(names) == 2:
                    input_reverse.append(' '.join(names[::-1]).strip())
                    target_py.append(' '.join([item for sublist in pinyin(target_text.strip()) for item in sublist]))

with open('input.txt', 'w') as i:
    i.write('\n'.join(input_texts))

with open('target.txt', 'w') as t:
    t.write('\n'.join(target_texts))

with open('input_reverse.txt', 'w') as r:
    r.write('\n'.join(input_reverse))

with open('target_py.txt', 'w') as p:
    p.write('\n'.join(target_py))
