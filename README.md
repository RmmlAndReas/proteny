proteny
=======

A tool to analyze synteny at the protein level.
We develop an algorithm to detect statistically significant clusters of genes between two proteomes.
It operates at the exon level, allowing for a very fine grained synteny analysis.
The tool provides algorithms to quickly detect and visualize results in order to support conclusions from genomic data.

The method discovers clusters of hits from a bi-directional BLASTp of translated exon sequences in two organisms.
A dendrogram for hits is built based on genomic distances between hits, and cut based on significance of a cluster score based on a permutation test at each node in the tree.
The result is a set of large clusters describing high exonic conservation.

![An example of the figures generated by proteny](/readme/aniger_51388-n402.png)

Algorithm
=========

We use BLASTp to produce a set of hits, which are used to build

![We use BLASTp to produce a set of hits, which are used to build](/readme/clustering_dendrogram_a.gif)

a dendrogram which is traversed to find

![a dendrogram which is traversed to find](/readme/clustering_dendrogram_b.gif)

significant clusters

![significant clusters.](/readme/clustering_dendrogram_c.gif)

Dependencies
=============
 * CIRCOS: http://circos.ca/
 * IBIDAS: https://github.com/mhulsman/ibidas
 * BLAST+: ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/

Usage
=========

Make sure that each dependency (and their dependencies) is installed.
modify the "$CIRCOS" variable in "run" to reflect the location of your circos installation.

"example.py" contains an example which details the way the tool can be used.
"run" is a script which actually runs circos finding each configuration file.

