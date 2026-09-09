eprints@whiterose.ac.uk
https://eprints.whiterose.ac.uk

Universities of Leeds, Sheffield and York

Deposited via The University of Sheffield.

White Rose Research Online URL for this paper:
https://eprints.whiterose.ac.uk/id/eprint/240241/

Version: Accepted Version

Article:
Liu, L., Li, S., Qi, J. et al. (2026) TARAG: A time-aware retrieval-augmented generation 
framework for supporting precision crop pest and disease management through large 
language models. Computers and Electronics in Agriculture, 248. 111786. ISSN: 01681699

https://doi.org/10.1016/j.compag.2026.111786

© 2026 The Authors. Except as otherwise noted, this author-accepted version of a journal 
article published in Computers and Electronics in Agriculture is made available via the 
University of Sheffield Research Publications and Copyright Policy under the terms of the 
Creative Commons Attribution 4.0 International License (CC-BY 4.0), which permits 
unrestricted use, distribution and reproduction in any medium, provided the original work is
properly cited. To view a copy of this licence, visit 
http://creativecommons.org/licenses/by/4.0/

Reuse 
This article is distributed under the terms of the Creative Commons Attribution (CC BY) licence. This licence 
allows you to distribute, remix, tweak, and build upon the work, even commercially, as long as you credit the 
authors for the original work. More information and the full terms of the licence here: 
https://creativecommons.org/licenses/

Takedown 
If you consider content in White Rose Research Online to be in breach of UK law, please notify us by 
emailing eprints@whiterose.ac.uk including the URL of the record and the reason for the withdrawal request.

---

Graphical Abstract

TARAG: A Time-aware Retrieval-augmented Generation Framework for Supporting Precision Crop Pest and Disease Management
through Large Language Models

Lei Liu, Shunbao Li, Jun Qi, Zhipeng Yuan, Po Yang

---

Highlights

TARAG: A Time-aware Retrieval-augmented Generation Framework for Supporting Precision Crop Pest and Disease Management
through Large Language Models

Lei Liu, Shunbao Li, Jun Qi, Zhipeng Yuan, Po Yang

• TARAG introduces a time-aware RAG framework for pest and disease
management.

• A time-annotated knowledge base module structures crop stages and
pest lifecycles.

• Hybrid retrieval with time-aware re-ranking improves time-aligned evidence retrieval.

• TARAG achieves 99.14% retrieval recall and improves time-consistent
decisions.

• TAQA is a new bilingual dataset with 30k+ QA pairs covering 2k+
pest and disease entities.

---

TARAG: A Time-aware Retrieval-augmented
Generation Framework for Supporting Precision Crop
Pest and Disease Management through Large Language

Models

Lei Liua, Shunbao Lib, Jun Qic, Zhipeng Yuanb,∗, Po Yangb,∗

aSchool of Software, Yunnan University, Kunming, 650091, China
bSchool of Computer Science, University of Sheﬃeld, Sheﬃeld, S10 2TN, United

Kingdom
cDepartment of Computing, Xian JiaoTong-Liverpool University, Suzhou, 215123, China

## Abstract



Plant diseases and pests cause signiﬁcant annual crop losses, severely threatening global food security. To mitigate crop losses, large language models
(LLMs) demonstrate the ability to alleviate challenges in accessing precise
farming support by acting as intelligent assistants that provide farmers with
timely and precise decision support services. However, existing eﬀorts still
fall short in precision due to the neglect of time-sensitive nature in agricultural practices. They implicitly treat domain knowledge as time-irrelevant,
ignoring the impact of crop phenology and pest life stages in their generated recommendations. To address this challenge, we propose a Time-Aware
Retrieval-Augmented Generation framework (TARAG), comprising a timeaware knowledge base construction module, a hybrid retrieval module, and
a time-based generation module to provide precise pest management suggestions. Firstly, the time-aware knowledge base construction module constructs a time-annotated knowledge base from unstructured documents to
provide supplementary agricultural knowledge. Secondly, the hybrid retrieval
moudle performs coarse-grained sparse retrieval to ensure relevance, with a

∗Corresponding author.

Email addresses: leiliu@stu.ynu.edu.cn (Lei Liu), shunbao.li@sheffield.ac.uk
(Shunbao Li),
Jun.Qi@xjtlu.edu.cn (Jun Qi), zhipeng.yuan1@sheffield.ac.uk
(Zhipeng Yuan), po.yang@sheffield.ac.uk (Po Yang)

---

time-sensitive re-ranking stage that reﬁnes the results to achieve both semantic relevance retrieval and time alignment with user queries.
Finally,
the time-aware generation module leverages the top-k retrieved documents
and an instruction prompt to produce the ﬁnal suggestion. To validate the
eﬀectiveness of the proposed framework, we contribute TAQA, the ﬁrst bilingual, time-annotated agricultural question-answering dataset. Experiments
demonstrate that TARAG signiﬁcantly outperforms state-of-the-art RAG
frameworks in retrieval precision and suggestion quality, with 99.14% retrieval recall and an F1 score of 66.85% for generated suggestions. The implementation and datasets for this work are available in https://github.com/leehash1/agri_rag.

Keywords:
Plant disease and pest management, Retrieval-augmented generation,
Time-aware agricultural question answering, Time-sensitive information
retrieval

## 1. Introduction

1

The presence of plant diseases and insect pests constitutes a persistent
2
and severe threat to global agricultural production, with a potential annual
3
yield loss of up to 40% of global crops (Junaid and Gokce, 2024).
Such
4
biological stresses inﬂict substantial economic damage across major crop5
ping systems and, more critically, undermine food security for a growing
6
population.
Traditional pest and disease management practices, particu7
larly reliance on broad-spectrum chemical pesticides, have led to additional
8
issues, including environmental contamination, pesticide resistance, and non9
target ecological impacts (Abate et al., 2000; Deka et al., 2006; Singh et al.,
10
2024). These issues highlight the urgent need for more precise, timely, and
11
context-aware crop protection strategies that can guide farmers toward ef12
fective and environmentally responsible interventions. However, obtaining
13
accurate agronomic recommendations remains diﬃcult in practice. Speciﬁ14
cally, expert knowledge is unevenly distributed. Extension resources are also
15
limited. Furthermore, textual agricultural guidelines often contain complex,
16
time-dependent instructions that are diﬃcult to interpret without specialized
17
experience (Li et al., 2024). This gap motivates the development of intelli18
gent systems capable of delivering reliable, time-sensitive decision support
19
for crop health management.
20

2

---

Large language models (LLMs), together with retrieval-augmented gener21
ation (RAG) frameworks, oﬀer promising capabilities for addressing the chal22
lenges outlined above (Yi et al., 2025). The RAG frameworks work by ﬁrst
23
searching relevant documents in a knowledge base based on user queries, then
24
feeding those retrieved results into an LLM for obtaining a more accurate re25
sponse. By combining the retrieval-based factual grounding and adaptive
26
reasoning ability of LLMs, LLM-based RAG frameworks mitigate issues aris27
ing from incomplete or outdated model priors, enabling more reliable access
28
to domain knowledge and supporting transparent decision-making pathways.
29
These advantages have motivated growing interest in applying LLM-based
30
RAG frameworks to agricultural scenarios, such as crop disease diagnosis,
31
pest management assistance, and knowledge-driven agronomic advisory tools
32
(Kuska et al., 2024)
33
For example, Pezego (Yuan et al., 2025) implements a RAG framework
34
with a structured expert knowledge base and a chain-of-thought in an Inter35
net of Things system to provide pest management support. AgriGPT further
36
enhances factual grounding by combining dense, sparse, and knowledge-graph
37
retrieval within a Tri-RAG framework (Yang et al., 2025). In addition, other
38
studies emphasize improving retrieval precision through query expansion, hy39
brid indexing, or reranking strategies, as summarized in the survey (Vizniuk
40
et al., 2025). Collectively, these systems demonstrate the value of domain41
aware retrieval and structured knowledge integration for agricultural question
42
answering.
43
Meanwhile, recent advances in RAG have begun to incorporate time in44
formation across the pipeline (Gao et al., 2025). Representative approaches
45
such as TimeR4 extend the standard framework by integrating time process46
ing into query reformulation, retrieval, and downstream reasoning, enabling
47
time-sensitive question answering. These eﬀorts demonstrate the potential
48
of incorporating time signals within a uniﬁed RAG pipeline (Zhang et al.,
49
2024b). However, such approaches are primarily designed for general-domain
50
time reasoning, where time information can be normalized into relatively
51
consistent representations (e.g., explicit time points, intervals, or event se52
quences) and directly utilized across diﬀerent stages of the pipeline. In con53
trast, agricultural knowledge exhibits fundamentally diﬀerent time character54
istics, where time is expressed through heterogeneous and context-dependent
55
forms such as phenological stages, seasonal patterns, and biological life cy56
cles. These forms are often implicitly embedded in domain knowledge and
57
cannot be easily normalized into a uniﬁed time representation.
58

3

---

Figure 1: Comparative Analysis of TARAG versus Traditional Retrieval-Augmented Generation. Based on the framework diagram, time sensitivity in agricultural QA involves
two aspects. Input time sensitivity means that the user's query often contains explicit or
implicit time constraints, such as the 1st-generation egg-hatching, early growth period, or
post-harvest management, which directly determine what actions are appropriate. Output time sensitivity requires that the framework's response remains consistent with that
speciﬁc stage, as the recommended control measures can vary dramatically across diﬀerent
growth or seasonal phases. Traditional RAG frameworks struggle with this because they
treat time expressions as ordinary tokens and rely primarily on semantic similarity during
retrieval.

