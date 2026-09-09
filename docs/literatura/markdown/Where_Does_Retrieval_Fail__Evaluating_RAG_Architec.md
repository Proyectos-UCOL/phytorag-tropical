Where Does Retrieval Fail? Evaluating RAG

Architectures for Agricultural Advisory

Khan Raiyan Ibne Reza
Sanjana Aktar Maria
Sumaiya Tabassum Nimi
North South University

Dhaka, Bangladesh
raiyan.reza, sanjana.maria, sumaiya.nimi@northsouth.edu

## Abstract



Retrieval quality in RAG systems is commonly reported
as a single aggregate score, which can hide large differences across query types and language conditions. We study
this problem in Bengali agricultural advisory, where farmer
queries are often colloquial while official advisory documents use formal scientific terminology. We construct a test
collection of 1,000 queries and 2,882 knowledge nodes extracted from 284 official Bangladeshi agricultural publications, and use it to evaluate five retrieval architectures and
six embedding models under three controlled language conditions.

The results show that no single retrieval method is
consistently best. For native Bengali queries, BM25 is the
strongest single retriever (R@10=0.506) while Hybrid RRF
reaches the highest overall R@10 of 0.539. However, dense
retrieval performance varies sharply by query type: R@10
is 0.093 on colloquial farmer queries and 0.970 on formal
safety queries. Across language conditions, BM25 R@10
drops from 0.506 on Bengali queries to 0.004 when English
queries are matched against the Bengali corpus, while dense
retrieval falls only from 0.464 to 0.425. We also find that
embedding task configuration and passage length can each
change reported R@10 by a factor of seven, independent
of architecture. These results show why low-resource RAG
evaluation should report performance by language condition and query type rather than relying on aggregate scores
alone. The dataset and evaluation scripts are available at
https://huggingface.co/datasets/RaiyanKhaan/AgriTrustRAG.

Keywords

Bengali, low-resource retrieval, RAG, agricultural advisory, benchmark, dense retrieval, BM25, hybrid fusion,
cross-lingual retrieval, multilingual evaluation, embedding
configuration

1
Introduction
1.1
Motivation and Gap

Retrieval-Augmented Generation (RAG) systems are increasingly deployed in domain-specific settings, yet evaluated almost exclusively on English benchmarks. Bengali
agricultural advisory is a useful test case: with 237 million speakers [2], advisory queries use colloquial farmer
language while authoritative source documents use formal scientific Bengali. This register gap challenges lexical
and dense retrieval in opposing ways, and the stakes are
concrete: 200 of the benchmark’s 1,000 queries cover safetycritical content (pesticide dosage, off-label chemical use),
where a retrieval failure has real-world consequences.

Existing retrieval benchmarks (BEIR [20], CRAG [23])
are English-only; multilingual collections like MIRACL [27]
and Mr. TyDi [26] do not target agricultural advisory or
query-register variation. Prior Bengali RAG systems translate queries before retrieval [6] or do not isolate the retrieval
layer [12], while the closest agricultural resource [15] is
not a retrieval-only benchmark with provenance-level gold
labels or controlled cross-lingual conditions.

1.2
The Benchmark Collection

Unlike existing retrieval benchmarks that pair text chunks
with aggregate scores, our benchmark is designed around
six properties that form its benchmark design: traceable
retrieval units, structured canonical nodes rather than raw
text, full document traceability, a controlled multilingual
protocol, agricultural domain grounding, and registeraware evaluation covering both farmer queries and formal
queries. The benchmark consists of: (i) 284 source PDFs
from five Bangladeshi government and research organizations; (ii) 2,882 knowledge nodes (1,022 image-linked),
each a traceable retrieval unit; (iii) a knowledge graph of
19,768 entities and 17,501 factual triples; (iv) 1,000 queries
(900 answerable) across three categories (farmer-anchored,
KG-grounded, safety), with gold-node mappings verified
by three independent annotators (Fleiss’ 𝜅=0.72); and (v)
an evaluation harness implementing strict document-level
gold matching, bootstrap confidence intervals, and an
embedding API configuration audit.

1

arXiv:2608.14886v1  [cs.CL]  14 Aug 2026

---

Khan Raiyan Ibne Reza
Sanjana Aktar Maria
Sumaiya Tabassum Nimi

Evaluating on this collection reveals four key findings,
summarized in the abstract and developed in full in Section 5, with analysis of these patterns in Section 6.

1.3
Contributions

## 1. Benchmarking collection. A rigorous test collection

for low-resource Bengali agricultural retrieval, covering 284 authoritative documents, 2,882 knowledge
nodes, 19,768 entities, 17,501 triples, and 1,000 annotated
queries (available at https://huggingface.co/datasets/
RaiyanKhaan/AgriTrust-RAG).
2. Canonical node representation. A layered retrieval
unit uniting natural-language content, structured facts,
and deterministic source metadata via bounded, schemaguided extraction.
3. Evaluation harness & audit protocol. A reproducible
framework implementing strict gold matching, bootstrap
confidence intervals, and an embedding API configuration audit.
4. Benchmark validation via systematic diagnosis.
Evaluation across five architectures, six embedding
models, and three language conditions demonstrates
that the benchmark’s register- and script-stratified
design surfaces failure modes invisible to aggregate,
single-condition evaluation.

2
Related Work
2.1
IR and RAG Evaluation Benchmarks

Standard RAG evaluation benchmarks such as BEIR [20],
RAGBench [3], GaRAGe [18], and CRAG [23] are built
almost entirely in English; recent extensions such as T2RAGBench [19] target text-and-table retrieval in financial
documents, not the provenance-grounded, low-resource
domain advisory setting we address. Multilingual retrieval
benchmarks such as MIRACL [27] (18 languages) and Mr.
TyDi [26] extend evaluation to diverse languages, but none
enable controlled architecture-isolated retrieval evaluation
with provenance grounding in a low-resource agricultural
setting. Standard benchmarks typically emphasize aggregate accuracy scores, concealing subgroup failure across
query registers, a limitation highlighted by concurrent
work on stratified retrieval evaluation [10].

