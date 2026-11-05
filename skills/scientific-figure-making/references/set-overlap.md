# Set overlap: flowers, UpSet and pairwise similarity

Use this branch for Venn/Euler questions, flower/petal diagrams, gene-family cores,
model success sets, retrieved-document overlap and training-data intersections.

1. Request **item identities and memberships**, not only set sizes. Define a shared
   item identifier, deduplication and matching rule. Counts alone cannot identify
   pairwise or higher-order overlaps. For genomic intervals, an explicit interval
   overlap policy must precede this item-based script; it does not infer that policy.
2. Use a flower summary for 2–6 sets when the story is the all-set core plus each
   set's unique items. Petals are schematic; **do not label the picture as a complete
   six-set Venn diagram**, infer intersection counts from region geometry or imply
   area proportionality. Show set totals separately. A zero core must stay zero.
3. Use UpSet for exact higher-order intersections. A column is membership in all
   marked sets **and absence from every unmarked set**. These exclusive columns
   partition the union. Order by count with a stable tie-breaker; if only top-k are
   shown, state both omitted intersection count and omitted item count.
4. Pairwise intersections are inclusive of higher-order overlaps. Jaccard is
   |A∩B| / |A∪B|. Two empty sets yield undefined (display —), not a measured 1.
   Pairwise similarities cannot reconstruct all higher-order intersections. Network
   positions are schematic and edges are overlaps, not causal or pathway claims.
5. Check that exclusive counts sum to union size, degree counts sum to union size,
   and total membership equals Σ degree × item count. Keep item IDs paired and
   never invent missing disjoint regions or reproduce example counts as research.
6. Export editable vectors; inspect names, zero counts, limits and legends at the
   intended manuscript size. Use the registered project palette; this script uses
   the Iris anchors plus two lighter ramps. Distinguish this script's synthetic demo
   from imported memberships.

## Reusable script

`python scripts/set_overlap.py --csv /path/members.csv --out /path/figures`
(from this skill's directory). Input has header `item,<2–6 distinct set names>`;
rows contain a unique string item ID and binary 0/1 memberships. No blank IDs,
duplicate rows, non-binary memberships or all-zero items are accepted. Empty
sets are permitted. The CSV uses standard quoting for identifiers and set names.

`python scripts/set_overlap.py --demo --out /tmp/set-overlap` generates a seeded
synthetic example. `--top 18` controls displayed UpSet columns. Outputs include
three standalone compositions in SVG/PDF/PNG, `exact-intersections.csv` and
`summary.json`; the latter records counts and undefined Jaccard values as null.
These are gallery masters; adapt dimensions and font sizes to the venue.

Import `summarize`, `flower`, `upset`, `jaccard` and `set_sizes` from the script
when arranging a larger composite. All three views must use the same summary.

## Sources

- Lex et al. (2014), [UpSet: Visualization of Intersecting Sets](https://www.visdesignlab.net/publications/2014_infovis_upset/), DOI 10.1109/TVCG.2014.2346248.
- Khan & Mathelier (2017), [Intervene](https://link.springer.com/article/10.1186/s12859-017-1708-7), DOI 10.1186/s12859-017-1708-7.

These sources motivate the choice of representations. The petal artwork and demo
memberships here are original; the user-supplied screenshot has no verified paper
provenance, so its plant illustrations and counts are not distributed as our data.
