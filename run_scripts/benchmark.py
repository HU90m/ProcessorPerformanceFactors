import shutil
import subprocess
import csv
from multiprocessing import Process

def execute_cmd(
    arch="ARM",
    sim="gem5/configs/example/se.py",
    f="mibench/telecomm/CRC32/crc_arm",
    args="mibench/telecomm/adpcm/data/large.pcm",
    outdir="m5out",
    oth=[]
):
    cmd = [
        f"./gem5/build/{arch}/gem5.opt",
        "-d", outdir,
        sim
    ] + oth + [
        "-c", f,
        "-o", args
    ]

    if subprocess.call(cmd, stdout=subprocess.DEVNULL,  stderr=subprocess.DEVNULL) != 0:
        raise Exception("Error executing command")

    stats = open(outdir + "/stats.txt").read()
    shutil.rmtree(outdir)

    return stats

def execute_crc(arch="ARM", oth=[]):
    return execute_cmd(
        arch=arch,
        f=f"mibench/telecomm/CRC32/crc_{arch.lower()}",
        args="mibench/telecomm/adpcm/data/large.pcm",
        oth=oth,
        outdir=f"out_crc_{arch.lower()}"
    )

def execute_susan(arch="ARM", oth=[]):
    return execute_cmd(
        arch=arch,
        f=f"mibench/automotive/susan/susan_{arch.lower()}",
        args="mibench/automotive/susan/input_large.pgm output_large.smoothing.pgm -s",
        oth=oth,
        outdir=f"out_susan_{arch.lower()}"
    )


def execute_cmd_with_append(
    apps={},
    *args, **kwargs
):
    for f, app in apps.items():
        shutil.move(f, f+".bak")
        with open(f+".bak") as src:
            with open(f, "w") as dst:
                dst.write(src.read() + app)

    try:
        execute_cmd(*args, **kwargs)
    except Exception as e:
        print(e)

    for f in apps:
        shutil.move(f+".bak", f)

def get_stat(stats, name):
    lines = stats.split("\n")
    for l in lines:
        parts = l.split()
        if len(parts) == 0:
            continue

        if parts[0] == name:
            return parts[1]

    raise Exception("Could not get stat {}".format(name))


def part_a(arch, testname, execf):
    with open(f"partA-{arch.lower()}-{testname}.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        stats = ["system.cpu.numCycles", "sim_insts", "sim_seconds", "system.cpu.dcache.overall_miss_rate::total"]
        writer.writerow(["l1d_size"] + stats)
        for size in["2kB", "4kB", "8kB", "16kB", "32kB"]:
            print(f"Doing part A for {arch}, {testname}, with cache size {size}")
            statinfo  = execf(arch=arch, oth=["--caches", f"--l1d_size={size}", "--cpu-type=TimingSimpleCPU"])
            print(f"Finished part A for {arch}, {testname}, with cache size {size}")
            writer.writerow([size] + [get_stat(statinfo, s) for s in stats])

def part_b(arch, testname, execf):
    with open(f"partB-{arch.lower()}-{testname}.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        stats = ["system.cpu.numCycles", "sim_insts", "sim_seconds", "system.cpu.dcache.overall_miss_rate::total"]
        writer.writerow(["l1d_size", "l1d_assoc", "cacheline_size"] + stats)
        for assoc in ["2", "8", "16", "32"]:
            for cachelinesize in ["16", "32", "64", "128"]:
                print(f"Doing part B for {arch}, {testname}, with assoc {assoc}, cachelinesize {cachelinesize}")
                statinfo = execf(arch=arch,
                    oth=[
                        "--caches",
                        f"--l1d_size=16kB",
                        f"--l1d_assoc={assoc}",
                        f"--cacheline_size={cachelinesize}",
                        "--cpu-type=TimingSimpleCPU"
                    ]
                )
                print(statinfo)
                print(f"Finished part B for {arch}, {testname}, with assoc {assoc}, cachelinesize {cachelinesize}")
                writer.writerow(["16kB", assoc, cachelinesize] + [get_stat(statinfo, s) for s in stats])

def part_d(arch, testname, execf):
    with open(f"partD-{arch.lower()}-{testname}.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        stats = ["system.cpu.numCycles", "sim_insts", "sim_seconds", "system.cpu.dcache.overall_miss_rate::total"]
        writer.writerow(["bp_type"] + stats)
        for bp in["BiModeBP", "TAGE", "MultiperspectivePerceptron8KB", "MultiperspectivePerceptron64KB"]:
            print(f"Doing part D for {arch}, {testname}, with bp {bp}")
            statinfo  = execf(arch=arch, oth=[
                f"--bp-type={bp}",
                "--cpu-type=DerivO3CPU",
                "--caches",
                f"--l1d_size=16kB",
            ])
            print(f"Finished part D for {arch}, {testname}, with bp {bp}")
            writer.writerow([bp] + [get_stat(statinfo, s) for s in stats])

def run_part(f):
    processes = []
    for arch in ["ARM", "X86"]:
        for test, exec_f in {"crc": execute_crc, "susan": execute_susan}.items():
            proc = Process(target=f, args=(arch, test, exec_f))
            processes.append(proc)
            proc.start()

    for proc in processes:
        proc.join()

    processes = []

#print("Running part A")
#run_part(part_a)

#print("Running part B")
#run_part(part_b)

print("Running part D")
run_part(part_d)
