import subprocess
import numpy as np


def main():
    num_of_runs = 3
    max_threads = 8
    chunk_pow_2 = 8

    # init the arrays where the values are stroed
    individual_static_time = [[0.0 for _ in range(max_threads)] for _ in range(num_of_runs)]
    individual_dynamic_time = [[0.0 for _ in range(max_threads)] for _ in range(num_of_runs)]
    individual_guided_time = [[0.0 for _ in range(max_threads)] for _ in range(num_of_runs)]
    individual_random_dynamic_time = [[0.0 for _ in range(max_threads)] for _ in range(num_of_runs)]
    individual_chunk_size = [[[0.0 for _ in range(max_threads)]for _ in range(chunk_pow_2)] for _ in range(num_of_runs)]

    # aggrogated numbers
    static_time = [0 for _ in range(max_threads)]
    static_div = 0
    dynamic_time = [0 for _ in range(max_threads)]
    dynamic_div = 0
    guided_time = [0 for _ in range(max_threads)]
    guided_div = 0
    random_dynamic_time = [0 for _ in range(max_threads)]
    rand_dynamic_div = 0
    chunk_size_time = [[0.0 for _ in range(chunk_pow_2)] for _ in range(num_of_runs)]
    chunk_size_div = 0


    for i in range(num_of_runs):

        for j in range(max_threads):

            # generate file names
            # static
            stxt = "results/SDG/" + str(i) + "_thread-" + str(j + 1) + "s.txt"
            # dynamic
            dtxt = "results/SDG/" + str(i) + "_thread-" + str(j + 1) + "d.txt"
            # guided
            gtxt = "results/SDG/" + str(i) + "_thread-" + str(j + 1) + "g.txt"
            # random Dynamic
            rand = "results/ranD/" + str(i) + "_thread-" + str(j + 1) + "ranD.txt"
            # call perf stat
            # subprocess.call(["perf", "stat", "--per-core", "-a", "-o", stxt, "./static", str(j+1)])
            individual_static_time[i][j] = float(parsefile(stxt, 71, 0))
            # subprocess.call(["perf", "stat", "--per-core", "-a", "-o", dtxt, "./dynamic", str(j+1)])
            individual_dynamic_time[i][j] = float(parsefile(dtxt, 71, 0))
            # subprocess.call(["perf", "stat", "--per-core", "-a", "-o", gtxt, "./guided", str(j+1)])
            individual_guided_time[i][j] = float(parsefile(gtxt, 71, 0))
            # subprocess.call(["perf", "stat", "--per-core", "-a", "-o", rand, "./ran_dynamic", str(j+1)])
            individual_random_dynamic_time[i][j] = float(parsefile(rand, 71, 0))
            print()

            # chunksize
            for j in range(max_threads-1):
                for c in range(chunk_pow_2):
                    # non random
                    chunk = "results/chunk/" + str(i) + "_thread-" + str(j+1) + "_chunksize-" + str(c) + "C_D.txt"
                    # random
                    #chunkrand = "results/chunk/" + str(i) + "_thread-" + str(j+1) + "_chunksize-" + str(c) + "ranC_D.txt"
                    subprocess.call(["perf", "stat", "--per-core", "-a", "-o", chunk, "./chunk_dynamic", str(j+1), str(2 ** c)])
                    individual_chunk_size[i][j][c] = float(parsefile(chunk, 71, 0))
                    #subprocess.call(["perf", "stat", "--per-core", "-a", "-o", chunkrand, "./chunk_ran_dynamic", str(j+1), str(2 ** c)])
                    #parsefile(chunkrand, 71, 0)

            chunk_size_time = np.array(chunk_size_time) + np.array(chunk_size_time[i])
            static_time = np.array(static_time) + np.array(individual_static_time[i])
            dynamic_time = np.array(dynamic_time) + np.array(individual_dynamic_time[i])
            guided_time = np.array(guided_time) + np.array(individual_guided_time[i])
            random_dynamic_time = np.array(random_dynamic_time) + np.array(individual_random_dynamic_time[i])
        static_time = np.array(static_time) / 3
        dynamic_time = np.array(dynamic_time) / 3
        guided_time = np.array(guided_time) / 3
        random_dynamic_time = np.array(random_dynamic_time) / 3
        chunk_size_time = np.array(chunk_size_time) / 3
    print("static time per core:")
    print(static_time)
    print("dynamic time per core:")
    print(dynamic_time)
    print("guided time per core:")
    print(guided_time)
    print("random dynamic time per core:")
    print(random_dynamic_time)
    print("chunk size time per block size per core:")
    print(chunk_size_time)


def parsefile(filename, line_num, array_pos):
    with open(filename) as file:
        line = file.readline()
        # print(filename)
        cnt = 1
        while line:
            if cnt == (line_num):
                # return the substring in file
                print(line.split()[array_pos])
                return line.split()[array_pos]

            line = file.readline()
            cnt += 1


# def parseline():


main()