2.2
Retrieval in Low-Resource Languages

Dense retrieval often degrades outside high-resource languages due to tokenization fragmentation and language
bias [5, 11, 24]. Cross-lingual DPR shows modest gains [22],
while multi-vector late-interaction models such as ColBERT [9] improve fine-grained token matching.

Table 1: Positioning of our benchmark relative to closest prior benchmarks and systems.

Resource
Low-res.
Arch.
Retr.
CrossProv.
lang.
isolated
only
lingual
ground.

BEIR [20]
✗
✓
✓
✗
✗
CRAG [23]
✗
✗
✗
✗
✗
MIRACL [27]
✓
✗
✓
✓
✗
Mr. TyDi [26]
✓
✗
✓
✓
✗
Amharic study [24]
✓
✗
✓
✗
✗
Cross-lingual RAG [6]
✓
✗
✗
✓
✗
Prior advisory benchmark [15]
✓
✗
✗
✗
✓
KinyaColBERT [13]
✓
✗
✓
✗
✗
This work
✓
✓
✓
✓
✓
Low-res. lang. = targets a low-resource language; Arch. isolated = evaluates
multiple retrieval architectures in isolation from generation; Retr. only =
a retrieval-only benchmark, with no downstream QA/generation layer required; Cross-lingual = includes a controlled cross-lingual query condition;
Prov. ground. = gold labels are grounded in document-level provenance
metadata.

In agricultural RAG, KinyaColBERT [13] attributes low
accuracy in Kinyarwanda to vocabulary coverage over architecture choice. Query-document vocabulary mismatch is
an established retrieval challenge across domains, from general human-system communication [4] and cross-genre retrieval [7] to medical consumer health search [25], where
lay queries routinely diverge from the formal vocabulary of
the documents they need to retrieve.

In Bengali, BenLLM-Eval [8] and TigerLLM [14] evaluate LLM capabilities, while KrishokBondhu [1] automates
voice advisory and Farmer.Chat [17] extends AI-powered
advisory to smallholder farmers across multiple languages.
Closest to our setting, our own prior work [15] provides
a QA generation dataset, and Hossain et al. [6] translate
queries before retrieval. Unlike these generation-focused efforts, our work establishes a retrieval-only benchmark to
isolate retriever architecture performance under controlled
register and language shifts.

As summarized in Table 1, our benchmark is among
the first to combine a low-resource language, architectureisolated evaluation, retrieval-only measurement, controlled
cross-lingual conditions, and provenance-grounded gold
labels in a single design. For example, while MIRACL
and Mr. TyDi provide diverse multilingual datasets, their
standard evaluations do not isolate retrieval architectures
across controlled intra-language register shifts (marked ✗
for Arch. isolated).

3
The Benchmark Collection

We construct the benchmark around three requirements
(Figure 1): (i) document-level provenance, so every retrieval
decision traces to a single source; (ii) knowledge-graph
grounding, so queries are verified against structured facts
instead of free text; and (iii) independent verification of

2

---

Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory

node quality and query-document mappings, not gold
labels accepted from a single automated pass.

3.1
Source Materials

We collect 284 Bengali agricultural PDFs from five government and research organizations (BRRI, IRRI, DAE, SRDI,
MoA). The Ministry of Agriculture (MoA) and its extension
arm (DAE) jointly contribute approximately 65% of the corpus via national farming handbooks, while specialized institutes (BRRI, IRRI, SRDI) supply targeted diagnostic manuals. Many source documents contain scanned pages, complex layouts, tables, and embedded figures. We therefore
convert each PDF into page-level Markdown using a layoutpreserving OCR pipeline based on Mistral OCR, retaining
document structure and page provenance for subsequent
node construction. The resulting Markdown corpus (2,680
section-level passages) serves solely as an intermediate preprocessing artifact. While 73% of this underlying raw text
originates from our own prior QA benchmark [15], this
work’s primary contribution is restructuring this text into a
novel, provenance-grounded knowledge graph (100% of KG
entity and triple construction, node schema, and the full 900query gold-mapping are new; only the underlying text and
colloquial queries are inherited), establishing a dedicated retrieval benchmark where prior work left retrieval for future
evaluation.

Corpus Diversity. To ensure robust retrieval evaluation
across the agricultural long tail, the extracted corpus spans
25 years of publications (1999 to 2024) encompassing five
major document genres: national farming handbooks, diagnostic manuals, pesticide whitelists, recommendation
cards, and extension guides. The resulting entity graph
explicitly indexes 915 unique crops (spanning horticulture,
agroforestry, and aquaculture), 704 disease variants, and
2,729 chemical or pesticide entities.

3.2
Canonical Knowledge Node
Construction

Each knowledge node is a provenance-preserving retrieval
unit spanning three layers: natural-language content, structured agricultural facts, and provenance (source, page, organization). Generation is bounded, not open-ended: extraction is constrained to information explicitly present in the
source text, and provenance fields are injected deterministically, not model-generated. A representative node is given
in Appendix B; the full extraction and generation prompts
are detailed in Appendix D.

Deterministic Provenance Injection. Citation metadata
(publisher, source document, page range) is never LLMgenerated: the generation prompt structurally forbids the
model from producing citation fields, which are instead

injected by a separate deterministic script directly from
Markdown trace comments. This decouples provenance
from semantic generation, making citation hallucination
(fabricated page numbers or source names) structurally impossible rather than merely unlikely. A separate post-hoc
verification pass cross-checks every extracted crop and
entity mention against the source Markdown text, flagging
any node whose entities do not appear in its cited passage
for correction.

Chunking. We segment text into 2,882 topic-coherent
knowledge nodes, each corresponding to a single agricultural concept. Nodes average ≈1,180 characters, reflecting
natural concept boundaries rather than fixed token windows, and are distributed across a 13-category agricultural
taxonomy, ranging from Variety (695 nodes) and Cultivation Practice (570) down to a long tail such as Food Safety
(18).

