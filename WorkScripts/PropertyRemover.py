fileIn = "D:\\Work\\Models\\Designer\\SE_Asia\\Reizky\\ImportPoro\\2018.08.16_RUN_HELP_grid.inc"

fileOut = "D:\\Work\\Models\\Designer\\SE_Asia\\Reizky\\ImportPoro\\2018.08.16_RUN_HELP_grid2.inc"

flag = True

with open(fileIn, "r") as fl:
    with open(fileOut, "a") as the_file:
        for line in fl:
            if "ACTNUM" in line:
                flag = False

            if flag is False and "/" in line:
                flag = True

            if flag is True:
                the_file.write(line)

print("Done")