This time mismatch can lead to context-insensitive recommendations, as
59
shown in Figure 1. For instance, suggesting pesticides appropriate only for
60
early-instar larvae when the pest population has already reached adulthood
61
(Ye et al., 2025). Therefore, a uniﬁed time-aware RAG framework is needed
62
that performs explicit time-based processing from query interpretation and
63
document selection to ﬁnal response generation, ensuring that recommenda64
tions remain consistent with the dynamic biological and ecological processes
65
governing real-world farming.
66
In response to this demand, we propose TARAG, a uniﬁed framework
67
that explicitly enforces time alignment across the entire pipeline for agri68
cultural decision-making. Speciﬁcally, TARAG consists of three tightly cou69
pled components: a time-aware knowledge base construction module for time
70
grounding, a hybrid time retrieval module for time alignment, and a time71

4

---

aware answer generation module for ensuring stage-consistent outputs. This
72
pipeline-level design distinguishes TARAG from existing time-aware RAG
73
approaches that incorporate time signals only in isolated components.
74
To validate the eﬀectiveness of TARAG, the ﬁrst time-annotated agricul75
tural question-answering dataset, TAQA, is constructed with approximately
76
30,196 bilingual QA pairs and time-related metadata, covering over 2,056
77
types of pests and diseases in agriculture, which serves as a challenge bench78
mark for evaluating RAG frameworks in agriculture. In the comparison ex79
periments, the TARAG framework outperforms the state-of-the-art RAG
80
framework. In addition, the eﬃcacy of each retrieval stage is demonstrated
81
through ablation experiments.
82
The main contributions of this paper are as follows:
83
1) We propose TARAG, a uniﬁed retrieval-augmented generation frame84
work designed for time-sensitive agricultural decision support . The frame85
work explicitly integrates time signals, such as crop phenology and pest life
86
cycles, into both the retrieval and generation stages. This framework eﬀec87
tively addresses the chronic issue of time misalignment in traditional RAG
88
systems, ensuring that recommendations are synchronized with real-world
89
biological processes.
90
2) We develop a hybrid retrieval strategy with a time-aware re-ranking
91
mechanism to improve evidence alignment. It models the time relevance be92
tween user queries and candidate documents by fusing sparse lexical matching
93
and dense embeddings. This mechanism signiﬁcantly mitigates the mismatch
94
between query intent and retrieved knowledge, leading to a marked improve95
ment in retrieval precision for complex farming scenarios.
96
3) We construct TAQA, a large-scale, bilingual benchmark for time97
annotated agricultural question answering . The dataset comprises approx98
imately 30,196 QA pairs across 2,056 pest and disease types, incorporating
99
ﬁne-grained time metadata. Our extensive experiments on this benchmark
100
demonstrate that TARAG outperforms state-of-the-art frameworks across
101
multiple evaluation metrics, providing a robust foundation for future research
102
in the ﬁeld.
103

## 2. Related Work

104

2.1. Retrieval-Augmented Generation (RAG)
105
As LLMs demonstrate formidable capabilities in text comprehension and
106
generation, RAG has become a leading paradigm for enhancing the factual
107

5

---

reliability and domain adaptability of LLMs. Early RAG frameworks paired
108
sparse lexical retrievers such as BM25 (Robertson et al., 2009) with genera109
tive decoders to introduce external knowledge grounding (Lewis et al., 2020),
110
while dense retrieval models, such as DPR (Karpukhin et al., 2020) further
111
strengthened semantic matching through dual-encoder architectures. Sub112
sequent developments introduced hybrid retrievers and advanced re-ranking
113
strategies that combine sparse precision with dense coverage, improving ro114
bustness in diverse knowledge domains. More recent variants, including Self115
RAG (Asai et al., 2024), ReAct-style retrieval reasoning (Zhang et al., 2024a),
116
and lightweight designs such as LightRAG, target hallucination reduction,
117
chunk optimization, and eﬃciency under constrained resources (Guo et al.,
118
2024).
Methods like HyDE (Gao et al., 2023) or graph-augmented RAG
119
(Edge et al., 2024) extend reasoning by synthesizing hypothetical evidence
120
or leveraging structured knowledge graphs.
121
While these advancements signiﬁcantly improve factual retrieval and rea122
soning, they largely assume that relevance is time-irrelevant, depending only
123
on semantic similarity rather than contextual factors such as time, state, or
124
environment. As a result, existing RAG frameworks often retrieve informa125
tion that is topically relevant but time-incompatible, leaving them inadequate
126
for domains where the validity of knowledge changes over time, as shown in
127
Figure 1.
128
To address this gap, time-aware extensions of RAG have emerged in recent
129
years. These methods introduce time cues through time-aware re-ranking,
130
time-adjusted embeddings, or specialized datasets designed for timestamp
131
prediction and time-sensitive question answering. Representative works, in132
cluding TimeR4 (Qian et al., 2024), TimeQA (Chen et al., 2021), and Ts133
Retriever (Wu et al., 2024), integrate time reasoning into retrieval and gen134
eration to better handle event ordering and time constraints. However, these
135
methods are primarily developed for general-domain scenarios, where time
136
information can be represented in relatively explicit and consistent forms,
137
such as timestamps, event sequences, or well-structured timelines. Despite
138
their progress, none of these frameworks model the ecological, seasonal, and
139
phenological time structures that deﬁne agricultural knowledge. Agronomic
140
recommendations, such as pest control timing, nutrient management sched141
ules, and phenology-dependent disease risks are governed by biological cycles
142
rather than explicit timestamps. Consequently, general-domain time-aware
143
RAG approaches cannot capture the implicit, domain-speciﬁc time depen144
dencies that determine whether an agricultural recommendation is appropri145

6

---

ate or actionable.
146

2.2. Pest and Disease Identiﬁcation
147
Pest and disease identiﬁcation has long been a central task in agricultural
148
decision support systems, as accurate diagnosis is a prerequisite for eﬀec149
tive intervention. Early approaches relied on rule-based systems and expert
150
knowledge, where symptoms, environmental conditions, and manual obser151
vations were encoded into decision rules for disease diagnosis and treatment
152
recommendation (Shafay et al., 2025). While interpretable, these methods
153
are limited by scalability and their dependence on handcrafted knowledge.
154
With the advancement of machine learning, particularly deep learning,
155
data-driven approaches have become dominant. Convolutional neural net156
works (CNNs) have been widely applied for crop disease and pest classiﬁca157
tion from leaf images, achieving high accuracy in controlled settings (Zheng
158
et al., 2025). More recently, Transformer-based architectures and multimodal
159
models have further improved performance by capturing complex visual pat160
terns and integrating textual or contextual information (Liu et al., 2025).
161
These methods signiﬁcantly enhance automated diagnosis but are primarily
162
focused on perception tasks, often lacking the ability to provide actionable,
163
context-aware recommendations.
164
To bridge this gap, recent studies have begun exploring large language
165
models (LLMs) for agricultural question answering and decision support
166
(Tzachor et al., 2023). These systems aim to move beyond recognition toward
167
knowledge-driven reasoning, enabling users to query treatment strategies,
168
management practices, and agronomic advice. Nevertheless, most existing
169
approaches treat agricultural knowledge as static and fail to incorporate time
170
constraints that are critical in real-world scenarios.
171
However, eﬀective pest and disease management is inherently time-sensitive,
172
as appropriate interventions depend on crop growth stages, pest life cycles,
173
and seasonal dynamics. Existing identiﬁcation and QA-based systems largely
174
ignore such time dependencies, limiting their practical applicability. This
175
highlights the need for frameworks that can jointly model domain knowledge
176
and time-aware reasoning, motivating the integration of time signals into
177
retrieval-augmented generation for agricultural decision support.
178

2.3. RAG in agriculture
179
Building upon advances in pest and disease identiﬁcation and agricultural
180
decision support, LLMs have recently been explored enabling applications
181

7

---

such as advisory chatbots, crop disease diagnosis assistants, and agronomic
182
knowledge extraction systems (Gong and Li, 2025) (Yuan et al., 2025). Exist183
ing studies often combine LLMs with retrieval components built from agricul184
tural extension manuals or plant protection documents, and some incorporate
185
structured resources such as agricultural knowledge graphs to enhance fac186
tual grounding (Lv et al., 2024) (Zhao et al., 2024). These eﬀorts highlight
187
growing interest in applying RAG-style methods to improve the reliability
188
and interpretability of agricultural AI tools.
189
However, current agricultural RAG applications face two major limita190
tions. First, they treat agronomic knowledge as time-irrelevant and overlook
191
the time dependencies that determine when recommendations are valid. Re192
trieval systems typically rely on lexical or semantic similarity (Bali et al.,
193
2024) without considering crop growth stages, pest life-cycle phases, or sea194
sonal constraints, leading to time-mismatched evidence, such as retrieving
195
pre-ﬂowering pesticide guidelines for late-season scenarios. Second, the agri196
cultural domain lacks high-quality, time-annotated QA datasets, making it
197
diﬃcult for models to learn or evaluate time-sensitive reasoning. Existing
198
datasets focus on factual content but rarely encode time conditions, prevent199
ing systematic assessment of how well RAG frameworks handle time-sensitive
200
queries (Kpodo et al., 2024) (Kasai et al., 2023).
201
These constraints reveal a critical gap:
while RAG improves factual
202
grounding, it remains ill-equipped to capture the dynamic, seasonal, and
203
phenological rhythms underlying agricultural decisions. This motivates the
204
development of a time-aware RAG framework, supported by a dedicated
205
time-sensitive agricultural QA dataset, to bridge the disconnect between
206
time-sensitive reasoning and retrieval-augmented generation in agriculture.
207

