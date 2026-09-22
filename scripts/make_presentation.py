import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

fig_dir = BASE_DIR
out_pptx = BASE_DIR

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (Dark Theme / Professional Blue & Navy)
NAVY = RGBColor(26, 43, 76)
WHITE = RGBColor(255, 255, 255)
LIGHT_BG = RGBColor(245, 247, 250)
ACCENT_BLUE = RGBColor(41, 128, 185)
DARK_TEXT = RGBColor(44, 62, 80)
MUTED_TEXT = RGBColor(127, 140, 141)

blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="MSc BIG DATA ANALYTICS — PRACTICAL EXAMINATION"):
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = category_text.upper()
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    
    txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = NAVY

def add_card(slide, left, top, width, height, title, body_bullets, bg_color=WHITE, border_color=ACCENT_BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.margin_bottom = Inches(0.2)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    for bullet in body_bullets:
        p2 = tf.add_paragraph()
        p2.text = "• " + bullet
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK_TEXT
        p2.space_before = Pt(6)

# SLIDE 1: Title Slide
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = NAVY
bg1.line.fill.background()

tx1 = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(3.5))
tf1 = tx1.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "Analysis of Genome Variation, Phylogenetic Relationships and Geographic/Temporal Patterns in Porcine Circovirus 3 (PCV3)"
p1.font.size = Pt(28)
p1.font.bold = True
p1.font.color.rgb = WHITE
p1.space_after = Pt(15)

p2 = tf1.add_paragraph()
p2.text = "MSc Big Data Analytics — Bioinformatics & Unsupervised Machine Learning Project"
p2.font.size = Pt(18)
p2.font.color.rgb = ACCENT_BLUE
p2.space_after = Pt(25)

p3 = tf1.add_paragraph()
p3.text = "Student Practical Examination | Dataset: 500 PCV3 Complete Genomes | Tools: Biopython, MAFFT, IQ-TREE 3, scikit-learn"
p3.font.size = Pt(14)
p3.font.color.rgb = RGBColor(200, 214, 229)

# SLIDE 2: Problem Statement
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Problem Statement & Biological Context")
add_card(slide2, 0.8, 1.5, 5.6, 5.2, "Biological Background", [
    "Porcine Circovirus 3 (PCV3) is an emerging circular ssDNA circovirus associated with porcine dermatitis, nephropathy syndrome (PDNS), and reproductive failure.",
    "First identified in 2015–2016, PCV3 has rapidly been detected in swine herds globally.",
    "Investigating whether PCV3 genomes exhibit distinct genomic subgroups and whether these subgroups correlate with geographical regions or collection years is vital for surveillance."
])
add_card(slide2, 6.8, 1.5, 5.6, 5.2, "Analytical Problem", [
    "Identify genome-wide variations (SNPs, conserved vs. polymorphic positions) across 500 complete genomes.",
    "Perform unsupervised dimensionality reduction (PCA) and clustering (K-Means) on genome-derived features without metadata bias.",
    "Determine statistical associations between genome-based clusters and geographic location / sample year using rigorous permutation tests.",
    "Evaluate phylogenetic tree structure to determine consistency with unsupervised genomic clusters."
])

# SLIDE 3: Objectives
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "Project Objectives & Technical Scope")
add_card(slide3, 0.8, 1.5, 3.6, 5.2, "1. Bioinformatic QC & Alignment", [
    "Inspect FASTA sequences and Excel metadata.",
    "Perform sequence quality control (lengths, GC%, ambiguous bases).",
    "Perform Multiple Sequence Alignment (MAFFT).",
    "Identify conserved, variable, and parsimony-informative positions."
])
add_card(slide3, 4.8, 1.5, 3.6, 5.2, "2. Unsupervised ML Pipeline", [
    "Extract one-hot binary SNP matrix (genome features only).",
    "Compute PCA (explained variance, PC1 vs PC2).",
    "Evaluate K-Means clustering ($k=2..10$) using Silhouette scores.",
    "Isolate metadata from feature extraction to prevent data leakage."
])
add_card(slide3, 8.8, 1.5, 3.6, 5.2, "3. Statistical & Phylogenetic Evaluation", [
    "Construct Cluster x Country and Cluster x Year contingency tables.",
    "Run Chi-square permutation tests & calculate Cramér's V.",
    "Construct Maximum Likelihood tree (IQ-TREE 3 ModelFinder: GTR+F+I+G4, 1000 UFBoot).",
    "Derive evidence-based findings while avoiding causal overclaims."
])

