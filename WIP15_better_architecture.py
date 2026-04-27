import argparse
import numpy as np



if __name__ == '__main__':

    # python .\WIP15_better_architecture.py -h to get this information, and 'help' information below
    parser = argparse.ArgumentParser(
        prog='Architecture tests', 
        description='Wave propagation in 2D with better architecture')
    
    # action='store_true' means that if the flag is present, movie will be set to True, otherwise it will be False
    parser.add_argument('-m', '--movie', action='store_true', help='Make video instead of animation')
    parser.add_argument('-n', '--name', help='Name of the output file, if movie')
    parser.add_argument('-t','--time', help='Simulation time', default=10.0, type=float)
    args = parser.parse_args()
    print(args)
    if args.movie and (args.name is None):
        randint = int((np.random.random()*10000))
        args.name = f'movie{randint}.mp4'

    if args.movie:
        print(f"Making movie: {args.name}")
        
    print(args)