## 3. Methodology

208

We ﬁrst provide an overview of the TARAG framework in Subsection 3.1.
209
The framework consists of three principal components: Subsection 3.2 intro210
duces a Time-Aware Knowledge Base Construction module that encodes time
211
cues and phenological metadata; Subsection 3.3 introduces a Hybrid Time
212
Retrieval module that fuses sparse, dense, and time ﬁltering to retrieve time213
aligned evidence; and Subsection 3.4 introduces a Time-Based Generation
214
module that synthesizes responses conditioned on retrieved, time-relevant
215
documents.
216

8

---

Figure 2: The TARAG framework consists of three main modules: (1) Time-Aware Knowledge Base Construction: utilizes an LLM to structure external knowledge, embedding each
entry with associated disease and time information; (2) Hybrid Time Retrieval: processes
an original query to perform disease-based retrieval, followed by a time-aware re-ranking
of the results to select the top-k most time-relevant documents; (3) Time-Aware Answer
Generation: augments the original query with the retrieved contexts and an instruction
prompt, guiding an LLM to generate a ﬁnal, time-sensitive response.

3.1. Overview of TARAG Framework
217
Unlike conventional question answering settings where document rele218
vance is often approximated by global semantic similarity, agricultural ques219
tion answering exhibits a more structured relevance mechanism.
220
In this domain, user queries typically contain two essential components:
221
(1) domain-speciﬁc entities, and (2) time conditions. These two components
222
jointly determine whether a piece of knowledge is applicable. Formally, we
223
represent a query as:
224
q = (qentity, qtime)
(1)

The entity component qentity includes crop types, pest or disease names,
225
and their variants. These elements are relatively stable and discrete, and
226
primarily determine the topical relevance of retrieved documents.
227
The time component qtime consists of heterogeneous time expressions,
228
which in agricultural scenarios cannot be treated as uniform timestamps. Fol229
lowing the time annotation schema deﬁned in our dataset, we categorize time
230
expressions into four canonical types: (1) phenological stages, (2) seasonal
231

9

---

periods, (3) calendar-based time, and (4) relative time expressions. These
232
categories exhibit diﬀerent semantic characteristics: phenological stages are
233
closely tied to biological processes, seasonal periods provide coarse entity con234
text, calendar-based expressions oﬀer explicit entity references, and relative
235
expressions encode procedural or event-dependent timing. As a result, time
236
in agricultural knowledge is inherently heterogeneous in both granularity and
237
dependency on biological states.
238
Correspondingly, each retrieved document d is associated with both entity
239
scope and time scope:
240
d = (dentity, dtime)
(2)

Based on this decomposition, we deﬁne document relevance as a two-stage
241
(nested) process. First, a candidate set is obtained based on entity matching:
242

Dentity = TopK

(

Scoreentity(qentity, dentity)

)

(3)

where Scoreentity measures the degree of entity-level matching (e.g., lex243
ical or semantic similarity), ensuring that retrieved documents are topically
244
relevant. Then, documents within the candidate set are re-ranked according
245
to time alignment:
246

d∗= TopK

(

Scoretime(qtime, d)

)

,
d ∈Dentity
(4)

Ultimately, d∗emerges as the most time-relevant and topically relevant
247
document. This is determined by Scoretime, which measures the alignment
248
between the query time condition and the document time scope, ensuring
249
the agronomic validity of the knowledge applied.
250
This formulation reﬂects the structured retrieval process in agricultural
251
QA. In practice, entity matching is ﬁrst used to retrieve a candidate set of
252
documents with high topical relevance, and time alignment is subsequently
253
applied to reﬁne the ranking by enforcing time consistency. Therefore, time
254
does not act as an independent relevance signal, but as a constraint that is
255
applied conditionally on entity-matched candidates.
256
From a theoretical perspective, this formulation can be viewed as a struc257
tured decomposition of relevance, which diﬀers from conventional RAG frame258
works that rely on a single similarity signal. By explicitly separating entity
259
grounding and time validity, the model can avoid retrieving documents that
260
are topically correct but time-inappropriate.
261
This theoretical formulation is consistent with the design of TARAG. The
262
ﬁrst-stage retrieval focuses on entity-level matching to ensure recall, while
263

10

---

the second-stage re-ranking enforces time alignment, ensuring that the ﬁnal
264
retrieved evidence satisﬁes both topical relevance and time validity.
265

3.2. Time-Aware Knowledge Base Construction module
266
To support ﬁne-grained time retrieval, agricultural documents are trans267
formed from unstructured text into structured JSON records through a con268
trolled prompting procedure. Each record contains standardized ﬁelds such
269
as: disease entity, crop stage, time validity intervals, and recommended treat270
ments.
271
Formally, for each raw document x, an LLM produces a structured out272
put:
273
S = LLMstruct(x, pstruct)
(5)

where pstruct denotes a schema-constrained prompt. The resulting knowledge
274
base K = S1, . . . , Sn thus encodes explicit time metadata, enabling later
275
retrieval modules to perform time-discriminative ranking.
276

3.3.
Hybrid Time Retrieval module
277
We propose a Three-Stage Hybrid Time Retrieval module that integrates
278
sparse lexical matching and dense time-aware semantic retrieval.
279

Stage 0: Entity and Time Cue Extraction
280
Before retrieval, an LLM extracts entity and time cues from the query q:
281

qentity, qtime = LLMextract(q)
(6)

where qentity contains crop or pest entities, and qtime contains time expressions
282
such as crop phenology stages or seasonal information. These extracted cues
283
are then used in the subsequent two retrieval stages.
284

Stage 1: Sparse Retrieval via BM25 with entity Filtering
285
The entity cue qentity guides BM25-based sparse retrieval. For a document
286
d, the BM25 score is computed as:
287

BM25(qentity, d) =

∑

t∈qentity∩d

IDF(t) ·
f(t, d) (k1 + 1)

f(t, d) + k1

(

1 −b + b
|d|
avgdl

)
(7)

where f(t, d) is the term frequency of token t in d, and k1, b are standard
288
hyperparameters. Only documents containing at least one disease entity are
289
retained:
290
DBM25 = {d ∈K | EntityMatch(qentity, d) = 1}
(8)

11

---

Stage 2: Dense Time-Aware Re-Ranking
291
The extracted time expressions qtime and dtime are represented as raw
292
text spans (e.g., crop stages or seasonal descriptions).
We encode these
293
expressions into dense vectors using a pre-trained sentence embedding model:
294

t = Enctime(t)
(9)

where Enctime is implemented using a frozen pre-trained encoder (e.g.,
295
BERT-based or sentence-transformer). The encoder is not further trained in
296
our framework; instead, it is directly reused to capture semantic similarity
297
between time expressions.
298
The candidate set DBM25 is then re-ranked using dense embeddings of
299
time cues extracted from the query and the documents:
300

qtime = Enctime(qtime),
dtime = Enctime(dtime)
(10)

sim(q, d) = cos(qtime, dtime)
(11)

where dtime denotes time expressions in the document.
By leveraging
301
the semantic representation ability of the embedding model, this stage maps
302
time-similar expressions (e.g., related crop stages or seasonal descriptions)
303
into nearby regions in the embedding space, ensuring that retrieved docu304
ments are time-aligned with the query and prioritizing contextually appro305
priate content for downstream generation.
306

3.4. Time-Aware Answer Generation Module
307
In the ﬁnal stage, TARAG employs an LLM to generate answers condi308
tioned on both the retrieved evidence and a time-aware grounding prompt.
309
Let Dk = d1, . . . , dk denote the selected documents. The generator produces:
310

a = LLM(q, Dk, ptime)
(12)

where ptime explicitly instructs the model to respect time constraints,
311
restrict answers to the correct crop stage, and avoid treatments irrelevant to
312
the speciﬁed period.
313
This module ensures that the ﬁnal answer reﬂects both domain correct314
ness (e.g., correct pesticide type and dosage) and time appropriateness (e.g.,
315
avoiding high-toxicity chemicals during pre-harvest safety interval).
316

12

---

Figure 3: Distribution of time expression categories in the TAQA dataset. Phenological
stages (e.g., "during ﬂowering") constitute the majority (36.8%), followed by seasonal
periods (12.5%), calendar-based times (17.5%), and relative expressions (33.2%). This
indicates a strong domain-speciﬁc bias towards ecological time references.

## 4. Dataset Construction: TAQA

317

To support systematic evaluation of time-aware reasoning in agricul318
tural question answering, we construct TAQA, a bilingual (Chinese–English)
319
dataset centered on ﬁne-grained time-sensitive understanding of crop diseases
320
and pests. This section details the design motivation, data collection pipeline,
321
time annotation schema, and statistical characteristics of the dataset.
322

4.1. Motivation and Design Principles
323
Existing agricultural QA datasets primarily focus on factual correctness
324
while overlooking the time dimension that is essential for ﬁeld decision325
making. Disease outbreaks, pest population dynamics, and recommended
326
control strategies all depend strongly on crop phenology and seasonal fac327
tors. Consequently, models lacking time situational awareness often fail to
328
produce stage-speciﬁc or time-valid answers.
329
The construction of TAQA is guided by three principles:
330