Entity and Triple Extraction. We extract 19,768 entities
(6.9/node) and 17,501 factual triples via schema-guided,
bounded open information extraction. Per-node entity
coverage exceeds 96%.

Source-Grounded Automated Verification. Node content
(summary, symptoms, management, entities) was generated
by Gemini-3.1-Flash-Lite from the source Markdown into
a structured JSON schema. Each generated node was then
independently verified by a separate model, GPT-5-Nano,
which received both the node and its ground-truth source
passage and scored the pair (0–5) along four criteria: faithfulness (every claim traceable to the source text), completeness, hallucination (unsupported content not present in
source), and crop/entity relevance. Using a separate model
for generation and verification reduces self-confirmation
bias. Because the verifier sees the source passage, not just
the node in isolation, its check is constrained to factual
consistency and never becomes an open-ended quality
rating. Across the resulting graph, entity coverage is 96.1%
(2,771 of 2,882 nodes contain at least one extracted entity)
and factual triple coverage reaches 100%.

Closed-Loop Refinement. Nodes falling below threshold
(≤3 on any dimension; 283 of 2,882 nodes, 9.8%) were
returned to Gemini-3.1-Flash-Lite together with the verifier’s specific error trace and regenerated against the
same source passage, then re-verified. This repeated until
each node passed threshold, yielding the final 2,882-node
collection without discarding agricultural content.

Human Audit. Because the automated stage already enforces source-level faithfulness, human review targeted a
layer the automated check is not designed to catch: domainappropriate terminology and information completeness under compression, judgments requiring agricultural expertise

3

---

Khan Raiyan Ibne Reza
Sanjana Aktar Maria
Sumaiya Tabassum Nimi

Figure 1: Canonical knowledge node construction
pipeline. Source documents are parsed, chunked by
topic, and processed into structured, provenancegrounded JSON nodes.

beyond simple text-source comparison. Three expert agricultural annotators independently evaluated a stratified random sample of 200 nodes on two dimensions: information
completeness (critical dosage/withholding details dropped
under compression) and technical terminology (formal Bengali agricultural terms vs. code-mixed transliterations). Annotators reached strong agreement (Fleiss’ 𝜅=0.81); 12 of
200 nodes (6.0%) fell below consensus threshold and were
corrected via direct manual edit against the source Markdown. Each node remains linked to its originating Markdown passage through deterministic provenance metadata,
while image-containing nodes continue through the multimodal extension described in §3.3.

3.3
Image-Linked Nodes

Of the 2,882 canonical knowledge nodes, 1,022 (35.5%)
additionally carry a linked visual asset (a diagnostic photograph, variety chart, or table-image) captured via an
image_refs field on the same text node, under the identical provenance schema (publisher, source_document,
source_pages) as the node’s textual content. Each image
reference additionally carries a figure-type label (one of 12
categories, e.g., symptom_close_up, variety_portrait,

procedure_illustration) and a bilingual visual description (visual_description_en/bn) generated by a
vision-language model, textualizing symptom color, shape,
and texture rather than requiring a dedicated vision encoder at retrieval time. These fields extend the schema in
Appendix C but, like the image reference itself, are not
separately indexed or evaluated in the present retrieval
experiments (§5).

This image-to-text linkage is motivated directly by the
register gap identified in §6.1. Because farmer queries
disproportionately describe visually observable symptoms
(“leaves turning yellow”) instead of the formal entity names
(Tungro virus) used in source documents, image-linked
nodes are the natural mechanism by which a future system
could close exactly the severe retrieval gap this benchmark
exposes (R@10=0.093 on farmer queries), rather than acting
as a general-purpose multimodal extension. We report their
structure in Appendix C and leave dedicated visual retrieval
to future work (§7.2).

3.4
Query Benchmark

The benchmark contains 1,000 queries across three categories (Table 2).

Farmer-anchored. 400 farmer-anchored queries adapted
from our own prior QA benchmark [15]. After threeannotator independent gold-node mapping, 300 achieved
majority-vote consensus and are retained as answerable;
the remaining 100 lacked majority-vote agreement among
annotators (Fleiss’ 𝜅for this subset: <0.4) and are excluded
from retrieval evaluation. These 100 excluded queries constitute the low-agreement subset; disagreement may reflect
ambiguous queries or multiple valid gold documents rather
than strict unanswerability.

KG-grounded (400). 400 queries constructed directly
from knowledge-graph triples (e.g., [crop, has_disease, disease_name]), targeting multi-hop relational retrieval. All
400 are verified by three annotators (Fleiss’ 𝜅=0.78) and
included in the answerable set.

Safety (200). All 200 queries test advisory failure modes
(pesticide dosage, off-label chemical use, dangerous agronomic advice), each with a verified gold document. Safety
queries use formal, precise language (chemical product
codes, BRRI variety names) that closely mirrors document
vocabulary: they show 1.6× higher lexical overlap with
their gold document than farmer queries (§6.1), consistent
with their high retrievability in §5.3. All 200 are answerable
and included in the 900-query evaluation set.

Independent Verification. Farmer-anchored and safety
queries were mapped by three annotators (Fleiss’ 𝜅= 0.72,
𝑛=600). Majority vote determines the gold node; queries
without majority agreement are excluded. KG-grounded

4

---

Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory

Table 2: Benchmark dataset statistics.

Property
Value

Source PDFs
284
Organizations
5 (BRRI, IRRI, DAE, SRDI, MoA)
KG nodes
2,882
Image-linked nodes
1,022 (35.5%)
Unique entities
19,768
Factual triples
17,501

Queries (total generated)
1,000
Farmer-anchored (answerable)
300
Farmer-anchored (low-agreement)
100
KG-grounded (answerable)
400
Safety-critical (answerable)
200
Answerable evaluation set
900

Inter-annotator 𝜅(farmer+safety)
0.72
Inter-annotator 𝜅(KG-grounded)
0.78
Entity coverage
>96%

