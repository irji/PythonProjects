import os


def ReadFile(fl, dr):
    ar1 = []  # создаем пустой список

    print("Файл: " + fl)

    with open(dr + fl) as f:
        ar2 = {}  # создаем пустой словарь
        lines = f.read().splitlines()

        min = 100000000000000000000
        max = 0

        date='01.01.1900'

        for ln in lines:
            if 'Time' not in ln:
                s = ln.split(',')

                if s[1] != date:
                    date = s[1]
                    print('{0} Min={1} Max={2}'.format(date, min, max))
                    min = 100000000000000000000
                    max = 0

                if float(s[3]) > max:
                    max = float(s[3])

                if float(s[3]) < min:
                    min = float(s[3])


def main():
    dirs = "D:/Programs/VM/Public/Extractor/Data/"
    files = "SIZ7@FORTS.txt"

    ReadFile(files, dirs)

    print("Done!")


if __name__ == '__main__':
    main()
    pass