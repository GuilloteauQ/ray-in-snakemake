import ray
from tqdm import tqdm
from random import random
import argparse

# Let's start Ray

SAMPLES = 1000000 
# By adding the `@ray.remote` decorator, a regular Python function
# becomes a Ray remote function.
@ray.remote
def pi4_sample():
    in_count = 0
    for _ in range(SAMPLES):
        x, y = random(), random()
        if x*x + y*y <= 1:
            in_count += 1
    return in_count

# To invoke this remote function, use the `remote` method.
# This will immediately return an object ref (a future) and then create
# a task that will be executed on a worker process. Get retreives the result. 
# future = pi4_sample.remote()
# pi = ray.get(future) * 4.0 / SAMPLES
# print(f'{pi} is an approximation of pi') 

# Now let's do this 100,000 times. 
# With regular python this would take 11 hours
# Ray on a modern laptop, roughly 2 hours
# On a 10-node Ray cluster, roughly 10 minutes 

def main():
    parser = argparse.ArgumentParser(description='plop')
    parser.add_argument('--batches', type=int, help='number of batches')
    parser.add_argument('--output', help='outfile')
    parser.add_argument('--snakeid', help='snakemake jobid')
    args = parser.parse_args()
    ray.init()
    BATCHES = args.batches
    print(f"SNAKEMAKE ID: {args.snakeid}")
    results = [] 
    for i in tqdm(range(BATCHES)):
        results.append(pi4_sample.remote())
    output = ray.get(results)
    pi = sum(output) * 4.0 / BATCHES / SAMPLES
    with open(args.output, "w") as output_file:
        output_file.write(f'{pi} is a way better approximation of pi\n') 


if __name__ == "__main__":
    main()