gold nodes (400 queries) were assigned by a domain expert
annotator and independently validated by three native
Bengali-speaking annotators who evaluated each assignment on factual grounding, faithfulness, and relevance
(Fleiss’ 𝜅=0.78, 𝑛=400). The final benchmark contains 900
answerable queries (300 farmer + 400 KG + 200 safety);
the 100 excluded farmer queries are withheld as a lowagreement subset.

3.5
Cross-Lingual Conditions
To isolate language as an explanatory variable independent of retrieval architecture, we translate both the full
query set and all 2,882 KG nodes into English, guided by a
domain-specific agricultural glossary (312 domain-critical
terms, cross-referenced against NCBI Taxonomy; 97%
back-translation equivalence on a 100-query spot check)
to preserve technical terminology. This produces three
controlled conditions on an otherwise identical benchmark:
Bengali queries against the Bengali KB (BN→BN), English
queries against the Bengali KB (EN→BN, cross-lingual),
and English queries against the translated English KB
(EN→EN). Because the corpus content and evaluation procedure are held constant across conditions, the comparison
isolates the effect of changing the language condition as
closely as possible.

4
Experimental Design

We evaluate five architectures and six embeddings not to
advance retrieval methodology, but because architectureisolated evaluation is itself part of the benchmark’s
contribution (§2). Our evaluation is designed to isolate
whether retrieval behavior is primarily determined by architecture, embedding model, or language condition. This

approach reveals failure modes that remain invisible to
single-architecture or aggregate-only evaluations. We organize primary experiments around four research questions:
which architecture leads in Bengali (RQ1); whether this
depends on the language boundary (RQ2); whether query
type moderates performance (RQ3); and how embedding
choice affects results (RQ4). We additionally conduct a
configuration audit to verify that architecture comparisons
are not artifacts of implementation settings. Analysis of
observed failures is in §6.

4.1
Retrieval Architectures

We evaluate five representative retrieval systems spanning
four retrieval families: (i) BM25 [16] uses Okapi weighting (𝑘1=1.5, 𝑏=0.75) with character bigram plus full-word
tokenization; (ii) Dense (Gemini) uses 𝐿2-normalized
3,072-dim gemini-embedding-001 vectors with exact
inner-product search (FAISS IndexFlatIP) and asymmetric
task types; (iii) Dense (BGE-M3 Native) uses 1,024-dim
native dense embeddings as an open, retrieval-specific
baseline; (iv) ColBERT [9] applies BGE-M3 multi-vector
scoring at 512-token passage granularity (to match the
dense baselines’ context window) with MaxSim; and (v)
Hybrid RRF fuses BM25 and Gemini dense rankings via
Reciprocal Rank Fusion (𝑘=60, top-100 candidates each). All
architectures retrieve from the identical 2,882-node benchmark corpus introduced in §3; only the retrieval mechanism
differs. Full configuration settings are in Appendix A.

4.2
Embedding Robustness

To separate architectural effects from embedding quality,
we evaluate six models spanning 384–4,096 dimensions (Table 6) on the same Bengali query set under identical retrieval
code, isolating embedding choice as the only varying factor.

4.3
Metrics

Retrieval (L1). We report R@1, R@5, R@10 (hereafter R@k),
MRR, and nDCG@10 against gold source nodes for the 900
answerable queries. A retrieved node counts as a hit only
if its exact node identifier matches the provenance-verified
gold node (serving as the strict retrieval document): a deterministic criterion admitting no partial credit. For context, the random baseline R@10 for a corpus of this size is
10/2,882 ≈0.003.
Separation score. Beyond Recall@𝑘, we measure how
well embeddings separate the gold node from the remainder of the corpus. For query 𝑞𝑖with gold node 𝑔𝑖, let
𝑠gold = cos(𝐸(𝑞𝑖), 𝐸(𝑔𝑖)) and 𝑠neg be the mean cosine similarity between 𝐸(𝑞𝑖) and all 2,881 non-gold nodes. The
separation score is the mean difference (𝑠gold −𝑠neg) across
all 𝑁evaluated queries. A score of zero indicates random

5

---

Khan Raiyan Ibne Reza
Sanjana Aktar Maria
Sumaiya Tabassum Nimi

Table 3: L1 Retrieval on 900 Answerable Bengali
Queries (BN→BN). Bold = best overall; underline =
best single-method.

Architecture
R@1
R@5
R@10
MRR
nDCG@10

Hybrid RRF (Gemini+BM25)
.291
.466
.539
.551
.461
BM25 (Sparse)
.205
.405
.506
.481
.407
Dense (Gemini-001)
.320
.431
.464
.514
.431
Dense (BGE-M3 Native)
.281
.369
.408
.432
.370
ColBERT (BGE-M3)‡
.255
.414
.487
.324
.416
‡ ColBERT evaluated at max_seq_length=512, matching the dense baselines’ context window.

ranking behaviour; negative values indicate the gold node
ranks below the corpus average.

4.4
Statistical Validation

We compare retrieval architectures using BCa bootstrap
confidence intervals (10,000 resamples). Pairwise significance is assessed via paired Wilcoxon signed-rank tests
with Holm-Bonferroni correction across 10 architecture
pairs in Table 3; per-category and per-embedding tables are
reported descriptively. Significance levels (𝑝< 0.001 for
BM25 vs. Dense; 𝑝< 0.01 for Hybrid RRF) and 95% CIs are
reported inline in §5.1.

5
Results
Each subsection answers one research question using the
900 answerable Bengali queries unless otherwise noted. All
reported numbers are from the post-audit verification run;
Section 6 discusses the observed failure patterns.

5.1
RQ1: Benchmark Difficulty and
Architecture Comparison

Table 3 presents R@10 across 900 answerable Bengali
queries
(random
baseline
R@10≈0.003).
Hybrid
RRF
achieves the highest overall R@10 (0.539): lexical and
dense signals provide complementary coverage. Among
single-method retrievers, BM25 leads (R@10=0.506, 95%
CI: [0.474, 0.538]), outperforming dense Gemini-001 (0.464,
95% CI: [0.432, 0.497]) by 9% (𝑝< 0.001, Wilcoxon signedrank test). Late-interaction ColBERT (BGE-M3, 512 tokens)
reaches R@10=0.487, outperforming both single-vector
dense variants (0.464, 0.408). Broken out by query category (Table 5), ColBERT is the best single architecture on
KG-grounded queries (R@10=0.600, vs. Dense 0.489, BM25
0.478) and reduces the gap on farmer queries relative to
Dense (0.210 vs. 0.093).

