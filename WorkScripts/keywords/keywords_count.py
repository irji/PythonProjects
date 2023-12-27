def KeywordsCount (input_file):
    #res_file = open(keywordOpen + ".txt", 'w')
    model_count = 0
    keywords_stat = {}
    keyword_name = ""

    sim_names = ["E100", "E300", "GEM", "IMEX", "IN", "MORE", "NEXUS", "STARS"]

    sim_name = input_file.split(".")[1]

    with open(input_file, "r") as fl:
        for line in fl:

            if line.__contains__("models") != True and line != "\n":
                #print("{} {}".format(line.rstrip(), model_count))
                keyword_name = line.rstrip()
                model_count = 0

            if line.__contains__("models") == True:
                model_count = model_count + 1

            if line == "\n":
                print("{} {} {}".format(sim_name, keyword_name, model_count))


def main():
    fileIn = "kw_to_models.STARS.txt"

    KeywordsCount(fileIn)

if __name__ == '__main__':
    main()
    pass