13

---

Table 1: Overview of TAQA Dataset Statistics
Dimension
Statistics
Number of QA pairs
30,000+
Crop categories
100+ distinct crop types
Unique
pest/disease
entities

2,000+ unique entities, such as "Apple Leaf
Rust Blight","Banana stem borer weevil"
Time coverage
Full seasonal cycle and long-term agronomic
stages
Average query length
∼20 words
Example of query diversity

“After ﬂowering, do grapes become susceptible to
black rot in 10–14 days?
How should it be prevented?”
“How to control grape black rot about two weeks
after ﬂowering?”

• Time Explicitness: each instance must contain at least one explicit
331
or implicit time cue (e.g., “Heading stage”, “after harvest”, “late Au332
gust”).
333

• Agronomic Faithfulness: questions and answers must align with
334
region-speciﬁc cultivation cycles and validated plant protection guide335
lines.
336

• Retrieval Compatibility: documents are segmented and annotated
337
to support time-aware retrieval modules such as time ﬁltering and hy338
brid sparse–dense ranking.
339

4.2. Data Sources and Annotation Process
340
• Data Sources: The dataset is compiled from authoritative agricul341
tural resources, including: (1) national and provincial plant protection
342
manuals; (2) digital agricultural extension archives; (3) peer-reviewed
343
agronomy literature (Yao et al., 2024; Yan et al., 2025); (4) farmer
344
consultation logs and expert Q&A forums.
345

All raw texts are processed following a two-stage pipeline:
346

• Question Generation and Veriﬁcation
347

We adopt a hybrid human-in-the-loop generation workﬂow. LLMs are
348
prompted to produce time-based questions based on each document
349

14

---

Figure 4: Summary statistics of text lengths for both queries and answers across four
time-related categories in the agricultural QA dataset. Across all categories, queries remain uniformly concise (median about 24 to 25 words, IQR about 6 to 7) with low variance,
whereas answers are substantially longer and more dispersed. The Phenological Stage category contains the largest sample size and yields the longest answers on average (mean
about 101 words, IQR about 76), followed by Calendar-Based Time and Seasonal Period, whose answers also span a wide range (maximum up to 552 words). The Relative
Time Expression category exhibits relatively shorter answers (mean about 77 words) but
still shows considerable variability. Overall, the consistent gap between query and answer
length highlights that time-related agricultural questions are brief and well deﬁned, while
their corresponding explanations require richer and category-dependent contextual information.

segment. Domain experts subsequently verify correctness, remove hal350
lucinations, and ensure agronomic validity.
351

• Golden Answer and Evidence Alignment
352

Each question in TAQA is paired with a gold-standard answer and its
353
corresponding evidence is deﬁned at the document level. Instead of
354
selecting a minimal continuous text span, annotators identify the spe355
ciﬁc source document(s), represented by unique document identiﬁers,
356
that contain suﬃcient information to support both the factual and time
357
components of the answer. This design provides an explicit grounding
358
signal for retrieval evaluation, enabling rigorous assessment of whether
359
a framework can retrieve the correct evidence document(s) necessary
360
for answering time-sensitive agricultural questions.
361

15

---

Table 2: Examples of time-aware agricultural question answering. The time condition is
explicitly speciﬁed in the query and categorized into diﬀerent time types. Red represents
pests and diseases, blue represents time, and related documents indicate which document
the question was extracted from.

Query
Time
(Category)

Answer
Relative
Docs

How should maize
northern leaf blight
be
controlled
at
the early infection
stage?

Early
infection
stage
(Relative
Time Expression)

Apply fungicides such as 5%
chlorothalonil WP (300× dilution) or 80% Sukejing WP
(1000×
dilution).
Spray
once every 10 days for 2–3
consecutive applications.

#387

What
should
be
done
after
maize
northern leaf blight
has occurred after
maize harvest?

Post-harvest
(Relative
Time Expression)

Remove and destroy diseased
plant residues both inside
and outside the ﬁeld.

#388

How should maize
Fusarium
seedling
blight be treated at
the seed stage?

Seed
stage
(Phenological
stage)

Treat seeds with 50% carbendazim WP at 0.2%–0.3%
of seed weight, or soak seeds
in 70% thiophanate-methyl
WP (500× dilution).

#1524

How
should
Monema
ﬂavescens
be
controlled
in
winter?

Winter (Seasonal Period)

During winter, remove overwintering cocoons by pruning branches.
Collected cocoons should be destroyed to
eliminate pest sources.

#63

How
should
Monema
ﬂavescens
be
controlled
around
June?

Around June
(CalendarBased Time)

During the egg hatching period, spray 20% insecticide
suspension (1500× dilution)
or 5% KASIKE suspension
(1500× dilution) at the early
larval stage.

#64

16

---

4.3. Time Annotation Schema
362
To explicitly capture the time semantics underlying agricultural phe363
nomena and disease dynamics, TAQA adopts a structured time annotation
364
schema focused on the categorization of time expressions. Although time
365
information in agricultural texts can span multiple dimensions, the present
366
work annotates the Time Category dimension, which establishes a uniﬁed
367
taxonomy for normalizing heterogeneous time mentions across sources.
368
Time Category: Each time expression in the dataset is assigned to one
369
of four canonical categories that frequently appear in agronomic decision370
making:
371

• Phenological Stage: Expressions describing crop growth or pest de372
velopment phases, such as “seedling stage”, “fruit set stage”, or “over373
wintering period”. These stages are strongly associated with risk vari374
ation and treatment eﬃcacy.
375

• Seasonal Period: Coarse-grained references to agricultural seasons
376
or sub-seasonal intervals, including phrases like “early spring”, “mid377
summer”, or “late autumn”. Such expressions provide broad time con378
text but often require integration with phenological cues for actionable
379
interpretation.
380

• Calendar-Based Time: Mentions expressed using explicit dates or
381
ranges, e.g., “August”, “late July”, or “during September”. These ex382
pressions facilitate alignment with real-world time but may vary in
383
precision across sources.
384

• Relative Time Expression: Context-dependent references such as
385
“before harvest”, “after ﬂowering”, or “during pesticide application”.
386
These expressions often encode procedural relations rather than abso387
lute time and are essential for modeling agronomic workﬂows.
388

This categorization supports downstream time-sensitive reasoning by map389
ping heterogeneous time expressions, each with distinct granularity and lin390
guistic form, into their corresponding normalized time categories. This struc391
tured normalization enables the framework to align queries and documents
392
based on consistent category-level time semantics rather than relying on
393
surface-level textual similarity. Furthermore, an analysis of the TAQA dataset,
394
as shown in Table 1 and
2, and Figure 3 and 4, demonstrates that these
395

17

---

Table 3: A comprehensive evaluation of the retrieval module

Model
Recall
nDCG

R@1
R@3
R@5
R@10
R@20
nD@1
nD@3
nD@5
nD@10
nD@20

Contriever (Izacard et al., 2021)
5.07%
9.84%
12.55%
17.02%
22.62%
5.07%
7.83%
8.94%
10.37%
11.78%
TS-Contriever (Wu et al., 2024)
7.07%
12.41%
15.36%
20.29%
25.97%
7.07%
10.16%
11.38%
12.97%
14.40%
E5 (Wang et al., 2024)
78.33%
92.29%
95.03%
96.71%
97.51%
78.33%
86.59%
87.72%
88.28%
88.48%
Agri-sentence-transformer (Rezayi et al., 2025)
1.42%
2.90%
3.68%
5.40%
7.73%
1.42%
2.27%
2.59%
3.14%
3.73%
BCE (Youdao, 2023)
69.77%
84.65%
88.58%
91.94%
94.32%
69.77%
78.56%
80.19%
81.28%
81.89%
Qwen3-Embedding-0.6B (Zhang et al., 2025)
71.16%
84.99%
88.53%
91.48%
93.57%
71.16%
79.35%
80.81%
81.77%
82.31%
Qwen3-Embedding-4B (Zhang et al., 2025)
76.28%
89.19%
92.07%
94.49%
96.21%
76.28%
83.91%
85.11%
85.89%
86.33%
Our
80.52%
93.45%
96.31%
98.44%
99.14%
80.52%
86.62%
87.75%
88.28%
88.49%

time categories are widely distributed across the corpus, highlighting their
396
central role in structuring time-based retrieval and reasoning within agricul397
tural question-answering tasks.
398

## 5. Experiments

399

5.1. Experimental environment
400
The experimental setup was conducted on a high–performance hardware
401
platform comprising a 12th Generation Intel(R) Core(TM) i7-12700H CPU
402
operating at 2.70GHz, an NVIDIA GeForce RTX 4090 GPU with 24 GB
403
of VRAM (driver version 525.125.06), and 24 GB of system memory. The
404
implementation of the experimental framework was carried out using Python
405
3.9.23 and the PyTorch 2.5.1 deep learning library, ensuring compatibility
406
and eﬃciency in handling computationally intensive tasks.
407

5.2. Experimental Design
408
Our experimental evaluation is conducted from two complementary per409
spectives: (1) a retrieval-focused evaluation that isolates the retriever to
410
assess the time alignment and relevance of retrieved documents, and (2) a
411
full RAG evaluation that examines how time information is preserved and
412
utilized throughout the entire pipeline to produce contextually appropriate
413
agronomic recommendations.
414

5.2.1. Evaluation of the Retrieval Module
415
To assess retrieval quality, we adopt two widely used ranking-based met416
rics: Recall@k(%) and nDCG@k(%). Recall@k evaluates whether the re417
triever successfully surfaces the relevant time-aligned documents within the
418
top-k results:
419

