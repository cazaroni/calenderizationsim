# calenderizationsim
NFL Big Data Bowl: Model and Analytics Pipeline

Executive Summary (for coaches)

We built a defensive analytics pipeline that learns play structure directly from tracking data—no manual labels needed. It encodes each play into a compact “play fingerprint,” clusters those fingerprints into defensive spacing archetypes, and scores plays on two axes:

DCI (Defensive Coverage Index): how tightly the defense collapses around the coverage shell.
DIS (Defensive Integrity Score): how clearly the defense executes a single structural intent (i.e., not stuck between two archetypes).
These scores are computed per play and then calibrated against game context (down, distance, defenders in the box) to better reflect outcomes on pass plays. The result is a fast, coach-facing metric suite that highlights spacing cohesion, structural clarity, and execution quality—without requiring hand-labeled coverage types.

Technical Overview (for data scientists)

We implement a self-supervised, graph-based representation learning pipeline on frame-level player tracking, followed by dimensionality reduction, cluster ensemble selection, metric computation, and supervised calibration.

Self-supervised backbone: PyTorch + PyG (R-GCN + TransformerConv + GRUCell)
Data: NFL tracking and supplementary CSVs (2023 train split), unified field direction
Graph construction: players are nodes; edges based on spatial proximity
Embeddings: learned at play level; reduced via PCA→UMAP; clustered by KMeans/GMM/HDBSCAN with stability checks
Metrics: geometric proxies derived from distances to learned archetypes; supervised calibration with HistGradientBoosting
Data Pipeline

Preprocessing

Script: preprocess_data.py

Source data location: /lustre/proyectos/p037/datasets/raw/114239_nfl_competition_files_published_analytics_final
Input/output CSV pairing: input_2023_w??.csv, output_2023_w??.csv
Field normalization:
Unifies all plays to “right” direction with coordinate flips (x: 0–120, y: 0–53.3).
Normalizes orientations o and dir to avoid direction inconsistency.
Converts player height to inches; retains core motion features [x, y, s, a, o, dir].
Play assembly:
Merges input/output, backfills play_direction, and joins supplementary metadata (EPA, pass result, down, yards to go).
Exports play-wise frame data to plays_processed.parquet.
Why this matters for coaches:

All plays are aligned to the same field orientation, making spacing comparisons consistent across games.
Representation Learning

Dataset & Graph Builder

Module: dataset_dynamic.py

Dynamic play dataset returns pairs of consecutive frames (Xt, Xt+1) per play.
Features per node (player): [x, y, s, a, o, dir]
Collate function pads player sets to handle variable roster presence per frame.
Graph construction:
Nodes: valid players (non-zero feature rows).
Edges: created for pairs closer than a spatial threshold (default 10 yards).
Output: PyG Data objects with x (node features), edge_index, edge_type (simple default).
Impact:

The model learns player interactions as edges rather than independent tracks, key to capturing spacing and leverage.
Model Architecture

Module: train_ssl.py

Encoder: DynamicEncoder
R-GCN layers (relational message passing) → TransformerConv (global attention) → GRUCell (optional temporal update).
Heads:
Projection head for contrastive learning (InfoNCE).
Reconstruction head for masked feature prediction (denoising auxiliary task).
Augmentations:
Node drop, edge drop, feature masking + jitter, small rotations and translations.
Loss:
Contrastive InfoNCE at the graph level between two augmented views.
Masked reconstruction loss at node level.
Training:
Mixed precision with autocast and GradScaler.
Regular checkpoints and loss plot saving.
Why this matters for coaches:

The model learns robust patterns of spacing and movement without labels—so it generalizes beyond predefined coverage names to the actual structure and cohesion it sees.
Embeddings and Clusters

Play-Level Embeddings

Script: generate_embeddings.py

Loads the trained backbone and generates play embeddings from early frames (guarded for NaNs/Inf and empty graphs).
Exports embeddings_playlevel.parquet with game_id, play_id, frame_id, and embedding dims.
Coach view:

Each play becomes a fingerprint of the defensive shell; we can compare similar fingerprints across games/weeks.
Cluster Ensemble and Archetypes

Script: cluster_embeddings.py

Normalizes and reduces embeddings:
StandardScaler → PCA (128→32) → UMAP (32→16 if available; else PCA fallback).
Clustering candidates:
KMeans (multiple K), GaussianMixture (GMM), HDBSCAN.
Model selection:
Scores each config using silhouette and bootstrap ARI stability.
Picks the best method/K automatically.
Outputs:
Saves reduced embeddings (PCA_embeddings.npy, UMAP_embeddings.npy).
Saves archetype centroids as A_ideal_best.parquet (the defensive spacing templates).
Records selected method/K in final/metadata.json.
Coach view:

These archetypes are “idealized defensive spacing schemes” learned from data—not labels—and serve as reference templates for measuring how closely a defense fits a clear structure on each play.
Metrics

Baseline metrics (unsupervised)

Script: compute_metrics_playlevel.py

Inputs:

embeddings_playlevel.parquet (metadata)
Reduced embeddings (UMAP_embeddings.npy preferred, fallback PCA_embeddings.npy)
Archetypes A_ideal_best.parquet
Process:

Computes Euclidean distances from each play to every archetype:
d1: nearest centroid distance (structure fit)
d2: second-nearest centroid distance (ambiguity margin)
Proxies:
Spacing Proxy: exp(−d1) → tighter spacing yields higher scores.
Execution Proxy: 1/(1 + d1) → simple decay complement.
Integrity Proxy: (d2 − d1) / d2 → clarity of intent; penalizes plays “between” archetypes.
Baseline indices:
DCI (Defensive Coverage Index): exp(−α·d1).
DIS (Defensive Integrity Score): average of Spacing and Integrity with tunable weights.
Output:

metrics_playlevel_baseline.parquet with cluster_id, distances, proxies, and baseline DCI/DIS.
Coach view:

DCI flags how well the defense collapses into a coherent coverage shell.
DIS highlights whether the defense had a clear, singular structural intent versus being stuck mid-adjustment or miscommunicated.
Supervised calibration (pass plays)

Script: train_dci_head.py

Merges baseline metrics with supplementary context:
down, yards_to_go, defenders_in_the_box, pass_result, epa.
Filters to pass plays and sets target:
Defensive success = 1 for incomplete/sack/interception; 0 for complete.
Features:
Distance/spacing/integrity metrics + integrity-to-distance ratio.
Context features + cluster_id (categorical).
Model:
HistGradientBoostingClassifier with categorical feature support and 5-fold CV predictions.
Outputs:
AUC and correlation with EPA for sanity.
metrics_playlevel_supervised.parquet with dci_supervised and dis_final.
Saves calibrator model to models/dci_calibrator.pkl.
Coach view:

We calibrate DCI with down/distance/box counts, better matching situational expectations.
Use dci_supervised for game planning and post-game review: which structures and contexts correlate with successful pass defense.
What You Can Do With It

For coaches:

Identify spacing archetypes your team executes best and worst.
Track weekly trends in DCI and DIS for opponent scouting—where do they lose integrity (confusion) and where are they tight?
Context-aware DCI helps separate good spacing that still fails due to unfavorable down/distance from true breakdowns.
For analysts:

Slice by coverage shell clusters, down/distance bins, and game state.
Run controlled comparisons of spacing integrity vs. EPA and success rates.
Extend metrics to personnel packages, motion effects, and splits by formation.
Inputs/Outputs at a Glance

Input features per player: [x, y, s, a, o, dir]
Graph edges: proximity within ~10 yards
Embeddings: HIDDEN_DIM (128) node embeddings → pooled graph embedding → reduced to 16D (UMAP) when available
Archetypes: learned centroids in reduced space
Scores:
DCI: exp(−distance to nearest archetype)
DIS: blend of spacing cohesion and integrity (margin to second archetype)
DCI_supervised: calibrated with down, distance, box count, and cluster ID
Notes and Edge Cases

Data hygiene: Embedding generation sanitizes NaNs/Inf and handles empty graphs gracefully.
Field normalization: All plays flipped to “right” ensures consistent geometry.
HDBSCAN: Included but only used if it finds >1 valid cluster with enough samples.
Fallbacks: If UMAP isn’t installed, PCA 32D is used for clustering.
Next Steps

Add offense/defense role tagging to improve relational types (edge_type) in R-GCN.
Incorporate temporal consistency by linking consecutive frames explicitly in a temporal GNN.
Expand supervised labels beyond pass outcome (e.g., separation allowed, air yards allowed, pressure events).
Produce interactive visualizations for coaches (play fingerprints, cluster exemplars, DCI/DIS timelines).
How to Run (reference)

Preprocess data:
preprocess_data.py → creates plays_processed.parquet
Train SSL backbone:
train_ssl.py → saves backbone checkpoints and final model
Generate embeddings:
generate_embeddings.py → embeddings_playlevel.parquet
Cluster and select archetypes:
cluster_embeddings.py → final/A_ideal_best.parquet
Compute baseline metrics:
compute_metrics_playlevel.py → metrics_playlevel_baseline.parquet
Supervised calibration:
train_dci_head.py → metrics_playlevel_supervised.parquet