Table 4: Cross-Lingual Comparison (95% BCa CIs for
R@10 in brackets; 900 queries).

Setting
Dense (Gemini)
BM25
Winner

Bengali (BN→BN)
.464 [.43, .50]
.506 [.47, .54]
BM25 (+9%)
Cross-lingual (EN→BN)
.425 [.39, .46]
.004 [.00, .01]
Dense (≈100×)
English (EN→EN)
.442 [.41, .47]
.384 [.35, .42]
Dense (+15%)

Table 5: R@10 by query category (95% BCa CIs
in
brackets;
900
verified
queries;
Farmer=300,
Safety=200, KG-grounded=400).

Architecture
Farmer
Safety
KG-Ground.
Farm.+Safe.
(colloquial)
(formal)
(formal)
(combined)

Dense (Gemini)
.093 [.06,.13]
.970 [.94,.99]
.489 [.44,.54]
.444 [.40,.49]
BM25
.523 [.47,.58]
.539 [.47,.60]
.478 [.43,.53]
.529 [.48,.57]
ColBERT (BGE-M3)‡
.210 [.17,.26]
.675 [.60,.74]
.600 [.55,.65]
.396 [.35,.44]

5.2
RQ2: Is architectural failure
determined by language mismatch?

Table 4 examines whether language boundary crossing
changes retrieval behaviour independent of architecture.
Within the same language, BM25 leads in Bengali (0.506 vs.
0.464) while Dense leads in English (0.442 vs. 0.384): neither
architecture is universally dominant. The results diverge
markedly in the cross-lingual setting (English queries →
Bengali corpus), where BM25’s exact lexical matching
declines sharply across script boundaries (R@10: 0.506 →
0.004, a 99% drop) and becomes effectively unusable. Multilingual dense embeddings, by contrast, largely preserve the
script boundary (R@10: 0.464 →0.425, only an 8% drop).
Architecture choice cannot be separated from the language
scenario it is deployed in.

5.3
RQ3: Does the query type moderate
retrieval performance?
Dense retrieval’s aggregate Bengali score masks large differences across query types (Table 5). Dense retrieval (Gemini)
performs poorly on colloquial farmer queries (R@10=0.093)
but reaches high R@10 on formal safety queries (0.970), a
difference driven entirely by query register. Safety queries
function as near-direct entity lookups, with little inferential gap to close between query and gold document (§6.1);
farmer queries instead require bridging the symptom-toentity register gap (§6.1). BM25 is comparatively stable
across categories: farmer (0.523), safety (0.539), KG (0.478).
On KG-grounded queries dense leads BM25 by a narrow
margin (0.489 vs. 0.478); BM25’s same-language advantage
over dense comes from consistent performance across colloquial and formal query types, in contrast to the large gap
between the two query types for dense retrieval.

6

---

Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory

Farmer
Safety
KG-grounded
0

0.2

0.4

0.6

0.8

1

R@10

Dense (Gemini)
BM25
ColBERT

Figure 2: R@10 by query register, plotted from Table 5.
Dense retrieval is sharply bimodal — it nearly fails
on colloquial farmer queries and saturates on formal
safety queries — while BM25 stays comparatively stable across registers.

Table 6: Multi-Embedding Analysis (95% BCa CIs for
R@10 in brackets; 900 queries, BN→BN). Random
baseline: separation = 0.

Model
Dim
Separation
R@10

Gemini-embedding-001
3,072
+0.127
.464 [.43,.50]
BGE-M3 (native proj.)
1,024
+0.133
.408 [.38,.44]
E5-Large (multilingual)
1,024
+0.037
.284 [.26,.32]
Qwen3 Embedding 8B
4,096
+0.108
.241 [.21,.27]
MPNet (paraphrase)
768
−0.010
.009 [.00,.02]
MiniLM (paraphrase)
384
−0.039
.005 [.00,.01]

5.4
RQ4: How do different embedding
models compare?

Evaluating six embedding models spanning 384–4,096 dimensions (Table 6) shows that retrieval-specific training
dominates model scale: Gemini-001 (0.464) and BGE-M3
(0.408) outperform larger models like Qwen3-8B (0.241).
Notably, BGE-M3 yields the highest mean cosine separation (+0.133 vs. Gemini’s +0.127) despite ranking second on
Recall@10 (.408 vs. .464); mean separation rewards models
with confident average alignment, whereas top-𝑘recall
penalizes a long tail of complete retrieval misses. Generalpurpose sentence-similarity encoders (MPNet, MiniLM)
fail (R@10 < 0.01), yielding negative separation scores that
indicate gold nodes are ranked below corpus average.

Configuration Audit. To verify that architecture comparisons are not implementation artifacts, we audited configuration sensitivity across embedding APIs and passage
granularity. Using a sentence-similarity task type instead of
the asymmetric RETRIEVAL_QUERY/RETRIEVAL_DOCUMENT
encoding reduced Gemini Dense R@10 from 0.464 to 0.063,
a 7× drop. Passage granularity is a second, independent

Table 7: Illustrative register gap: a farmer-anchored
query and its gold node (English glosses of Bengali
text in brackets).

Farmer query (colloquial): [My chickpea plants’ leaves are
turning yellow and drooping, what should I do?]
Gold node title: [Chickpea crop disease control and remedies]
(B7_CH2_CHHOLA_0006_N1)
Gold node entity: wilt disease (formal pathological term; not
present in query)
Token-level Jaccard: 0.03 (below 0.10 near-universal gap
threshold, §6.1)

