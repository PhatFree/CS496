import subprocess
import numpy as np


def main():
    np.set_printoptions(precision=5)
    #try:
    #  state = input("please input a 1 to run the tests, leave blank just to analyze")

    #except:
    #    print("1 not provided, analyzing only")
    state = 0
    num_of_runs = 3
    max_threads = 8
    chunk_pow_2 = 8

    # init the arrays where the values are stroed
    individual_static_time = np.zeros([num_of_runs,max_threads])
    individual_dynamic_time = np.zeros([num_of_runs,max_threads])
    individual_guided_time = np.zeros([num_of_runs,max_threads])
    individual_random_dynamic_time = np.zeros([num_of_runs,max_threads])
    individual_chunk_size = np.zeros([num_of_runs,chunk_pow_2,max_threads])
    dynamic_num_instrcuts = np.zeros([num_of_runs,max_threads,max_threads])
    chunk_num_instrcuts = np.zeros([num_of_runs,chunk_pow_2,max_threads])


    # aggrogated numbers
    static_time = np.zeros([max_threads])
    dynamic_time = np.zeros([max_threads])
    guided_time = np.zeros([max_threads])
    random_dynamic_time = np.zeros([max_threads])


    chunk_size_div = 0

    for i in range(num_of_runs):
        #do our scheduler math
        for j in range(1, (max_threads + 1)):
            # generate file names
            # static
            stxt = "results/SDG/" + str(i) + "_thread-" + str(j) + "s.txt"
            # dynamic
            dtxt = "results/SDG/" + str(i) + "_thread-" + str(j) + "d.txt"
            # guided
            gtxt = "results/SDG/" + str(i) + "_thread-" + str(j) + "g.txt"
            # random Dynamic
            rand = "results/ranD/" + str(i) + "_thread-" + str(j) + "ranD.txt"
            # call perf stat
            if state == 1:
                subprocess.call(["perf", "stat", "--per-core", "-a", "-o", stxt, "./static", str(j)])
            individual_static_time[i][(j - 1)] = float(parsefile(stxt, 71, 0))
            if state == 1:
                subprocess.call(["perf", "stat", "--per-core", "-a", "-o", dtxt, "./dynamic", str(j)])
            individual_dynamic_time[i][(j - 1)] = float(parsefile(dtxt, 71, 0))
            dynamic_num_instrcuts[i][j - 1][0] = int(parsefile(dtxt,11,2).replace(',',''))
            dynamic_num_instrcuts[i][j - 1][1] = int(parsefile(dtxt,19,2).replace(',',''))
            dynamic_num_instrcuts[i][j - 1][2] = int(parsefile(dtxt,27,2).replace(',',''))
            dynamic_num_instrcuts[i][j - 1][3] = int(parsefile(dtxt,35,2).replace(',',''))
            dynamic_num_instrcuts[i][j - 1][4] = int(parsefile(dtxt,43,2).replace(',',''))
            dynamic_num_instrcuts[i][j - 1][5] = int(parsefile(dtxt,51,2).replace(',',''))
            dynamic_num_instrcuts[i][j - 1][6] = int(parsefile(dtxt,59,2).replace(',',''))
            dynamic_num_instrcuts[i][j - 1][7] = int(parsefile(dtxt,67,2).replace(',',''))


            if state == 1:
                subprocess.call(["perf", "stat", "--per-core", "-a", "-o", gtxt, "./guided", str(j)])
            individual_guided_time[i][(j - 1)] = float(parsefile(gtxt, 71, 0))
            if state == 1:
                subprocess.call(["perf", "stat", "--per-core", "-a", "-o", rand, "./ran_dynamic", str(j)])
            individual_random_dynamic_time[i][(j - 1)] = float(parsefile(rand, 71, 0))


        # chunksize
        for j in range(1, (max_threads + 1)):
            for c in range(chunk_pow_2):
                # non random
                chunk = "results/chunk/" + str(i) + "_thread-" + str(j) + "_chunksize-" + str(c) + "C_D.txt"
                # random
                # chunkrand = "results/chunk/" + str(i) + "_thread-" + str(j+1) + "_chunksize-" + str(c) + "ranC_D.txt"
                if state == 1:
                    subprocess.call(["perf", "stat", "--per-core", "-a", "-o", chunk, "./chunk_dynamic", str(j), str(2 ** c)])
                individual_chunk_size[i][j - 1][c] = float(parsefile(chunk, 71, 0))
                if j == 8:
                    chunk_num_instrcuts[i][c][0] = int(parsefile(chunk, 11, 2).replace(',', ''))
                    chunk_num_instrcuts[i][c][1] = int(parsefile(chunk, 19, 2).replace(',', ''))
                    chunk_num_instrcuts[i][c][2] = int(parsefile(chunk, 27, 2).replace(',', ''))
                    chunk_num_instrcuts[i][c][3] = int(parsefile(chunk, 35, 2).replace(',', ''))
                    chunk_num_instrcuts[i][c][4] = int(parsefile(chunk, 43, 2).replace(',', ''))
                    chunk_num_instrcuts[i][c][5] = int(parsefile(chunk, 51, 2).replace(',', ''))
                    chunk_num_instrcuts[i][c][6] = int(parsefile(chunk, 59, 2).replace(',', ''))
                    chunk_num_instrcuts[i][c][7] = int(parsefile(chunk, 67, 2).replace(',', ''))
            # subprocess.call(["perf", "stat", "--per-core", "-a", "-o", chunkrand, "./chunk_ran_dynamic", str(j+1), str(2 ** c)])
            # parsefile(chunkrand, 71, 0)

    chunk_size_time = np.mean(individual_chunk_size,axis=0)
    chunk_size_div = np.std(individual_chunk_size, axis=0)

    chunk_size_num_instrcuts_avg = np.mean(chunk_num_instrcuts,axis=0)
    dynamic_num_instrcuts_avg = np.mean(dynamic_num_instrcuts,axis=0)
    #dynamic_num_instrcuts_div = np.std(dynamic_num_instrcuts,axis=0)

    static_time = np.mean(individual_static_time,axis=0)
    dynamic_time = np.mean(individual_dynamic_time,axis=0)
    guided_time = np.mean(individual_guided_time,axis=0)
    random_dynamic_time = np.mean(individual_random_dynamic_time,axis=0)

    static_time_div  = np.std( individual_static_time,  axis=0)
    dynamic_time_div = np.std( individual_dynamic_time, axis=0)
    guided_time_div  = np.std( individual_guided_time,  axis=0)

    #print("static time per core:")
    #print(static_time)
    #print("dynamic time per core:")
    #print(dynamic_time)
    #print("guided time per core:")
    #print(guided_time)
    #print("random dynamic time per core:")
    #print(random_dynamic_time)
    print("chunk size time per block size per core:")
    print(chunk_size_time)
    time = np.column_stack((static_time,dynamic_time,guided_time,random_dynamic_time))
    div = np.column_stack((static_time_div,dynamic_time_div,guided_time_div))
    print ("static, dynamic, guided, random dynamic")
    print(time)

    print("Min static div:", static_time_div.min())
    print("Min dynamic div:", dynamic_time_div.min())
    print("Min guided div:", guided_time_div.min())
    print("Min of all div:", div.min())

    print( "Max static div:", static_time_div.max())
    print( "Max dynamic div:", dynamic_time_div.max())
    print( "Max guided div:", guided_time_div.max())
    print( "Max of all div:", div.max())

    print("avg static div:", static_time_div.mean())
    print("avg dynamic div:", dynamic_time_div.mean())
    print("avg guided div:", guided_time_div.mean())
    print("avg of all div:", div.mean())

   # print(chunk_size_div)
    print ("Min chunk size Div:", chunk_size_div.min())
    print ("Max chunk size Div:",chunk_size_div.max())
    print( "avg chunk size Div:",chunk_size_div.mean())
    #print (dynamic_num_instrcuts_div)

    np.savetxt("results/SDG/static_dynamic_guided.csv", time, delimiter=",")
    np.savetxt("results/SDG/dynamic_instruct.csv", dynamic_num_instrcuts_avg, delimiter=",")
    np.savetxt("results/chunk/chunksize.csv", chunk_size_time, delimiter=",")
    np.savetxt("results/chunk/chunk_instruct.csv",chunk_num_instrcuts[0],delimiter=",")





def parsefile(filename, line_num, array_pos):
    with open(filename) as file:
        line = file.readline()
        # print(filename)
        cnt = 1
        while line:
            if cnt == (line_num):
                # return the substring in file
                #print(line.split()[array_pos])
                return line.split()[array_pos]

            line = file.readline()
            cnt += 1

main()