# SLIDE 4: Dataset & Input Validation
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Input Data Audit & Metadata Matching")
add_card(slide4, 0.8, 1.5, 5.6, 5.2, "Input Files Validation", [
    "viral_genome.fasta: 500 complete genomes (~2,000 bp). Header format: <Accession>_<Country>_<Year>.",
    "accessions.csv.xlsx: 500 metadata rows with columns 'accession ' and 'Region '.",
    "Audit Result: Direct index matching matched only 22/500 rows. Key-based accession matching resolved records cleanly.",
    "No raw files were modified or deleted."
])
add_card(slide4, 6.8, 1.5, 5.6, 5.2, "Metadata Provenance Categorization", [
    "Excel_Verified (474 records): Accession and country matched Excel without conflict.",
    "Geography_Conflict_Excel (16 records): Accession matched Excel, but Excel contained conflicting regions (e.g. Spain vs Poland). Flagged explicitly.",
    "FASTA_Header_Only (10 records): Accession absent from Excel sheet; metadata derived directly from FASTA header.",
    "No metadata values were fabricated or silently overwritten."
])

# SLIDE 5: Complete Pipeline Architecture
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "End-to-End Bioinformatics Pipeline Architecture")
add_card(slide5, 0.8, 1.5, 11.7, 5.2, "Sequential Analysis Workflow", [
    "Phase 1: Input Data Inspection (FASTA & Excel integrity verification)",
    "Phase 2: Master Metadata Construction (Provenance flagging: Excel_Verified, Geography_Conflict, FASTA_Header_Only)",
    "Phase 3: Sequence Quality Control (Length distribution, GC content, ambiguous base filtering)",
    "Phase 4: Multiple Sequence Alignment (MAFFT alignment to 2,156 bp)",
    "Phase 5: Genome Variation & SNP Extraction (Identification of 890 variable sites, 466 parsimony-informative)",
    "Phase 6: Feature Extraction (Primary: 2,067 binary SNP features | Supplementary: 256 k-mer features)",
    "Phase 7 & 8: PCA & K-Means Clustering (Standardized mean-centering, PC variance ratio, Silhouette evaluation for k=7)",
    "Phase 9 & 10: Statistical Association (Chi-square permutation tests, Cramér's V, expected count diagnostics)",
    "Phase 11 & 12: Phylogenetics & Distance Heatmap (IQ-TREE 3 ModelFinder GTR+F+I+G4, 1000 UFBoot, evaluating tree-cluster consistency)"
])

def add_figure_slide(title, subtitle, fig1_name, fig2_name=None, text_card_title=None, text_card_bullets=None):
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, title, subtitle)
    
    fig1_path = os.path.join(fig_dir, fig1_name)
    if fig2_name:
        fig2_path = os.path.join(fig_dir, fig2_name)
        if os.path.exists(fig1_path):
            slide.shapes.add_picture(fig1_path, Inches(0.8), Inches(1.5), width=Inches(5.7))
        if os.path.exists(fig2_path):
            slide.shapes.add_picture(fig2_path, Inches(6.8), Inches(1.5), width=Inches(5.7))
    else:
        if os.path.exists(fig1_path):
            slide.shapes.add_picture(fig1_path, Inches(0.8), Inches(1.5), width=Inches(6.2))
        if text_card_title and text_card_bullets:
            add_card(slide, 7.3, 1.5, 5.2, 5.2, text_card_title, text_card_bullets)
    return slide

# SLIDE 6: Sequence QC
add_figure_slide("Sequence Quality Control (Length & GC Content)", "PHASE 3 — QUALITY CONTROL",
                 "fig01_sequence_length_distribution.png", "fig02_gc_content_distribution.png")