configuration axis: at the field-standard default of 128 tokens, Bengali knowledge nodes (mean ≈1,180 characters)
are truncated by 95–99%, and ColBERT falls below even
the weaker dense baseline (R@10=0.376 vs. BGE-M3’s
0.408); increasing the context window to 512 tokens lifts
ColBERT to R@10=0.487 (Table 3), reversing this ranking.
Two independent default settings each changed reported
architecture rankings by a wide margin. Configuration
auditing should therefore precede architecture comparison
in low-resource retrieval settings. Full configuration details
are in Appendix A.

6
Analysis of Retrieval Failures

This section explains the performance patterns from Section 5 through two lenses: the query-document register
gap (§6.1), and the complementary failure patterns between
BM25 and dense retrieval (§6.2).

6.1
Register Gap Analysis

Token-level Jaccard similarity across all 900 query-gold
pairs reveals a near-universal lexical gap: 96.4% of queries
have Jaccard < 0.10 with their gold document (mean: 0.044;
maximum: 0.172). This confirms that benchmark evaluation
requires semantic matching, not direct surface overlap.

However, surface overlap varies substantially across
query registers: safety queries achieve a mean Jaccard of
0.055 vs. 0.034 for farmer queries (1.6× higher alignment).
Verbatim entity inspection explains dense retrieval’s collapse on colloquial farmer queries (R@10=0.093): only 3.5%
of gold document entity names appear verbatim in farmer
queries, while 92% are entirely absent. Farmers describe
observable symptoms (“leaves turning yellow”), whereas
authoritative documents encode formal scientific entities
(Tungro virus) (illustrated in Table 7). Safety queries use
precise chemical codes and variety names that closely
match document vocabulary, so dense retrievers achieve
high accuracy (0.970) on this category.

7

---

Khan Raiyan Ibne Reza
Sanjana Aktar Maria
Sumaiya Tabassum Nimi

6.2
Failure Complementarity and Hybrid
Attribution

Hybrid RRF’s gain over either single-method retriever is explained by complementary failure patterns between BM25
and Dense retrieval at the category level (Table 5). BM25
is comparatively stable across query registers (farmer 0.523,
safety 0.539, KG-grounded 0.478), while Dense is sharply bimodal (farmer 0.093, safety 0.970). Because the two architectures reach their strongest and weakest performance on
largely different query registers, fusing their rankings recovers queries that either method alone would miss, consistent with Hybrid RRF’s overall gain over both single methods (R@10=0.539 vs. 0.506 and 0.464). Persistent shared difficulty concentrates in colloquial farmer queries and multihop KG-grounded queries, where neither lexical nor semantic matching reliably surfaces the gold document, consistent with the symptom-to-entity register mismatch identified above as the primary barrier in low-resource retrieval.

7
Discussion
7.1
Methodological Implications

Evaluating low-resource retrieval with aggregate scores
alone hides important failure modes. Dense retrieval R@10
drops from 0.970 on formal safety queries to 0.093 on colloquial farmer queries, corroborating concurrent findings
on stratified retrieval evaluation [10]. Across language conditions, BM25 leads within Bengali while dense retrieval
leads under cross-lingual conditions. Our configuration
audit additionally shows that two independent default
settings, an embedding-API task type and passage-length
truncation, each changed reported architecture rankings
by a wide margin; configuration auditing should therefore
precede architectural evaluation [21].

7.2
Limitations and Ethics

Limitations. Evaluation is limited to agricultural advisory
and to first-stage zero-shot retrievers; learned sparse models (e.g., SPLADE) and cross-encoder rerankers are left to
future work. Machine-translated English queries may carry
subtle lexical shifts despite 97% back-translation equivalence on a 100-query random sample (§3.5); future work
should expand translation validation to the full corpus
to systematically characterize terminology preservation.
However, BM25’s near-total collapse under cross-lingual
querying (R@10=0.004) reflects an expected consequence
of exact lexical matching across non-cognate scripts, since
the cross-lingual condition compares English queries directly against the untranslated Bengali corpus; this result
is unlikely to be a translation artifact. Image-linked nodes
(Appendix C) attach a visual reference to a subset of text

nodes but are not separately embedded or evaluated as a distinct retrieval modality in this work. A human audit of 200
nodes found 12 requiring correction, so a small fraction of
unresolved failure queries may reflect annotation artifacts
in the benchmark itself. Source documents span 1999–2024.
The benchmark evaluates whether a retriever surfaces the
correct authoritative source document, not whether that
document’s recommendations remain current; deploying
any system built on this corpus for live advisory would
require a separate regulatory-currency check independent
of retrieval accuracy. Finally, while reliance on proprietary
APIs for initial query generation poses a reproducibility risk
as models deprecate, the resulting benchmark is released as
a static, version-controlled JSON corpus, supporting stable
retrieval evaluations over time.

Ethics and broader impact. Annotations were completed by three compensated domain-expert annotators
with informed consent. The benchmark evaluates retrieval performance to motivate model improvement in
low-resource domain advisory and contains no personally
identifiable information. Given the safety-critical query subset, retrieval accuracy does not certify advisory correctness
for unsupervised deployment; systems evaluated on this
benchmark should retain human oversight for high-stakes
recommendations.

8
Conclusion

We presented a provenance-grounded benchmark for
Bengali agricultural retrieval built from authoritative
government publications through canonical knowledge
nodes, image-linked resources, and register- and languagestratified evaluation. Beyond providing a reproducible
benchmark, our experiments show that retrieval behaviour
depends jointly on linguistic register, language boundary,
and implementation configuration rather than retrieval
architecture alone. These findings provide a stronger empirical basis for evaluating future low-resource retrieval and
RAG systems.

A
Reproducibility Checklist

• Data: 284 source PDFs, 2,882 knowledge nodes, 1,000
queries (900 with verified gold-node mappings; 100
low-agreement queries released for future work).
Available at https:
//huggingface.co/datasets/RaiyanKhaan/AgriTrust-RAG.
• BM25: Okapi (𝑘1=1.5, 𝑏=0.75), char-bigram + full-word
tokenization.
• Dense (Gemini): gemini-embedding-001, 3,072-dim,
asymmetric RETRIEVAL_QUERY/RETRIEVAL_DOCUMENT
task types.