18

---

Recall@k = |Relevant ∩Retrieved@k|

|Relevant|
(13)

where, Relevant denotes the set of all documents that are truly relevant and
420
time-aligned with the query, while Retrieved@k denotes the set of the top-k
421
documents returned by the retrieval method.
422
This metric is particularly suitable for time-sensitive agricultural QA be423
cause relevant evidence is often sparse and time-dependent; thus failing to
424
retrieve such passages directly undermines downstream generation accuracy.
425
To complement recall, we use normalized Discounted Cumulative Gain
426
(nDCG@k), which considers both correctness and ranking position:
427

nDCG@k =
1
IDCG@k

k
∑

i=1

2reli −1
log2(i + 1)
(14)

where reli denotes the relevance of the i-th retrieved document.
428
Deﬁnition of IDCG@k: IDCG@k (Ideal DCG at rank k) is the maxi429
mum possible DCG value for the top-k documents, obtained by sorting the
430
candidate set in descending order of their true relevance scores:
431

IDCG@k =

k
∑

i=1

2rel∗
i −1
log2(i + 1)
(15)

where rel∗

i is the relevance score of the i-th document in the ideally ranked
432
list.
433
Computation of reli: In our time-sensitive agricultural retrieval setting,
434
reli is deﬁned as a binary or graded score reﬂecting both semantic relevance
435
and time correctness of document di with respect to the query q:
436

reli =

