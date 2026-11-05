# Bioinformatics compositions

Five new browser studies use typed biological tables, editable SVG, linked marks,
and Iris colors. Defaults are seeded **synthetic fixtures**, not measured patients,
tissue, organisms or sequencing reads. Biological names in a fixture do not imply
that its frequencies or associations are real.

| Study | Online view | Layout |
| --- | --- | --- |
| `bio-oncoprint` | [OncoPrint](https://grady10086.github.io/Prismatica/#lab/bio-oncoprint) | Patient alteration matrix, cohort strip, panel burden, gene alteration frequency |
| `bio-spatial` | [Spatial omics](https://grady10086.github.io/Prismatica/#lab/bio-spatial) | Two maps in one spatial frame and a composition ribbon; optional local tissue image |
| `bio-phylogeny` | [Annotated phylogeny](https://grady10086.github.io/Prismatica/#lab/bio-phylogeny) | Radial branch-length tree, categorical/numeric rings, leaf traits and group counts |
| `bio-circos` | [Genomic Circos](https://grady10086.github.io/Prismatica/#lab/bio-circos) | Length-proportional chromosome arcs, density/GC windows and interval ribbons, with summaries to the left |
| `bio-sashimi` | [Sashimi](https://grady10086.github.io/Prismatica/#lab/bio-sashimi) | Full-width coverage/junction tracks above a support matrix and paired count view |

## Editing and export

Open the data drawer to edit CSV or import an exported JSON table. These five
families accept quoted text IDs, Unicode and categorical names, while the older
numeric schemas remain unchanged. Newick can be pasted or imported for the tree.
All data is processed locally. CSV/JSON downloads preserve input rows; SVG/PNG
exports use the complete calculated figure, independently of zoom, hover or morph
animations. The UI abbreviates long labels where space is limited; tooltips and
downloaded tables retain their complete values.

The scope is **visualization of supplied values**, not mutation calling, image
registration, expression normalization, phylogenetic inference, alignment,
synteny discovery, splice quantification or hypothesis testing. Units and the
meaning of biological replication must come from the source analysis.

## OncoPrint

```csv
sample,gene,alteration,cohort
P1,KRAS,WT,Cohort A
P1,TP53,NA,Cohort A
P2,KRAS,missense,Cohort B
P2,TP53,amplification,Cohort B
```

Use 2–64 samples and 2–20 genes. Calls are `WT`, `NA`, `missense`, `truncating`,
`amplification` and `deletion`. Every sample–gene pair must be explicit. `NA`
means unassayed, not wild type; WT/NA cannot coexist with another call on the
same pair. Multiple distinct alterations can share a cell. Cohort is consistent
per sample (up to six cohorts). Genes with no assayed samples have an undefined
frequency, displayed as “not assayed”. Panel burden counts altered genes and is
**not exome-wide TMB**. No statistical comparison between cohorts is inferred.

## Spatial

```csv
spot,x,y,cell_type,expression
S1,120,180,Immune,0.8
S2,240,260,Stromal,1.4
```

One coordinate frame, up to 3,000 unique spots and eight annotated types.
Expression must be non-negative and already normalized as needed by the caller.
Both maps preserve equal x/y scale and increasing image-y downward. Without an
image, coordinates are labelled as supplied units. A PNG/JPEG can be uploaded
locally (under 4 MB and 40 megapixels); coordinates must match its **original
pixel dimensions**. The raster is downsampled to at most 1,800 pixels per side for
embedding, while coordinate mapping uses original dimensions. The SVG contains
the image rather than a remote link. Removing the image restores the coordinate
view. Changing the synthetic-data parameters clears it; opacity edits retain it.
It is not an automatic registration or spot-deconvolution tool.

## Phylogeny

```csv
node,parent,label,length,group,value
root,,,0,,
A,root,Taxon A,0.1,Clade A,4
B,root,Taxon B,0.2,Clade B,7
```

One supplied root (blank parent, length 0), non-negative branch lengths, no
cycles, unique nodes/leaf labels, 2–64 leaves and up to 192 nodes. Parent links
need not be in input order. Group and non-negative numeric leaf annotations may
be blank. Missing values remain missing rather than becoming measured zeroes.

Native Newick example: `('Taxon A':0.1,(B:0.2,C:0.3):0.4);`. Non-root lengths
are required; quoted labels and internal labels are supported. Comments/extended
Newick metadata are not interpreted. This preserves the supplied rooting and
topology; it does not infer an outgroup, branch lengths or support values. Newick
alone supplies no annotation values. Export the node CSV to add them, or to use
the Python helper. Radius encodes root distance; categorical and numeric outer
rings are annotation glyphs independent of branch length.

## Circos

```csv
kind,chrom,start,end,value,target,target_start,target_end,label
chromosome,chr1,0,1000000,0,,0,0,chr1
chromosome,chr2,0,800000,0,,0,0,chr2
gc,chr1,0,100000,0.42,,0,0,GC fraction
density,chr1,0,100000,12,,0,0,Supplied density
link,chr1,10000,30000,1,chr2,20000,40000,Block A
```

Declare 2–12 chromosome lengths. All intervals use integer, **zero-based half-open
bp coordinates** within their declared chromosome. GC is in [0,1]; density and
link weights are non-negative supplied values. Target fields belong to links
only; non-link target coordinates may be blank or 0. GC/density windows cannot
overlap within a chromosome. Unsupplied windows remain gaps; supplied zero
windows retain a neutral background. The mean GC summary is interval-length
weighted. Chromosome arcs and ribbon endpoints follow real coordinates. Ribbon
width reflects interval span, not a count or statistical association. The side
weight chart aggregates supplied weights by source, without deduplicating
biological events. No genomic homology or rearrangements are inferred.

## Sashimi

```csv
kind,sample,start,end,value,label
exon,GENE1,1000,1200,0,Exon 1
exon,GENE1,1500,1700,0,Exon 2
coverage,Control,1000,1200,20,
coverage,Treated,1000,1200,28,
junction,Control,1200,1500,8,J1
junction,Treated,1200,1500,17,J1
```

One locus and one exon annotation per file; use integer zero-based half-open bp
coordinates, 2–40 exon intervals, 1–4 samples and 1–10 distinct junctions. Coverage
values are supplied non-negative window averages, with non-overlapping windows
per sample. A junction value is an integer supporting-read count. Every
sample–junction combination needs an explicit row; use 0 for assayed zero support.
Coverage gaps are left blank rather than filled with zeroes. All tracks share one
coverage scale. Arc thickness is sqrt-scaled raw support with exact counts in
labels/tooltips. Coordinates are ascending genomic order; transcript strand is
not inferred. A one-sample file leaves the paired-comparison panel unavailable.
Counts are not library-size-normalized automatically and are not PSI values.
Their sum is a sum of junction counts, **not a count of unique reads**.

## Reusable Python figures and skill

The [skill guide](../skills/scientific-figure-making/references/bioinformatics.md)
routes these data contracts and production checks. The
[Python helper](../skills/scientific-figure-making/scripts/bioinformatics.py)
accepts the same CSV tables, including string identifiers and missing annotation
values. It exports native Matplotlib SVG/PDF/PNG. The bundled CSVs are fixed
exports of the browser generator at seed 1107, so both implementations can use
identical observations. The Python layouts are independently composed gallery
masters, not pixel-identical copies of the browser; resize for venue typography.

```sh
uv run python skills/scientific-figure-making/scripts/bioinformatics.py --kind oncoprint --demo --out figures/oncoprint
uv run python skills/scientific-figure-making/scripts/bioinformatics.py --kind spatial --csv spots.csv --image tissue.png --out figures/spatial
uv run python skills/scientific-figure-making/scripts/bioinformatics.py --kind phylogeny --csv nodes.csv --out figures/tree
uv run python skills/scientific-figure-making/scripts/bioinformatics.py --kind circos --demo --out figures/circos
uv run python skills/scientific-figure-making/scripts/bioinformatics.py --kind sashimi --demo --out figures/sashimi
```

## Reference studies

These are composition and semantics references, not sources of the synthetic
values. No source-paper images or patient records are included.

- [Genomic evolution of pancreatic cancer at single-cell resolution, Nature Genetics (2026), Fig. 1](https://www.nature.com/articles/s41588-025-02468-9#Fig1).
- [Human hippocampus single-nucleus and spatial atlas, Nature Neuroscience (2025), Figs. 3–4](https://www.nature.com/articles/s41593-025-02022-0#Fig4).
- [iTOL v6, Nucleic Acids Research (2024)](https://doi.org/10.1093/nar/gkae268).
- [Purpleleaf Plum genome assembly, Scientific Data (2025), Fig. 1](https://www.nature.com/articles/s41597-025-05568-7#Fig1).
- [Nucleotide dependency analysis of genomic language models, Nature Genetics (2025)](https://www.nature.com/articles/s41588-025-02347-3).