8

---

Where Does Retrieval Fail? Evaluating RAG Architectures for Agricultural Advisory

• Dense (BGE-M3): Native projection head, 1,024-dim,
𝐿2-normalized.
• ColBERT: BGE-M3 multi-vector, 512-token sequence
length, MaxSim scoring.
• Hybrid RRF: Reciprocal Rank Fusion (𝑘=60, top-100
candidates per method).
• Audit Variants: sentence-similarity task type;
128-token passage truncation.
• Stats: BCa bootstrap (10,000 resamples), paired
Wilcoxon signed-rank tests with Holm-Bonferroni
correction.

B
Node Representation

A representative canonical knowledge node (trimmed; full
schema released with benchmark code), showing the threelayer structure (natural-language content, structured facts,
deterministic provenance):

{ "category": "disease",

"title_bn": "[Chickpea crop disease control and remedies]",
"summary": "[Guidance on wilt disease control via seed treatment,
variety selection, and infected plant management]",
"key_points": [
"[Treat seeds with Provex-200 WP at 2.5-3.0 g/kg rate]",
"[Grow resistant varieties: BARI Chickpea-5, -9, -10]"
],
"structured": {"symptoms": ["wilt disease"],
"management":
["seed
treatment
(Provex-200
WP)",
"fungicide
spray"],
"prevention": ["use resistant varieties"]},
"entities": {"chemicals": ["Provex-200 WP"],
"diseases": ["wilt disease"], "crops": ["chickpea"]},
"generation_model": "gemini-3.1-flash-lite",
"_provenance_layer": {"node_id": "B7_CH2_CHHOLA_0006_N1",
"publisher": "BARI",
"source_document": "krishiProjuktiHatboi_10.pdf",
"source_pages": [112, 112]} }

Field values in brackets are English translations of the stored UTF-8
Bengali text.

C
Image-Linked Node Structure

Nodes with a linked visual asset extend the standard schema
(Appendix B) with an image_refs field, without introducing a separate node type:

{ ...

"image_refs": [
{ "caption_en": "[Chickpea leaf showing early wilt symptoms]",

"image_type": "diagnostic_photo" }
], ... }

All other fields (node_id, category, title_bn, _provenance_layer)
are unchanged from the node shown in Appendix B.

In total, 1,022 of 2,882 nodes (35.5%) carry one or more
image references. Image references have not undergone the
three-annotator human audit (§3.2) applied to node text, and
we report them as a structural resource, not an independently verified evaluation asset (§7.2).

D
Node Extraction Protocol

The canonical nodes in the benchmark are constructed via
a two-stage generative pipeline bounded by deterministic
checks.

First, an automated extraction stage identifies critical entities (crops, diseases, agricultural chemicals) from the source
Markdown passage and stores them in a temporary registry.
The extraction prompt enforces exact surface-form matching and forbids hallucination:

### Strict Bounding: Extract ONLY entities explicitly mentioned in
the text. Do not infer or add external knowledge. If a category is
missing, return an empty list.
### Surface Form: Extract the verbatim string exactly as it appears
in the Bengali text.
### Categories: "crops", "diseases_and_pests", "chemicals".
### Output: Emit a valid JSON object ONLY.

Second, the Markdown passage is converted into structured JSON node(s) by Gemini-3.1-Flash-Lite. Following
generation, a deterministic script verifies that the entities
extracted in Stage 1 exactly match those present in the generated node. Provenance metadata is then injected purely
deterministically. The abridged generation instruction
enforces 1-to-N dynamic chunking and semantic bounding:

### Strict Domain Bounding: The generated node(s) must only contain
information from the specific .md document provided... Never claim
a crop or topic that the trace and body do not support.
### Faithfulness: Every factual claim must come from the section
you were given. You do not add facts, doses, chemical names, or
yields from memory. If you cannot ground a field in the text, leave
it blank.
### How many nodes: One coherent topic →one node. Several distinct
sub-topics (separate varieties, a disease and its treatment) →one
node each. Each node must be a distinct, non-redundant unit.
###
Category:
Pick
the
single
best
from:
variety,
disease,
pest,
fertilizer,
cultivation_practice,
post_harvest,
seed_tech,
machinery, irrigation, ipm, cropping_system, food_safety, general.
### Schema Enforcement: Output a JSON array conforming to the
node
schema
with
fields
"title_bn",
"summary",
"key_points",
"structured", "entities".

## References



[1] Mohd Ruhul Ameen, Akif Islam, Farjana Aktar, and M Saifuzzaman

Rafat. 2026.
KrishokBondhu: A Retrieval-Augmented Voice-Based
Agricultural Advisory Call Center for Bengali Farmers. In 2026 IEEE
2nd International Conference on Quantum Photonics, Artificial Intelligence & Networking (QPAIN). IEEE, 1–6.
[2] David M. Eberhard, Gary F. Simons, and Charles D. Fennig. 2024.

Ethnologue: Languages of the World. https://www.ethnologue.com/
language/ben/. Online version.
[3] Robert Friel, Masha Belyi, and Atindriyo Sanyal. 2024.
Ragbench:
Explainable benchmark for retrieval-augmented generation systems.
arXiv preprint arXiv:2407.11005 (2024).
[4] George W. Furnas, Thomas K. Landauer, Louis M. Gomez, and Susan T.

Dumais. 1987. The vocabulary problem in human-system communication. Commun. ACM 30, 11 (1987), 964–971.
[5] Seongtae Hong, Youngjoon Jang, Jungseob Lee, Hyeonseok Moon,

and Heuiseok Lim. 2026. Improving semantic proximity in information retrieval through cross-lingual alignment. In The Fourteenth International Conference on Learning Representations.

9

---

Khan Raiyan Ibne Reza
Sanjana Aktar Maria
Sumaiya Tabassum Nimi

[6] Md Asif Hossain, Nabil Subhan, Mantasha Rahman Mahi, and Jan-

natul Ferdous Nabila. 2026. Cost-Efficient Cross-Lingual RetrievalAugmented Generation for Low-Resource Languages: A Case Study

