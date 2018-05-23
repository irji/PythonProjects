import os
import sys

def main(param):

    files = os.listdir(os.getcwd())

    for fl in files:

        if fl.endswith(".data") or fl.endswith(".dat"):

            with open(fl) as file_in:
                text = file_in.read()

            text = text.replace("@REPLACE_SOMETHING@", param)

            with open(fl + "_upd", "w") as file_out:
                file_out.write(text)


if __name__ == '__main__':
#    main("it works!")
    main(sys.argv[1])
    pass
