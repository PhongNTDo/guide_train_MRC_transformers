import json


def main(path_to_data, path_to_save):
    data = json.load(open(path_to_data))

    new_data = {'version': 'v1.0'}
    ds_data = []

    dem = 0
    for a in data['data']:
        for p in a['paragraphs']:
            for qa in p['qas']:
                id = qa['id']
                dem += 1
                answer_start, answer_text = [], []
                if True: # not qa['is_impossible']:
                    for an in qa['answers']:
                        answer_start.append(an['answer_start'])
                        answer_text.append(an['text'])
                ds_data.append({
                    "id": id,
                    "context": p['context'],
                    "question": qa['question'],
                    "answers": {'answer_start': answer_start, 'text': answer_text}})
    new_data["data"] = ds_data

    with open(path_to_save, 'w') as f:
        json.dump(new_data, f)


if __name__ == '__main__':
    path_to_data = 'path_to_data'
    path_to_save = 'path_to_save_data_with_new_format'
    main(path_to_data, path_to_save)