in Bengali Agricultural Advisory.
arXiv preprint arXiv:2601.02065
(2026).
[7] Tomasz Jurczyk and Jinho D. Choi. 2017. Cross-genre Document Re-

trieval: Matching between Conversational and Formal Writings. In
Proceedings of the First Workshop on Building Linguistically Generalizable NLP Systems. Association for Computational Linguistics.
[8] Mohsinul Kabir, Mohammed Saidul Islam, Md Tahmid Rahman

Laskar, Mir Tafseer Nayeem, M Saiful Bari, and Enamul Hoque. 2024.
BenLLM-eval: A comprehensive evaluation into the potentials and
pitfalls of large language models on Bengali NLP. In Proceedings of
the 2024 Joint International Conference on Computational Linguistics,
Language Resources and Evaluation (LREC-COLING 2024). 2238–2252.
[9] Omar Khattab and Matei Zaharia. 2020. Colbert: Efficient and effec-

tive passage search via contextualized late interaction over bert. In
Proceedings of the 43rd International ACM SIGIR conference on research
and development in Information Retrieval. 39–48.
[10] Andrew Klearman, Radu Revutchi, Rohin Garg, Rishav Chakravarti,

Samuel Marc Denton, and Yuan Xue. 2026. Coverage, Not Averages:
Semantic Stratification for Trustworthy Retrieval Evaluation. arXiv
preprint arXiv:2604.20763 (2026).
[11] Seungyoon Lee, Minhyuk Kim, Seongtae Hong, Youngjoon Jang,

Dongsuk Oh, and Heui-Seok Lim. 2026. CLEAR: Cross-Lingual Enhancement in Retrieval via Reverse-training. In Proceedings of the 64th
Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 347–362.
[12] Noshin Nawal, Sanju Basak, and Rifat Shahriyar. 2024.
Effective
retrieval-augmented generation for open domain question answering in
bengali. Ph. D. Dissertation. Ph. D. dissertation.
[13] Antoine Nzeyimana and Andre Niyongabo Rubungo. 2025. Kinya-

ColBERT: A Lexically Grounded Retrieval Model for Low-Resource
Retrieval-Augmented Generation.
arXiv preprint arXiv:2507.03241
(2025).
[14] Nishat Raihan and Marcos Zampieri. 2025.
TigerLLM-a family of
Bangla large language models. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short
Papers). 887–896.
[15] Khan Raiyan Ibne Reza, Sumaiya Tabassum Nimi, and Omar-Ibne

Shahid. 2026. KrishokChat: A Provenance-Traceable Multi-Task Bengali Agricultural Benchmark with Safety-Critical Chemical Advisory.
In Proceedings of the 18th Conference of the European Chapter of the
Association for Computational Linguistics.
[16] Stephen Robertson and Hugo Zaragoza. 2009. The probabilistic rele-

vance framework: BM25 and beyond. Vol. 4. Now Publishers Inc.
[17] Namita Singh, Jacqueline Wang’ombe, Nereah Okanga, Tetyana Ze-

lenska, Jona Repishti, Jayasankar G K, Sanjeev Mishra, Rajsekar
Manokaran, Vineet Singh, Mohammed Irfan Rafiq, Rikin Gandhi, and
Akshay Nambi. 2024. Farmer.Chat: Scaling AI-Powered Agricultural
Services for Smallholder Farmers.
arXiv preprint arXiv:2409.08916
(2024).
[18] Ionut Teodor Sorodoc, Leonardo FR Ribeiro, Rexhina Blloshmi,

Christopher Davis, and Adrià de Gispert. 2025. Garage: A benchmark
with grounding annotations for rag evaluation. In Findings of the Association for Computational Linguistics: ACL 2025. 17030–17049.
[19] Jan Strich, Enes Kutay Isgorur, Maximilian Trescher, Chris Biemann,

and Martin Semmann. 2026. T2-RAGBench: Text-and-Table Aware
Retrieval-Augmented Generation. In Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers). 165–191.

[20] Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava,

and Iryna Gurevych. 2021.
Beir: A heterogenous benchmark for
zero-shot evaluation of information retrieval models. arXiv preprint
arXiv:2104.08663 (2021).
[21] Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Ma-

jumder, and Furu Wei. 2024. Multilingual E5 Text Embeddings: A
Technical Report. arXiv preprint arXiv:2402.05672 (2024).
[22] Jie Wu, Zhaochun Ren, and Suzan Verberne. 2024. What are the limits

of cross-lingual dense passage retrieval for low-resource languages?
arXiv preprint arXiv:2408.11942 (2024).
[23] Xiao Yang, Kai Sun, Hao Xin, Yushi Sun, Nikita Bhalla, Xiangsen

Chen, Sajal Choudhary, Rongze D Gui, Ziran W Jiang, Ziyu Jiang,
et al. 2024. Crag-comprehensive rag benchmark. Advances in Neural
Information Processing Systems 37 (2024), 10470–10490.
[24] Tilahun Yeshambel, Moncef Garouani, Serge Molina, and Josiane

Mothe. 2025. Dense Retrieval for Low Resource languages-the Case
of Amharic Language. In Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval.
3098–3100.
[25] Qing T. Zeng and Tony Tse. 2006. Exploring and developing consumer

health vocabularies. Journal of the American Medical Informatics Association 13, 1 (2006), 24–29.
[26] Xinyu Zhang, Xueguang Ma, Peng Shi, and Jimmy Lin. 2021. Mr. TyDi:

A multi-lingual benchmark for dense retrieval. In Proceedings of the
1st workshop on multilingual representation learning. 127–137.
[27] Xinyu Zhang, Nandan Thakur, Odunayo Ogundepo, Ehsan Kamal-

loo, David Alfonso-Hermelo, Xiaoguang Li, Qun Liu, Mehdi Rezagholizadeh, and Jimmy Lin. 2023. Miracl: A multilingual retrieval
dataset covering 18 diverse languages. Transactions of the Association
for Computational Linguistics 11 (2023), 1114–1131.

10