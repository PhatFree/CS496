import subprocess 



def main():
    for i in range(3):
        for j in range(1,9):
            #generate file names
            #static
            stxt = "results/SDG/" + str(i) +"_thread-"+ str(j)  + "s.txt"
            #dynamic
            dtxt = "results/SDG/" + str(i) +"_thread-"+ str(j)  + "d.txt"
            #guided
            gtxt = "results/SDG/" + str(i) +"_thread-"+ str(j)  + "g.txt"
            #random Dynamic
            rand = "results/ranD/" + str(i) +"_thread-"+ str(j)  + "ranD.txt"

                        #call perf stat
#			subprocess.call(["perf", "stat", "--per-core", "-a", "-o", stxt, "./static", str(j)])
            parsefile(stxt)
#			subprocess.call(["perf", "stat", "--per-core", "-a", "-o", dtxt, "./dynamic", str(j)])
            parsefile(dtxt)
#			subprocess.call(["perf", "stat", "--per-core", "-a", "-o", gtxt, "./guided", str(j)])
            parsefile(gtxt)
#			subprocess.call(["perf", "stat", "--per-core", "-a", "-o", rand, "./ran_dynamic", str(j)])
            parsefile(rand)

            #chunksize
            for j in range (2,9):
                for c in  range (0,9):
                    #non random
                        chunk = "results/chunk/" + str(i) +"_thread-"+ str(j)+ "_cunksize-"+ str(c)  + "C_D.txt"
                        #random
                        chunkrand = "results/chunk/" + str(i) +"_thread-"+ str(j)+"_chunkszie-"+ str(c)+ "ranC_D.txt"
#			            subprocess.call(["perf", "stat", "--per-core", "-a", "-o", chunk, "./chunk_dynamic", str(j),str(2**c)])
                        parsefile(chunk)
#			            subprocess.call(["perf", "stat", "--per-core", "-a", "-o", chunkrand, "./chunk_ran_dynamic", str(j),str(2**c)])
                        parsefile(chunkrand)

def parsefile(filename):
    with open(filename) as file:
        line = file.readline()
        cnt = 1
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            line = file.readline()
            cnt += 1
#def parseline():



main()
