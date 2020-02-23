import os
from multiprocessing import Pool


GEM5_PATH = '/usr/local/src/gem5'
GEM5_CMD = 'build/X86/gem5.opt'
SIM_SCRIPT = 'configs/example/se.py'


BRANCH_PREDICTORS = {
     0 : 'MultiperspectivePerceptron8KB',
     1 : 'TAGE_SC_L_8KB',
     2 : 'LocalBP',
     3 : 'BiModeBP',
     4 : 'TAGE',
     5 : 'MultiperspectivePerceptron64KB',
     6 : 'MultiperspectivePerceptronTAGE8KB',
     7 : 'TAGE_SC_L_64KB',
     8 : 'TournamentBP',
     9 : 'LTAGE',
    10 : 'MultiperspectivePerceptronTAGE64KB',
}



def partD(select):
    gem5_cmd = os.path.join(GEM5_PATH, GEM5_CMD)
    sim_script = os.path.join(GEM5_PATH, SIM_SCRIPT)

    branch_predictor = BRANCH_PREDICTORS[select]


    output_dir = f'/home/output/gem5_out_dirs/D_{branch_predictor}'
    stdout_file = f'/home/output/stdout_files/D_{branch_predictor}.txt'

    benchmark = '/home/susan/susan'
    benchmark_options = ' '.join([
        '/home/susan/input_large.pgm',
        f'/home/output/susan_out/D_{branch_predictor}.pgm',
    ])

    gem5_part = f'{gem5_cmd} -d {output_dir}'

    sh_part = f'> {stdout_file} 2>&1'

    sim_part = '{} -c {} -o "{}" --bp-type {}'.format(
        sim_script,
        benchmark,
        benchmark_options,
        branch_predictor,
    )

    command = ' '.join([
        gem5_part,
        sim_part,
        sh_part,
    ])

    os.system(command)
    return f'Ran the Command:\n\t{command}\n'


if __name__ == '__main__':

    with Pool(3) as pool:
        return_strings = pool.map(partD, [3, 7, 10])

    for return_string in return_strings:
        print(return_string)
