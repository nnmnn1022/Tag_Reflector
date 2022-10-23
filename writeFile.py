import pathlib, csv

def run(data, filename, dirpath = '') :
    # 경로가 주어지지 않으면 실행 파일과 같은 위치에 파일 저장하기
    if dirpath == '':
        dirPath = str(pathlib.Path.cwd()) + f'/{filename}.csv'
    else:
        dirPath = str(dirpath) + f'/{filename}.csv'

    with open(dirPath, 'w', encoding='utf-8-sig', newline='') as writeFile:
        try:
            csvWriter = csv.writer(writeFile)
            csvWriter.writerows(data)
        except Exception as e:
            print(e)

if __name__ == '__main__' :
    run()