import json

if __name__ == '__main__':
    with open('data.txt', 'r', encoding='utf-8') as f:
        dt = f.read()
        dt = dt.split('#')
        items = []
        for i in dt[:-1]:
            items.append(json.loads(i))
    print(items)