# SLIDE 7: Metadata Distribution
add_figure_slide("Geographic & Temporal Metadata Distribution", "PHASE 3 — METADATA DISTRIBUTION",
                 "fig03_samples_by_country.png", "fig04_samples_by_year.png")

# SLIDE 8: Multiple Sequence Alignment
add_figure_slide("Multiple Sequence Alignment (MAFFT)", "PHASE 4 — ALIGNMENT ANALYSIS",
                 "fig05_msa_summary.png", None,
                 "MAFFT Alignment Summary", [
                     "Alignment length: 2,156 bp across all 500 sequences.",
                     "Conserved Positions: 1,266 bp (58.72% of genome).",
                     "Variable / Polymorphic Sites: 890 bp (41.28%).",
                     "Parsimony-Informative Sites: 466 bp (21.61%).",
                     "Overall gap percentage: 7.24% across alignment matrix."
                 ])

# SLIDE 9: SNP Analysis
add_figure_slide("Genome Variation & SNP Density Analysis", "PHASE 5 — VARIATION PROFILING",
                 "fig06_variable_sites_snp_density.png", None,
                 "SNP Density & Variant Summary", [
                     "Identified 890 variable positions across PCV3 alignment.",
                     "SNP density analyzed in 50 bp sliding windows.",
                     "Highest variation observed in specific genomic regions corresponding to viral capsid (Cap) and replicase (Rep) genes.",
                     "All 890 variable positions exported to table01_snp_positions_summary.csv for downstream feature extraction."
                 ])

# SLIDE 10: Feature Extraction
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Genome-Derived Feature Extraction Matrix", "PHASE 6 — FEATURE EXTRACTION")
add_card(slide10, 0.8, 1.5, 5.6, 5.2, "Primary Feature Matrix (SNP Matrix)", [
    "One-Hot / Binary encoding of 890 aligned variable nucleotide positions across all 500 sequences.",
    "Feature Expansion: 890 variable positions produce 2,067 binary features due to one-hot encoding of non-constant nucleotide states (A, C, G, T) per site.",
    "Captures exact nucleotide substitution patterns at every variable genomic locus.",
    "Used as the PRIMARY input matrix for PCA and K-Means clustering."
])
add_card(slide10, 6.8, 1.5, 5.6, 5.2, "Supplementary k=4 K-mer Matrix", [
    "Extracted 256 k-mer tetranucleotide frequencies (k=4) normalized by sequence length.",
    "Provides alignment-free complementary feature representation.",
    "Strict Isolation: Country, Region, and Year were STRICTLY EXCLUDED from feature matrices to prevent metadata leakage."
])

# SLIDE 11: PCA Analysis
add_figure_slide("Principal Component Analysis (PCA)", "PHASE 7 — DIMENSIONALITY REDUCTION",
                 "fig07_pca_explained_variance.png", "fig08_pca_country.png")

# SLIDE 12: Clustering Analysis
add_figure_slide("K-Means Clustering & Silhouette Evaluation", "PHASE 8 — UNSUPERVISED CLUSTERING",
                 "fig10_silhouette_scores.png", "fig11_pca_clusters.png")

# SLIDE 13: Cluster vs Geography
add_figure_slide("Cluster vs. Geographical Location Association", "PHASE 9 — GEOGRAPHICAL ASSOCIATION",
                 "fig12_cluster_country_heatmap.png", None,
                 "Geographical Statistical Test", [
                     "Constructed 7 x 9 Cluster x Country contingency table.",
                     "Chi-square Statistic: 525.36 (dof = 48).",
                     "Asymptotic p-value: 1.56e-81.",
                     "Monte Carlo Permutation p-value (5,000 perms): p = 0.0002.",
                     "Cramér's V = 0.4185 (Strong geographical association).",
                     "Diagnostics: 50.8% of cells had expected count < 5; permutation test confirms validity.",
                     "Caution: Statistical association does NOT prove geographical transmission routes, origin, or causal divergence."
                 ])

