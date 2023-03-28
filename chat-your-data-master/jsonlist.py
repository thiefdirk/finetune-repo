import os
import pandas as pd

def merge_files():
    path = 'C:/work/repo-20230321/finetune-repo/chat-your-data-master/input'
    file_list = os.listdir(path)
    print(file_list)

    all_contents = []

    for file in file_list:
        if file.endswith('.json'):
            with open(path + '/' + file, 'r', encoding='utf-8') as f:
                content = f.read()
                content_single_line = content.replace('\n', '')
                all_contents.append(content_single_line)

    df = pd.DataFrame(all_contents)
    df.to_csv(path + '/all_files_merged.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    merge_files()