{

1,
if di is relevant and time aligned with q
0,
otherwise
(16)

nDCG@k therefore measures how well the top-k retrieved documents
437
are both relevant and time-consistent, which is critical because downstream
438
generation quality deteriorates when irrelevant or time-mismatched passages
439
dominate the top ranks.
440
We focus on the top-20 retrieved documents (i.e., Recall@20 and nDCG@20).
441
Retrieving beyond this depth provides diminishing gains: introducing exces442
sive context into the LLM not only increases computational cost but also risks
443
overwhelming the generator with noisy or time-inconsistent information.
444

19

---

5.2.2. Evaluation of the End-to-End RAG Framework
445
For full pipeline evaluation, we adopt standard QA metrics, namely Re446
call(%), Precision(%), and F1(%), computed over the top-10 retrieved doc447
uments that support control recommendations, rather than over generated
448
answer candidates. This threshold balances coverage with reliability, ensur449
ing that metrics reﬂect the practical usefulness of the recommendations in
450
real-world agricultural decision-making.
451
To account for the strong dependency between treatment validity and
452
time conditions in agricultural pest management, we further introduce a
453
task-speciﬁc interpretation of TP/FP/FN/TN.
454
Instead of using their generic deﬁnitions, we operationalize them based
455
on whether the generated recommendation is both agronomically correct and
456
time-appropriate:
457

• TP: the model outputs a pesticide and dosage that are agronomically
458
correct and consistent with the required time condition.
459

• FP: the model suggests a pesticide that is either not supported by the
460
reference answer or violates time constraints (i.e., time-inappropriate
461
treatment).
462

• FN: the model fails to include a required pesticide that is speciﬁed in
463
the reference answer under the given time condition.
464

• TN: the model correctly avoids recommending pesticide application
465
when treatment is unnecessary or time-prohibited.
466

Based on these deﬁnitions, the evaluation metrics are computed as:
467

Precision@10 =
TP
TP + FP,
Recall@10 =
TP
TP + FN
(17)

F1@10 = 2 × Precision@10 × Recall@10

Precision@10 + Recall@10
(18)

This design allows us to quantify not only factual correctness but also the
468
time sensitivity of generated recommendations, providing a uniﬁed measure
469
of how well a RAG framework aligns agronomic actions with the appropriate
470
phenological or seasonal stage.
471

20

---

5.3. Baselines
472
To comprehensively evaluate both the retrieval and end-to-end capabili473
ties of our proposed TARAG framework, we compare it against a diverse set
474
of strong baselines. These baselines cover (1) standalone retrievers widely
475
used in domain-general and time-aware retrieval research, and (2) repre476
sentative RAG frameworks that reﬂect diﬀerent prompt-based, retrieval477
augmented, and structure-enhanced paradigms.
478

5.3.1. Retrieval Baselines
479
We compare TARAG's hybrid time-aware retriever with a diverse set
480
of dense and sparse retrieval baselines, including both general-purpose and
481
time-sensitive models: Contriever (Izacard et al., 2021), TS-Contriever (Wu
482
et al., 2024),BCE (Youdao, 2023), E5 (Wang et al., 2024), Qwen-Embedding (Zhang
483
et al., 2025), Agri-Sentence-Transformer (Rezayi et al., 2025), BM25 (Robert484
son et al., 2009), and BGE-M3 (Chen et al., 2024).
485

5.3.2. RAG Framework Baselines
486
For the end-to-end comparison, we evaluate TARAG against several rep487
resentative RAG and prompting frameworks that reﬂect diﬀerent philoso488
phies of reasoning, retrieval integration, and knowledge organization, and we
489
employ DeepSeek's 1.5B, 7B, and 14B models as the underlying generation
490
backbone (Guo et al., 2025).
491

• Direct Prompting: The LLM answers queries without any retrieval
492
augmentation, providing a lower bound for model performance.
493

• Chain-of-Thought (CoT) Prompting (Wei et al., 2022):
A
494
reasoning-enhanced prompting strategy that encourages step-by-step
495
generation, serving as a non-retrieval reasoning baseline.
496

• Naive RAG (Lewis et al., 2020):
The standard retrieve-then497
generate pipeline where retrieved passages are directly concatenated
498
with the query.
499

• TimeR4 (Qian et al., 2024): A time-enhanced RAG framework
500
incorporating rule-based time re-ranking for improved time-sensitive
501
retrieval.
502

21

---

• LightRAG (Guo et al., 2024): A lightweight and modular RAG
503
framework supporting multiple retrieval paradigms and eﬃcient rank504
ing mechanisms.
505

This collection of baselines ensures a rigorous evaluation across both re506
trieval quality and time-aligned generation, enabling a comprehensive assess507
ment of TARAG's contributions.
508

5.4. Main Results
509
5.4.1. Overall Performance
510
Across both retrieval-only and full RAG evaluations, TARAG achieves
511
the best performance among all compared frameworks. In the retrieval task,
512
TARAG's hybrid time-aware retriever consistently outperforms all dense and
513
sparse baselines, achieving the highest Recall@20 (99.14%) and nDCG@20
514
(88.49%), as shown in Table 3. Similarly, in end-to-end evaluation, TARAG
515
delivers the strongest Precision@10 (up to 54.41%), Recall@10 (up to 86.67%),
516
and F1@10 (up to 66.85%), demonstrating superior time grounding and fac517
tual consistency compared to direct prompting, CoT prompting, and existing
518
RAG frameworks such as TimeR4 and LightRAG, as shown in Table 4. No519
tably, the gains in Precision@10 and F1@10 are particularly important, as
520
these metrics directly reﬂect the ability to ﬁlter time-irrelevant evidence in
521
time-sensitive agricultural decision-making.
522
Notably, while several dense retrievers and RAG baselines have shown
523
strong performance in general-purpose question answering benchmarks, their
524
eﬀectiveness drops markedly in our time-sensitive agricultural setting. This
525
performance gap highlights the unique challenge of time grounding in agri526
cultural decision support, where correct recommendations depend not only
527
on semantic relevance but also on strict alignment with crop growth stages
528
and seasonal constraints.
529

5.4.2. Why TARAG Performs Better
530
The superiority of TARAG can be attributed to two key design choices
531
that directly address the time characteristics of agricultural knowledge.
532
First, the time-aware knowledge base construction enriches each passage
533
with explicit time metadata, enabling the retriever to ﬁlter out seasonally
534
or phenologically incompatible information at an early stage. This design
535
eﬀectively mitigates a common failure mode observed in dense retrievers,
536
which often retrieve passages with high semantic similarity but invalid time
537

22

---

Table 4: Comparison of Recall@10, Precision@10, and F1@10 across models and methods.

Model
Method
Recall@10
Precision@10
F1@10

DeepSeek-

R1-1.5B

Direct Prompt
0.0%
0.0%
0.0%
CoT
1.12%
1.08%
1.10%
Naive RAG
33.86%
31.92%
32.86%
TimeR4
47.80%
38.53%
42.67%
Light RAG
14.38%
14.33%
14.38%
Our
63.56%
46.98%
54.03%

DeepSeek-

R1-7B

Direct Prompt
3.68%
3.56%
3.62%
CoT
9.31%
8.80%
9.00%
Naive RAG
40.27%
35.45%
37.70%
TimeR4
59.68%
43.80%
50.31%
Light RAG
22.67%
21.28%
21.95%
Our
76.36%
53.11%
62.50%

DeepSeek-

R1-14B

Direct Prompt
9.38%
9.28%
9.33%
CoT
23.01%
21.68%
22.32%
Naive RAG
57.56%
46.13%
51.22%
TimeR4
78.64%
51.56%
62.28%
Light RAG
39.94%
33.77%
36.60%
Our
86.67%
54.41%
66.85%

applicability. Prior studies on time reasoning have similarly emphasized that
538
explicit time constraints are essential in decision-critical domains, and our
539
results further conﬁrm this observation in the agricultural context.
540
Second, the hybrid time-aware retrieval mechanism integrates sparse lexi541
cal matching with time-weighted dense embeddings, improving ranking qual542
ity for queries containing agricultural time expressions. By jointly modeling
543
lexical cues and time relevance, TARAG retrieves evidence that is not only
544
semantically relevant but also time-aligned with the query intent. This di545
rectly beneﬁts the generation stage, as the LLM receives cleaner and more
546
time-compatible evidence rather than noisy or time-conﬂicting documents,
547
leading to higher end-to-end Precision and F1 scores.
548

23

---

5.4.3. Why Existing Baselines Underperform
549
Dense retrievers such as Contriever (Izacard et al., 2021), BGE (Chen
550
et al., 2024), and E5 (Wang et al., 2024) excel at semantic matching and
551
have demonstrated strong performance in a wide range of open-domain re552
trieval tasks. However, they treat time information as unstructured text,
553
making them insensitive to phenological constraints that are critical in agri554
cultural decision-making. As a result, these models frequently retrieve pas555
sages that describe correct diseases but inappropriate time periods, such as
556
recommending chemicals eﬀective during overwintering when the query con557
cerns a summer growth stage. This behavior explains why dense retrievers
558
achieve high Recall@20 but substantially lower nDCG@20 and end-to-end
559
F1@10, as shown in Tables 3 and 4.
560
Sparse retrievers such as BM25 rely on lexical overlap and can partially
561
capture explicit time expressions. However, they fail to recognize semanti562
cally equivalent but lexically divergent time phrases (e.g., “pre-bloom” vs
563
“bud break”), resulting in poor recall for time-sensitive queries. Similarly,
564
baseline RAG frameworks, including Direct Prompting, CoT-Prompting (Wei
565
et al., 2022), Naive RAG (Lewis et al., 2020), and LightRAG (Guo et al.,
566
2024), lack explicit time grounding mechanisms. These methods depend on
567
general-purpose generative reasoning, which often overlooks implicit time
568
cues and leads to seasonally or phenologically inappropriate recommenda569
tions.
570
It is worth noting that these baseline frameworks were not originally de571
signed for ﬁne-grained agricultural time reasoning, which partially explains
572
their limited performance in our setting. In contrast, TARAG explicitly in573
corporates time constraints during retrieval, reducing both false positives
574
caused by time-irrelevant evidence and false negatives caused by missing
575
time-appropriate measures. This targeted modeling of time relevance ulti576
mately leads to signiﬁcantly improved F1@10 in time-sensitive agricultural
577
decision support.
578

5.5. Ablation Studies
579
To better understand the contribution of each component in our time580
aware retrieval-augmented framework, we conduct a series of ablation stud581
ies focusing on two aspects: (1) disentangling the hybrid retriever into its
582
dense and sparse components, and (2) validating the generality of our hybrid
583
retrieval strategy by pairing BM25 with alternative dense retrievers.
584

24

---

Table 5: Ablation study on Retrieval Module
Method
Recall@K
nDCG@K

1
3
10
1
3
10

BM25
58.22%
79.14%
91.25%
58.22%
69.69%
73.95%
BGE
78.19%
89.19%
95.24%
78.19%
84.65%
86.90%
Our
80.52%
93.45%
98.44%
80.52%
86.62%
88.28%

5.5.1. Eﬀect of Hybrid Retrieval
585
Our hybrid retriever combines a dense encoder with a sparse BM25 re586
triever to jointly capture semantic relevance and lexical-time cues. To isolate
587
the eﬀect of this design, we compare the full hybrid retriever with its indi588
vidual components (Dense-only and BM25-only).
589
Table 5 shows that the hybrid retriever consistently outperforms both
590
standalone dense and standalone sparse retrieval. This conﬁrms that dense
591
retrieval excels at capturing semantic similarity, while BM25 contributes
592
complementary lexical grounding essential for agricultural terminology and
593
time expressions. The combination yields superior recall and nDCG, demon594
strating the necessity of integrating both signals for time-sensitive agricul595
tural QA.
596
The clear performance drop when removing either component indicates
597
that both semantic matching and lexical relevance are crucial for time-sensitive
598
agricultural retrieval. BM25 often retrieves passages containing explicit time
599
markers (e.g., "pre-bloom", "early fruiting"), while dense retrievers capture
600
higher-level biological transitions not explicitly stated in text. Their comple601
mentary strengths explain the observed performance gains.
602

5.5.2. Generalization Across Dense Retrievers
603
To examine whether our hybrid retrieval design beneﬁts only a particular
604
dense encoder or is generally applicable, we substitute the dense encoder
605
with several widely used models (BCE, E5, and Qwen Embedding).
For
606
each dense model, we compare dense-only retrieval with its hybrid variant
607
(Dense Model + BM25).
608
As shown in Figure 5, adding BM25 consistently improves both Recall@20
609
and nDCG@20 across all dense encoders. This demonstrates that our hybrid
610
retrieval strategy is not tied to a speciﬁc dense model but is a general en611
hancement applicable to a wide range of retrievers.
612

25

---

Figure 5: Performance evaluation of the hybrid retrieval framework. This ﬁgure uses four
subplots (arranged in a 4 × 1 pattern) to compare the recall (Recall@K) of diﬀerent dense
retrieval models under the hybrid framework with the BM25 baseline. The horizontal
axis represents the K value (1, 3, 5, 10), and the vertical axis represents the recall. The
curves show that integrating each model (such as BCE and Qwen-0.6B) into the proposed
hybrid framework signiﬁcantly outperforms their individual use or the BM25 baseline.
The average improvement percentage marked above further validates the eﬀectiveness of
the framework.

26

---

The uniform improvement across all models indicates that hybrid retrieval
613
eﬀectively oﬀsets the time insensitivity of dense retrievers by injecting explicit
614
lexical signals, which are particularly important for agricultural phenology,
615
stage-speciﬁc management actions, and seasonal pest behaviors.
616
These ablations collectively validate that hybrid time-aware retrieval is
617
an essential component of our TARAG framework, providing a stronger foun618
dation for downstream time-based answer generation.
619

5.6. Qualitative Case Study of Existing RAG Limitations
620
To further illustrate the practical advantages of our time-aware RAG
621
framework, we present a case study comparing model outputs on a time622
sensitive agricultural query. Across diﬀerent baseline conﬁgurations, we ob623
serve distinct error patterns reﬂecting the limitations of each method. Di624
rect Prompting often fails to produce actionable recommendations, as the
625
model tends to provide vague or generic descriptions without specifying con626
crete chemical control measures or growth-stage aligned treatments. Naive
627
RAG shows partial improvement by retrieving relevant segments; however,
628
the presence of substantial irrelevant context, combined with the model’s
629
susceptibility to hallucination, leads to inaccurate or inconsistent control
630
recommendations. LightRAG, despite leveraging a knowledge-graph-based
631
structure, suﬀers from signiﬁcant information loss during graph construction
632
and frequently retrieves semantically misaligned fragments, resulting in er633
roneous or incomplete answers. For more details, please see Table 6. To sys634
tematically characterize these recurring vulnerabilities, Table 7 categorizes
635
the baseline failures into three principal modes: time misidentiﬁcation, time636
misaligned retrieval, and time inconsistency. As illustrated, while traditional
637
pipelines frequently output time disjointed or generic advice, TARAG eﬀec638
tively anchors the generation to the exact phenological stage, consistently
639
delivering precise and actionable agronomic treatments.
640

5.7. Failure Mode Analysis
641
While the proposed TARAG framework eﬀectively mitigates the afore642
mentioned baseline errors through explicit time modeling and hybrid re643
trieval, it still exhibits speciﬁc failure modes when processing highly ambigu644
ous queries. Our analysis indicates that performance degradation primarily
645
occurs when time cues are weakly speciﬁed or implicitly bounded. For exam646
ple, as shown in Table 8, user expressions such as "before peak emergence"
647
introduce partial time ambiguity. Lacking a hard chronological boundary,
648

27

---

Table 6: Case study comparing four methods on a time-sensitive agricultural question.
Incorrect outputs are marked in red; correct chemical recommendations from our method
are marked in blue.

Method
Question:
“What
should
be
done
during
the
1st-generation egg-hatching period of Adoxophyes
orana?”
Direct
Prompt

During the ﬁrst-generation egg-hatching period of Adoxophyes orana, timing is especially important because the
young larvae are most vulnerable before they roll leaves or
enter fruit clusters. At this stage, it helps to intensify ﬁeld
monitoring and conﬁrm hatch timing through degree-day accumulation or direct scouting.
Naive RAG
Some steps you can take include removing the badly aﬀected
leaves to reduce early infestations and keeping an eye on
the orchard for newly hatched larvae. It may also help to
adjust ﬁeld management to keep the canopy dry and improve
airﬂow.
For chemical control, you could consider using a
pyrethroid spray every few days to suppress emerging larvae,
and treatments like chlorpyrifos can also be applied around
the ﬂowering period to keep populations low.
LightRAG
When dealing with the ﬁrst-generation egg-hatching period
of Adoxophyes orana, it is important to manage the larvae
before they enter leaves or shoots. According to the retrieved
information, growers can consider applying dormant-season
treatments such as lime-sulfur or even high-concentration oil
emulsions, which help suppress overwintering pest populations. Chemical control: Spray with 50% phoxim EC at a
dilution of 1,000 times, or 10% imidacloprid EC at a dilution of 2,000 times, or 10% imidacloprid WP at a dilution of
2,000 times, or 40% cypermethrin EC at a dilution of 600800 times.
Our
(TARAG)

Identiﬁed that the pest was in the 1st–generation egghatching stage and provided control measures suitable for
this timing.
Suggested applying “80% dichlorvos EC at
800 × dilution,” “or 50% phoxim EC at 1500 × dilution,”
“or 48% chlorpyrifos EC at 2000× dilution.”to target newly
emerged larvae before they enter protected feeding sites.
Also included several routine management practices, such
as improving orchard cleanliness, maintaining regular monitoring during hatch, and checking young larval activity to
ensure treatments are applied at the optimal moment.

28

---

Table 7:
Representative failure modes of existing RAG frameworks compared with
TARAG. In the user queries, red represents pests and blue represents time constraints.
For the model outputs, traditional RAG failures across the pipeline are highlighted in
red, with the speciﬁc error type denoted in parentheses, while TARAG provides precise,
stage-aware recommendations in blue.

User Query
Traditional RAG
Output

TARAG Output
(Ours)

What control
measures should be
taken during the
early infestation
stage of wheat
aphids?

“I recommend focusing
on general ﬁeld
sanitation and ensuring
proper winter irrigation.
Keep the ﬁeld clean to
reduce future outbreaks.”
(Time
Misidentiﬁcation)

“For the early infestation
stage, rapid suppression
is critical. Apply a
targeted foliar spray of
10% imidacloprid WP
(1500× dilution) to
eﬀectively control the
initial population before
it spreads.”

What should be
done during the
egg-hatching
period of rice stem
borers?

“It is highly
recommended to perform
deep soil plowing and
practice stubble burning
after the rice harvest.”
(Time-Misaligned
Retrieval)

“During the egg-hatching
period, treatments must
target the larvae before
stem penetration.
Immediately apply
chlorantraniliprole SC to
achieve optimal control
of the newly hatched rice
stem borers.”

How to control
cotton bollworm
during larval
emergence?

“For controlling cotton
bollworm during this
stage, a comprehensive
approach is best. Set up
adult pheromone traps to
monitor moth ﬂights, and
simultaneously apply
late-stage chemical
defoliants to expose the
bolls.”
(Time Inconsistency)

“To control cotton
bollworm during larval
emergence,
stage-consistent
biological treatments are
required. Apply Bacillus
thuringiensis (Bt)
directly to the foliage to
eﬀectively target the
actively feeding young
larvae.”

29

---

Table 8: Analysis of TARAG's residual error when handling queries with ambiguous time
boundaries. In the user query, red represents pests and blue represents time constraints.
For the model outputs, incorrectly hallucinated or out-of-stage extensions are marked in
red.

User Query
Traditional RAG
Output

TARAG Output
(Residual Error)

What actions should
be taken before peak
emergence of leaf
miners?

To eﬀectively manage
leaf miners, a
comprehensive approach
is recommended. You
should perform winter
orchard pruning to
eliminate overwintering
pupae. Additionally,
apply systemic larval
pesticides to control
feeding larvae, and set
up adult pheromone
traps.

Before the peak
emergence of leaf
miners, prioritize setting
up pheromone
monitoring networks
and applying light
preventive sprays. To
ensure complete control,
also apply a
high-concentration
abamectin
(avermectins) treatment
to eradicate larvae
already mining inside
the leaves.

the framework retrieves a broader time scope, which subsequently leads the
649
generation module to output a mixture of both preventive and reactive mea650
sures, rather than a single pinpointed solution. These observations highlight
651
a current limitation of our time-aware design: it relies heavily on extractable
652
time anchors. Consequently, further improvements are required to enhance
653
the model's complex time-reasoning capabilities during the generation phase,
654
speciﬁcally for resolving vague, continuous, or highly implicit time expres655
sions.
656

## 6. Conclusion and Future Work

657

In this work, we present TARAG, a framework designed to address the
658
time misalignment that commonly arises in agricultural question answering.
659
By integrating a time-indexed knowledge base, hybrid retrieval mechanisms,
660
and time-based answer generation, TARAG substantially improves both re661

30

---

trieval quality and end-to-end QA performance. Our experiments demon662
strate that time metadata plays a pivotal role in aligning model outputs
663
with crop phenology, pest development stages, and season-dependent man664
agement constraints. The proposed TAQA dataset further enables systematic
665
evaluation of time-sensitive reasoning, ﬁlling a critical gap in agricultural QA
666
research.
667
While TARAG marks a signiﬁcant step toward reliable and context-aware
668
agricultural assistance, several avenues remain open for exploration. First,
669
time metadata in agricultural texts is often implicit; future work could in670
corporate automated time inference models to enhance coverage and granu671
larity. Second, integrating real-time environmental signals, such as weather
672
trajectories or pest monitoring data, would allow the framework to adapt to
673
dynamically changing ﬁeld conditions. Finally, extending TARAG to mul674
timodal settings, including remote sensing imagery and sensor data, may
675
further enhance its utility in precision crop management.
676
Overall, we hope this work provides a foundation for developing time677
robust RAG frameworks that support safer, more accurate, and more sus678
tainable agricultural decision-making.
679

## References

680

Abate, T., van Huis, A., Ampofo, J.K.O., 2000. Pest management strate681
gies in traditional agriculture: an african perspective. Annual review of
682
entomology 45, 631–659. https://doi.org/10.1146/annurev.ento.45.
683
1.631.
684

Asai, A., Wu, Z., Wang, Y., Sil, A., Hajishirzi, H., 2024. Self-RAG: Learn685
ing to retrieve, generate, and critique through self-reﬂection, in:
The
686
Twelfth International Conference on Learning Representations.
https:
687
//openreview.net/forum?id=hSyW5go0v8.
688

Bali, A., Bhagwat, A., Bhise, A., Joshi, S., 2024.
Semantic similarity
689
detection and analysis for text documents, in:
2024 Second Interna690
tional Conference on Emerging Trends in Information Technology and
691
Engineering (ICETITE), IEEE. pp. 1–9. http://dx.doi.org/10.1109/
692
ic-ETITE58242.2024.10493834.
693

Chen,
J.,
Xiao,
S.,
Zhang,
P.,
Luo,
K.,
Lian,
D.,
Liu,
Z.,
2024.
694
Bge m3-embedding: Multi-lingual, multi-functionality, multi-granularity
695

31

---

text embeddings through self-knowledge distillation.
arXiv preprint
696
arXiv:2402.03216 4. https://doi.org/10.48550/arXiv.2402.03216.
697

Chen, W., Wang, X., Wang, W.Y., 2021.
A dataset for answering time698
sensitive questions. arXiv preprint arXiv:2108.06314. https://doi.org/
699
10.48550/arXiv.2108.06314.
700

Deka, M., Bhuyan, M., Hazarika, L., 2006.
Traditional pest manage701
ment practices of assam.
Indian Journal of Traditional Knowledge
702
5, 75–78.
https://www.academia.edu/99492232/Traditional_pest_
703
management_practices_of_Assam?sm=b.
704

Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S.,
705
Metropolitansky, D., Ness, R.O., Larson, J., 2024. From local to global:
706
A graph rag approach to query-focused summarization. arXiv preprint
707
arXiv:2404.16130. https://doi.org/10.48550/arXiv.2404.16130.
708

Gao, L., Ma, X., Lin, J., Callan, J., 2023. Precise zero-shot dense retrieval
709
without relevance labels, in: Proceedings of the 61st Annual Meeting of
710
the Association for Computational Linguistics (Volume 1: Long Papers),
711
pp. 1762–1777. https://doi.org/10.18653/v1/2023.acl-long.99.
712

Gao, Y., Xiong, Y., Zhong, Y., Bi, Y., Xue, M., Wang, H., 2025. Synergizing
713
rag and reasoning: A systematic review. arXiv preprint arXiv:2504.15909
714
https://doi.org/10.48550/arXiv.2504.15909.
715

Gong, R., Li, X., 2025.
The application progress and research trends of
716
knowledge graphs and large language models in agriculture. Computers
717
and electronics in agriculture 235, 110396. https://doi.org/10.1016/
718
j.compag.2025.110396.
719

Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., Zhu, Q., Ma, S.,
720
Wang, P., Bi, X., et al., 2025. Deepseek-r1: Incentivizing reasoning capa721
bility in llms via reinforcement learning. arXiv preprint arXiv:2501.12948
722
https://arxiv.org/abs/2501.12948.
723

Guo, Z., Xia, L., Yu, Y., Ao, T., Huang, C., 2024. Lightrag: Simple and fast
724
retrieval-augmented generation. arXiv preprint arXiv:2410.05779. https:
725
//doi.org/10.48550/arXiv.2410.05779.
726

32

---

Izacard, G., Caron, M., Hosseini, L., Riedel, S., Bojanowski, P., Joulin, A.,
727
Grave, E., 2021. Unsupervised dense information retrieval with contrastive
728
learning. arXiv preprint arXiv:2112.09118. https://doi.org/10.48550/
729
arXiv.2112.09118.
730

Junaid, M., Gokce, A., 2024. Global agricultural losses and their causes.
731
Bulletin of Biological and Allied Sciences Research 2024, 66–66. https:
732
//doi.org/10.54112/bbasr.v2024i1.66.
733

Karpukhin, V., Oguz, B., Min, S., Lewis, P.S., Wu, L., Edunov, S., Chen,
734
D., Yih, W.t., 2020. Dense passage retrieval for open-domain question
735
answering., in: EMNLP (1), pp. 6769–6781. https://doi.org/10.18653/
736
v1/2020.emnlp-main.550.
737

Kasai, J., Sakaguchi, K., Le Bras, R., Asai, A., Yu, X., Radev, D., Smith,
738
N.A., Choi, Y., Inui, K., et al., 2023. Realtime qa: What’s the answer right
739
now? Advances in neural information processing systems 36, 49025–49043.
740
https://doi.org/10.48550/arXiv.2207.13332.
741

Kpodo, J., Kordjamshidi, P., Nejadhashemi, A.P., 2024. Agxqa: A bench742
mark for advanced agricultural extension question answering. Computers
743
and Electronics in Agriculture 225, 109349. https://doi.org/10.1016/
744
j.compag.2024.109349.
745

Kuska, M.T., Wahabzada, M., Paulus, S., 2024. Ai for crop production–
746
where can large language models (llms) provide substantial value? Com747
puters and electronics in agriculture 221, 108924. https://doi.org/10.
748
1016/j.compag.2024.108924.
749

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N.,
750
Küttler, H., Lewis, M., Yih, W.t., Rocktäschel, T., et al., 2020. Retrieval751
augmented generation for knowledge-intensive nlp tasks. Advances in neu752
ral information processing systems 33, 9459–9474. https://doi.org/10.
753
48550/arXiv.2005.11401.
754

Li, S., Yuan, Z., Peng, R., Leybourne, D., Xue, Q., Li, Y., Yang, P., 2024.
755
An eﬀective farmer-centred mobile intelligence solution using lightweight
756
deep learning for integrated wheat pest management. Journal of Industrial
757
Information Integration 42, 100705. https://doi.org/10.1016/j.jii.
758
2024.100705.
759

33

---

Liu, J., Zhou, C., Zhu, Y., Yang, B., Liu, G., Xiong, Y., 2025. Ricepest-detr:
760
A transformer-based model for accurately identifying small rice pest by
761
end-to-end detection mechanism. Computers and Electronics in Agricul762
ture 235, 110373. https://doi.org/10.1016/j.compag.2025.110373.
763

Lv, B., Wu, H., Chen, W., Chen, C., Miao, Y., Zhao, C., 2024. Veg-mmkg:
764
Multimodal knowledge graph construction for vegetables based on pre765
trained model extraction. Computers and electronics in agriculture 226,
766
109398. https://doi.org/10.1016/j.compag.2024.109398.
767

Qian, X., Zhang, Y., Zhao, Y., Zhou, B., Sui, X., Zhang, L., Song, K.,
768
2024.
Timer4: Time-aware retrieval-augmented large language models
769
for temporal knowledge graph question answering, in: Proceedings of the
770
2024 Conference on Empirical Methods in Natural Language Processing,
771
pp. 6942–6952. https://doi.org/10.18653/v1/2024.emnlp-main.394.
772

Rezayi, S., Liu, Z., Wu, Z., Dhakal, C., Ge, B., Dai, H., Mai, G., Liu, N.,
773
Zhen, C., Liu, T., Li, S., 2025. Exploring new frontiers in agricultural nlp:
774
Investigating the potential of large language models for food applications.
775
IEEE Transactions on Big Data 11, 1235–1246. https://doi.org/10.
776
1109/TBDATA.2024.3442542.
777

Robertson, S., Zaragoza, H., et al., 2009. The probabilistic relevance frame778
work: Bm25 and beyond. Foundations and Trends® in Information Re779
trieval 3, 333–389. http://dx.doi.org/10.1561/1500000019.
780

Shafay, M., Hassan, T., Owais, M., Hussain, I., Khawaja, S.G., Senevi781
ratne, L., Werghi, N., 2025.
Recent advances in plant disease detec782
tion:
challenges and opportunities.
Plant Methods 21, 140.
https:
783
//doi.org/10.1186/s13007-025-01450-0.
784

Singh, A., Shraogi, N., Verma, R., Saji, J., Kar, A.K., Tehlan, S., Ghosh,
785
D., Patnaik, S., 2024. Challenges in current pest management practices:
786
Navigating problems and a way forward by integrating controlled release
787
system approach.
Chemical Engineering Journal 498, 154989.
https:
788
//doi.org/10.1016/j.cej.2024.154989.
789

Tzachor, A., Devare, M., Richards, C., Pypers, P., Ghosh, A., Koo, J.,
790
Johal, S., King, B., 2023.
Large language models and agricultural ex791
tension services. Nature food 4, 941–948. https://doi.org/10.1038/
792
s43016-023-00867-x.
793

34

---

Vizniuk, A., Diachenko, G., Laktionov, I., Siwocha, A., Xiao, M., Smolg,
794
J., 2025. A comprehensive survey of retrieval-augmented large language
795
models for decision making in agriculture: Unsolved problems and research
796
opportunities. Journal of Artiﬁcial Intelligence and Soft Computing Re797
search 15, 115–146. https://doi.org/10.2478/jaiscr-2025-0007.
798

Wang, L., Yang, N., Huang, X., Yang, L., Majumder, R., Wei, F., 2024.
799
Multilingual e5 text embeddings:
A technical report.
arXiv preprint
800
arXiv:2402.05672. https://doi.org/10.48550/arXiv.2402.05672.
801

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., Le, Q.V.,
802
Zhou, D., et al., 2022. Chain-of-thought prompting elicits reasoning in
803
large language models. Advances in neural information processing systems
804
35, 24824–24837. https://doi.org/10.48550/arXiv.2201.11903.
805

Wu, F., Liu, L., He, W., Liu, Z., Zhang, Z., Wang, H., Wang, M., 2024.
806
Time-sensitve retrieval-augmented generation for question answering, in:
807
Proceedings of the 33rd ACM International Conference on Information and
808
Knowledge Management, pp. 2544–2553.
https://doi.org/10.1145/
809
3627673.3679800.
810

Yan, R., An, P., Meng, X., Li, Y., Li, D., Xu, F., Dang, D., 2025.
A
811
knowledge graph for crop diseases and pests in china. Scientiﬁc Data 12,
812
222. https://doi.org/10.1038/s41597-025-04492-0.
813

Yang, B., Zhang, Y., Feng, L., Chen, Y., Zhang, J., Xu, X., Aierken, N.,
814
Li, Y., Chen, Y., Yang, G., et al., 2025. Agrigpt: A large language model
815
ecosystem for agriculture. arXiv preprint arXiv:2508.08632. https://doi.
816
org/10.48550/arXiv.2508.08632.
817

Yao, X., Hao, X., Liu, R., Li, L., Guo, X., 2024.
Agcner, the ﬁrst
818
large-scale chinese named entity recognition dataset for agricultural dis819
eases and pests.
Scientiﬁc Data 11, 769.
https://doi.org/10.1038/
820
s41597-024-03578-5.
821

Ye, K., Hu, G., Tong, Z., Xu, Y., Zheng, J., 2025. Key intelligent pesti822
cide prescription spraying technologies for the control of pests, diseases,
823
and weeds: A review. Agriculture 15, 81. https://doi.org/10.3390/
824
agriculture15010081.
825

35

---

Yi, W., Zhang, L., Kuzmin, S., Gerasimov, I., Liu, M., 2025. Agricultural
826
large language model for standardized production of distinctive agricul827
tural products. Computers and Electronics in Agriculture 234, 110218.
828
https://doi.org/10.1016/j.compag.2025.110218.
829

Youdao, N., 2023. Bcembedding: Bilingual and crosslingual embedding for
830
rag.
https://github.com/netease-youdao/BCEmbedding/ (Accessed:
831
26 November 2025).
832