# SLIDE 14: Cluster vs Year
add_figure_slide("Cluster vs. Collection Year Association", "PHASE 10 — TEMPORAL ASSOCIATION",
                 "fig13_cluster_year_heatmap.png", None,
                 "Temporal Association Test", [
                     "Grouped collection years into 4 temporal bins (<2015, 2015-17, 2018-20, 2021-25).",
                     "Chi-square Statistic: 145.50 (dof = 18).",
                     "Asymptotic p-value: 5.54e-22.",
                     "Monte Carlo Permutation p-value (5,000 perms): p = 0.0002.",
                     "Cramér's V = 0.3114 (Moderate-to-strong temporal association).",
                     "Temporal grouping prevents sparse cell count distortions.",
                     "Caution: Statistical association does NOT prove temporal origin or molecular clock evolutionary rates."
                 ])

# SLIDE 15: Phylogenetics
add_figure_slide("Maximum Likelihood Phylogenetic Tree (IQ-TREE 3)", "PHASE 11 & 12 — PHYLOGENETICS",
                 "fig14_phylo_tree_country.png", "fig15_phylo_tree_year.png")

# SLIDE 16: Genetic Distance
add_figure_slide("Pairwise Genetic Distance Heatmap", "PHASE 13 — GENETIC DISTANCE",
                 "fig16_genetic_distance_heatmap.png", None,
                 "Genetic Distance Metrics", [
                     "Computed pairwise nucleotide p-distances across aligned PCV3 genomes.",
                     "Mean Pairwise Distance: 0.0117 (1.17% mean nucleotide divergence).",
                     "Max Pairwise Distance: 0.0489 (4.89% maximum divergence).",
                     "High sequence conservation observed across global PCV3 isolates, consistent with single-stranded circular circovirus genomes."
                 ])

# SLIDE 17: Integrated Findings & Limitations
slide17 = prs.slides.add_slide(blank_layout)
add_header(slide17, "Integrated Synthesis & Study Limitations", "PHASE 14 — INTEGRATED ANALYSIS")
add_card(slide17, 0.8, 1.5, 5.6, 5.2, "Integrated Findings", [
    "Genome Variation: 890 variable sites define PCV3 genomic divergence.",
    "Unsupervised Grouping: PCA and K-Means Silhouette analysis identify 7 distinct genomic clusters.",
    "Geographic & Temporal Trends: Clusters display strong statistical association with country (V=0.4185) and temporal period (V=0.3114).",
    "Phylogenetic Consistency: The phylogenetic tree structure was broadly consistent with the K-Means genomic clustering patterns."
])
add_card(slide17, 6.8, 1.5, 5.6, 5.2, "Study Limitations", [
    "Sampling Imbalance: High sample counts from China (117), USA (69), Spain (57), South Korea (51) vs single isolates from Sweden/Mexico.",
    "Metadata Inconsistencies: 16 records in Excel had conflicting regions (Spain vs Poland); 10 were absent from Excel.",
    "Causality Constraint: Statistical association does NOT prove geographical transmission routes, origin, or functional virulence alterations."
])

# SLIDE 18: Conclusion & References
slide18 = prs.slides.add_slide(blank_layout)
add_header(slide18, "Conclusion & Key References", "SUMMARY & CONCLUSION")
add_card(slide18, 0.8, 1.5, 5.6, 5.2, "Summary Conclusions", [
    "PCV3 maintains a highly conserved circular genome (1.17% mean divergence) with clear SNP-defined sublineages.",
    "Unsupervised ML successfully partitions genomic variation without metadata bias.",
    "Observed sequence patterns are significantly associated with geographical location and collection year.",
    "Complete pipeline and figures are fully reproducible."
])
add_card(slide18, 6.8, 1.5, 5.6, 5.2, "Key References", [
    "Phan TG, et al. (2016). Detection of a novel circovirus PCV3 in pigs with cardiac and multi-systemic inflammation. Virology.",
    "Stadejek T, et al. (2020). Global transcriptional and phylogenetic analysis of PCV3. PLOS ONE.",
    "Franzo G, et al. (2020). Porcine circovirus 3 phylodynamics and evolutionary rate. Scientific Reports.",
    "Minh BQ, et al. (2020). IQ-TREE 2: New models and efficient algorithms for phylogenomics. Mol Biol Evol."
])

prs.save(out_pptx)
print(f"PowerPoint presentation generated successfully with refined scientific wording: {out_pptx}")
