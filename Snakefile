
BATCH_SIZES = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90]



rule all:
	input:
		expand("results/pi_{batch_size}.txt", batch_size=BATCH_SIZES)
		
		
rule run_ray:
	input:
		"pi.py",
	output:
		"results/pi_{batch_size}.txt"
	shell:
		"nix develop --command python3 {input} --batches {wildcards.batch_size} --output {output} --snakeid {jobid}"
		
