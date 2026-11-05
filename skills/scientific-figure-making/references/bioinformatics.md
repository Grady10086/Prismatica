# Biological tables and genomic compositions

Use for OncoPrint, spatial omics, annotated phylogenies, chromosome Circos and
Sashimi plots. Use the sibling set-overlap guide for gene-set cores/UpSet.

## Input and chart choice

- **OncoPrint:** supplied mutation/copy-number calls + sample/cohort identities.
  Preserve WT vs unassayed, co-occurring events and assayed denominators. Panel
  burden is altered genes, not TMB. Keep paired sample identities; never fill a
  missing call as WT. Accept standardized categories only after an explicit,
  documented mapping from the upstream caller.
- **Spatial:** supplied coordinates, type labels and expression. Preserve x/y
  aspect, units, image orientation, coordinate frame and original image size.
  Match one tissue frame at a time. Register images upstream; do not stretch an
  image to make unregistered spots appear to align. Cell/spot composition is
  descriptive, not a donor-level inferential test.
- **Phylogeny:** supplied topology/root and non-negative branch lengths; numeric
  traits and groups are optional annotations, not inferred clades. Match leaf
  IDs exactly. Show missing annotations as missing. Do not fabricate bootstrap
  support, rooting, branch lengths or relationships from a decorative tree.
- **Circos:** chromosome declarations + zero-based half-open bp intervals. Arc
  lengths follow chromosome lengths and ribbons attach at supplied intervals.
  GC/density windows need consistent units; distinguish zero windows from absent
  windows and use length-weighted GC summaries. Layout cannot infer synteny,
  structural variants, homologous genes or causal edges.
- **Sashimi:** one locus/transcript annotation, supplied coverage windows and
  junction counts by sample. Keep all samples on the same coordinate/coverage
  scale. Require explicit zero counts for assayed sample–junction combinations;
  absent values are not zero. Junction counts are not PSI, unique-read totals or
  automatically library-size-normalized. This first compositor is unstranded;
  use a dedicated genome viewer for strand-aware multi-transcript interpretation.

## Native Python helper

Run from this skill directory:

```sh
python scripts/bioinformatics.py --kind oncoprint --demo --out /tmp/oncoprint
python scripts/bioinformatics.py --kind spatial --csv /path/spots.csv --image /path/tissue.png --out /tmp/spatial
python scripts/bioinformatics.py --kind phylogeny --csv /path/nodes.csv --out /tmp/tree
python scripts/bioinformatics.py --kind circos --demo --out /tmp/circos
python scripts/bioinformatics.py --kind sashimi --csv /path/locus.csv --out /tmp/sashimi
```

Each command exports editable SVG/PDF and PNG. `--demo` loads the corresponding
**synthetic** member table in `assets/bioinformatics/`. Real imports require
`--csv`; outputs keep the source-provenance distinction. Import the `render`,
`read_table`, `validate`, `tree_structure` or individual plot functions when
building a larger composition. The Python helper uses supplied node tables;
the online tree also converts branch-length Newick into such a table.

## CSV schemas

| Kind | Columns |
| --- | --- |
| oncoprint | `sample,gene,alteration,cohort` |
| spatial | `spot,x,y,cell_type,expression` |
| phylogeny | `node,parent,label,length,group,value` |
| circos | `kind,chrom,start,end,value,target,target_start,target_end,label` |
| sashimi | `kind,sample,start,end,value,label` |

Quoted text/Unicode names are accepted. Blank tree parents identify the root;
blank numeric leaf values mean missing, not zero. OncoPrint uses `WT`, `NA`,
`missense`, `truncating`, `amplification`, `deletion`; every sample–gene pair is
explicit. Spatial expression and numeric tree traits are non-negative. Circos
kinds are `chromosome`, `gc`, `density`, `link`; target fields apply only to links.
Sashimi kinds are `exon`, `coverage`, `junction`; all sample–junction pairs need
explicit non-negative integer counts. Supplied genomic intervals are not clipped
or merged silently. Keep the original genome assembly/version with real inputs.

## Production review

Use the registered Iris anchors/ramp steps and distinguish event categories with
explicit legends; NA must be visually distinct from WT. Keep categorical colors
stable across linked panels. Genome/phylogeny/spatial figures preserve geometry;
zooming is a viewing operation, never a change to the underlying values. Check
long IDs, crowded leaves, multi-event cells, zero tracks and missing annotations.
Gallery masters use 11.6 × 6.8 inch canvases; adapt typography/panel count to final
paper dimensions with `paper_layout` and inspect before delivery. Export tables,
source code and normalization/coordinate definitions with final figures.

Composition references: [OncoPrint, Nature Genetics 2026](https://www.nature.com/articles/s41588-025-02468-9#Fig1),
[spatial hippocampus atlas, Nature Neuroscience 2025](https://www.nature.com/articles/s41593-025-02022-0#Fig4),
[iTOL v6, 2024](https://doi.org/10.1093/nar/gkae268),
[genome Circos, Scientific Data 2025](https://www.nature.com/articles/s41597-025-05568-7#Fig1),
[Sashimi and genomic language models, Nature Genetics 2025](https://www.nature.com/articles/s41588-025-02347-3).
These are source references, not original figures licensed for redistribution.
