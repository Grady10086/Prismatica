# CS diagnostic figures: training, attention and failures

Run the self-contained local demo:

```sh
uv run --with matplotlib --with scikit-learn python skills/scientific-figure-making/examples/cs_diagnostic_gallery.py --out /tmp/cs-diagnostics
```

Three PNG/SVG compositions and `experiment-record.json` are produced. Uses scikit-learn’s real 8×8 handwritten digits; trains a deliberately tiny NumPy attention-pooling classifier on a fixed stratified split. This is an actual local demonstration, not a published benchmark or a pretrained vision-language model. The simple model is weak; do not present its accuracy as a competitive result. No external image downloads are needed.

## Compositions and semantics

**Optimization observatory.** Dark background, large parameter-checkpoint trajectory, smaller unsmoothed train/held-out loss view, and a horizontal single-input prediction strip. PCA is fit to five saved parameter vectors (steps 0, 10, 40, 120, 300); segments only connect those checkpoints and do not show the intervening optimization path. Each vector concatenates trainable embedding, query, classifier and bias; its Euclidean/PCA geometry depends on parameter scaling. The same held-out source (first in the fixed split) is retained across the strip, even when it remains wrong. The JSON holds all 301 evaluated losses, accuracies and the five full prediction arrays. Preserve loss spikes rather than smoothing them away. Held-out evaluation does not feed training updates; no early stopping is used.

**Attention studio.** A dominant input overlay, five actual patch crops linked to the pooled representation by weight-dependent line thickness, and a small secondary contact sheet. Model: 16 nonoverlapping 2×2 patches → trainable tanh embedding plus fixed random position vectors → learned single-query softmax attention → weighted pooling → ten-way classifier. These are actual pooling weights, not Transformer self-attention, text alignment, gradient attribution or causal importance. Overlays use fixed magma limits 0–1 and alpha 0.65 for all examples; original grayscale is unchanged underneath. Link width is `0.7 + 8 × attention`, not a pure proportional flow. Only the top five links are drawn; omitted mass is stated (rounded to two decimals). Hero is selected post hoc by largest maximum class probability; other images are the first held-out sources of labels 1, 3, 5, 8. A shared standalone colorbar records this normalization.

**Failure casebook.** Asymmetric summary statistics and four large error/control pairs. Select the four wrong held-out predictions with largest maximum softmax probability; this is a score, not calibrated confidence. Controls are raw-pixel nearest same-label TRAINING images and are not guaranteed to be classified correctly. They are visual comparisons, not counterfactual corrections. All sample IDs, labels, scores, selection rules and control IDs are recorded. Do not infer an error mechanism from resemblance or cherry-picked examples.

## Adapt to research results

Keep the distinct compositions but replace the demo with actual run logs, checkpoint weights, attention tensors and evaluated examples. Record model/head/layer, token order, patch geometry, normalization and selection protocol. Preserve shared image display scales. For large models, replace all-parameter PCA with a justified sampled layer or projection and state it. Use several seeds for training claims and include uncertainty where applicable. These wide editorial layouts need venue-sized typography and reduced titles before becoming manuscript figures.
