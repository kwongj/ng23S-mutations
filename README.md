# ng23S-mutations
Identifies mutations in 1-4 copies of the 23S rRNA gene in Neisseria gonorrhoeae

##Author

Jason Kwong (@kwongjc)

##Dependencies
* [Snippy](https://github.com/tseemann/snippy)
* Python 2.7.x

##Usage

1. Run snippy with Illumina reads for each *N. gonorrhoeae* query isolate. Use the reference genome NCCP11945 included in this repository. Note that this reference genome has been altered to mask 3 copies of the 23S rRNA gene to force mapping to a single region.
```
$ snippy --outdir snippy --ref NG_NCCP11945_23S-masked.gbk --R1 isolate_R1.fastq.gz --R2 isolate_R2.fastq.gz
```

2. Run ng23S-mutations script. Results are printed to stdout.
```
$ ng23S-mutations.py snippy1 snippy2 ... snippyN
```
To save results to file:
```
$ ng23S-mutations.py snippy1 snippy2 ... snippyN > results.txt
```


```
$ ng23S-mutations.py -h
usage: 
  ng23S-mutations.py <snippy1> <snippy2> ... <snippyN>

Script to identify 23S mutations in NG

positional arguments:
  DIR              Snippy directories (required)

optional arguments:
  -h, --help       show this help message and exit
  --prefix PREFIX  Snippy .tab output prefix (default="snps")
  --version        show program's version number and exit
```

##Bugs

Please submit via the [GitHub issues page](https://github.com/kwongj/ng23S-mutations/issues).  

##Software Licence

[GPLv3](https://github.com/kwongj/ng23S-mutations/blob/master/LICENSE)