Yuan, Z., Liu, K., Li, S., Peng, R., Leybourne, D., Musa, N., Yang, P., 2025.
833
Pezego: A precision agriculture system based on large language models and
834
internet of things for pest management. IEEE Internet of Things Journal
835
12, 49120–49130. https://doi.org/10.1109/JIOT.2025.3586374.
836

Zhang, L., Zhang, H., Wang, C., Liang, P., 2024a. Rag-enhanced commit
837
message generation. arXiv preprint arXiv:2406.05514. https://doi.org/
838
10.48550/arXiv.2406.05514.
839

Zhang, S., Xue, Y., Zhang, Y., Wu, X., Luu, A.T., Zhao, C., 2024b.
840
Mrag:
A modular retrieval framework for time-sensitive question an841
swering. arXiv preprint arXiv:2412.15540 https://doi.org/10.48550/
842
arXiv.2412.15540.
843

Zhang, Y., Li, M., Long, D., Zhang, X., Lin, H., Yang, B., Xie, P., Yang, A.,
844
Liu, D., Lin, J., Huang, F., Zhou, J., 2025. Qwen3 embedding: Advancing
845
text embedding and reranking through foundation models. arXiv preprint
846
arXiv:2506.05176. https://doi.org/10.48550/arXiv.2506.05176.
847

Zhao, X., Chen, B., Ji, M., Wang, X., Yan, Y., Zhang, J., Liu, S., Ye, M.,
848
Lv, C., 2024. Implementation of large language models and agricultural
849
knowledge graphs for eﬃcient plant disease detection. Agriculture 14, 1359.
850
https://doi.org/10.3390/agriculture14081359.
851

Zheng, Y., Qi, J., Yang, Y., Yang, P., Yuan, Z., 2025.
Aphid-yolo: A
852
lightweight detection model for real-time identiﬁcation and counting of
853
aphids in complex ﬁeld environments. IEEE Transactions on AgriFood
854
Electronics 3, 605–614. https://doi.org/10.1109/TAFE.2025.3600008.
855

36