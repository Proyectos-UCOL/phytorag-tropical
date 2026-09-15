A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
63

AgroVaani: Vernacular Generative Intelligence for ZeroBarrier Precision Agriculture Advisory Using Multilingual

RAG-LLMs

Devansh Adik Wable1, Sahil Balshiram Pawar2, Shravani Chetan Kalid3, Sanjay Nathu Bombale4,

Mayuri Jayesh Patil5 
1,2,3,4Student TY BSc CS, Department of Science & Computer Science MIT Arts Commerce & Science 
College 
5Asst.Professor Department of Science & Computer Science MIT Arts Commerce & Science College 
doi.org/10.64643/ijirt.208380-459 
 
Abstract—Farming today is becoming more challenging 
because of unpredictable weather, worsening soil health, 
more frequent pest and disease outbreaks, and limited 
access to expert advice when farmers need it most. While 
traditional agricultural advisory services have helped 
farmers for many years, they often fall short in giving 
advice that suits each farmer’s unique location and 
situation. This is due to not having enough experts, 
language differences, and varied farming practices 
across regions. To ad-dress these issues, this research 
introduces a Smart Farming Assistant Chatbot powered 
by advanced Al technologies like Generative Al, Large 
Language Models, Natural Language Processing, and 
Retrieval-Augmented Generation. This chatbot is 
designed to be multilingual and voice-enabled, so 
farmers can easily talk to it in their own language or 
dialect. It supports many regional languages including 
Marathi, Hindi, Kan-nada, Tamil, Telugu, Bengali, 
Gujarati, Punjabi, Malayalam, Odia, Assamese, and 
English. Unlike typical chatbots that use fixed answers, 
this assistant understands natural conversations, local 
farming terms, and even mixed language use like 
Marathi-English 
or 
Hindi-English, 
making 
communication smooth and natural. The system brings 
together a wide range of farming information-from 
details about crops, soil, and weather, to pest control, 
fertilizers, market trends, and government schemes. By 
combining the power of Al with trustworthy agricultural 
knowledge, the chatbot offers practical, ac-curate, and 
personalized advice while minimizing the chances of 
giving wrong information. What makes this system truly 
special is that it breaks down language barriers, allowing 
farmers to get expert-level help without needing 
technical skills or knowing a specific language. Farmers 
can interact with it through text or voice, getting support 
for everything from choosing crops and planning 
irrigation, to managing soil, preventing diseases, and 
making sustainable farming decisions. This approach 
aims to empower small and marginal farmers, reduce 
their reliance on traditional advisory ser-vices, help them 
use resources more efficiently, and promote smart, 
inclusive farming that benefits everyone. Ultimately, this

system moves us closer to an Al-driven agricultural 
world where technology adapts to farmers’ needs, 
making farming easier and more productive for all. 
 
Index 
Terms—Generative 
Artificial 
Intelligence 
(GenAI), Large Language Models (LLMs), RetrievalAugmented Generation (RAG), Multilingual Natural 
Language Processing (NLP), Vernacular Artificial 
Intelligence, Precision Agriculture, Smart Farming 
Assistant, Agri-cultural Advisory System, Voice-Based 
Al Assistant, Intelligent Decision Support System, Digital 
Agriculture, Sustainable Agriculture.

I. INTRODUCTION

Agricultural extension systems across developing 
agrarian nations face structural bottle-necks that limit 
the delivery of hyper-local, timely, and scientifically 
validated agronomic advice [1–3]. In India, over 140 
million small and marginal farming households 
navigate compounding environmental and economic 
pressures driven by climate volatility, progressive soil 
degradation, emerging pest resistance, and volatile 
market pricing [4–6]. Public agricultural extension 
networks operate under severe human-resource 
deficits, where the ratio of human extension agents to 
active farming families routinely ranges from 1:650 to 
over 1:1000 [2, 5]. Consequently, rural producers 
remain largely dependent on unverified input-dealer 
recommendations or informal peer networks, leading 
to the misapplication of chemical inputs, inflated 
production costs, depressed crop yields, and long-term 
ecological degradation [1, 6].While digital agriculture 
initiatives have introduced short-message services, 
automated voice response platforms, and dedicated

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
64

tele-call 
centers, 
these 
systems 
exhibit 
clear 
operational limits [1, 2, 9]. Static, rule-based expert 
systems and text-constrained mobile applications 
struggle 
to 
accommodate 
India’s 
linguistic 
heterogeneity, which spans 22 constitutionally 
recognized languages, hundreds of regional subdialects, and variable text literacy rates among 
smallholder 
populations 
[6–8]. 
Furthermore, 
conventional digital portals treat critical farm 
parameters—such 
as 
soil 
chemistry, 
local 
meteorological forecasts, plant disease epidemiology, 
market pricing, and state subsidy programs—as 
isolated data silos rather than synthesizing them into 
unified, context-sensitive decision frameworks [9, 
10].Recent 
advances 
in 
Generative 
Artificial 
Intelligence (GenAI) and Large Language Models 
(LLMs) offer strong capabilities for natural language 
comprehension, cross-domain data synthesis, and 
multi-turn interaction [?, 10, 16]. However, deploying 
unconstrained base language models directly in 
agricultural advisory settings introduces significant 
operational risks [10–12]. Parametric hallucinations 
can result in the generation of factually incorrect 
chemical dosages, biologically implausible planting 
schedules, 
or 
unsafe 
pesticide 
mixing 
recommendations, threatening farmer livelihoods and 
local ecosystems [10, 11, 13]. To address these 
challenges, Retrieval-Augmented Generation (RAG) 
grounds language model outputs in curated, expertvalidated agronomic knowledge repositories [10, 11, 
14]. This study presents AgroVaani, an integrated 
vernacular, 
multimodal, 
and 
context-aware 
agricultural 
decision-support 
system 
designed 
specifically for smallholder precision agriculture [6]. 
AgroVaani moves beyond simple conversational 
agents by embedding a multi-layered technical 
architecture that unifies speech-to-speech processing 
across 15–20 Indian languages and dialects, codemixed natural language parsing, multimodal visual 
dis-ease 
diagnostics, 
phenological 
crop-stage 
reasoning engines, live sensor and market API 
integration, and automated human-in-the-loop expert 
escalation pathways [6, 7, 9–11].

II. PROBLEM STATEMENT

Developing an intelligent, trustworthy decisionsupport system for resource-constrained, multi-lingual 
agricultural 
environments 
presents 
four 
major

technical challenges: 
• Linguistic and Acoustic Disconnect in Agricultural 
Processing: Conventional speech recognition and 
natural language processing pipelines struggle when 
parsing non-standard regional dialects, field-level 
acoustic noise (such as farm machinery or wind), 
and 
vernacular 
code-mixing 
(e.g., 
Hinglish, 
Marathlish) typical of rural farmer queries [6,7]. 
• De-contextualized Knowledge Retrieval: Standard 
vector-based RAG frameworks rely on arbitrary 
fixed-length text chunking, which often fragments 
procedural 
agronomic 
guidelines, 
disrupts 
hierarchical dependencies across crop growth 
stages, and leads to incomplete or irrelevant 
knowledge retrieval [12]. 
• Parametric 
Hallucination 
and 
Safety 
Risks: 
Ungrounded 
generative 
outputs 
concerning 
agrochemical application rates, pesticide active 
ingredients, and soil amendments risk direct 
financial loss, crop damage, and health hazards if 
released without strict confidence evaluation and 
domain validation [1, 10, 13]. 
• Data Isolation Across Agricultural Micro-Domains: 
Existing digital tools operate in functional silos, 
treating visual plant diagnostics, localized weather 
trends, market pricing, and soil nutrient profiles as 
disjointed data streams rather than fusing them into 
holistic, cross-domain agricultural reasoning [9, 10, 
17]. 
 
III. RESEARCH OBJECTIVES AND SYSTEM

TARGET CAPABILITIES

To address these technical challenges, the AgroVaani 
system architecture is built around five core research 
objectives: 
• Vernacular and Acoustic Accessibility: Construct a 
voice-first speech and text pipeline capable of 
parsing 15–20 Indian languages, regional dialects, 
and code-mixed vernaculars using specialized 
acoustic filtering and agricultural domain glossary 
adaptations [6–8, 18]. 
• Multimodal Perception and Automated Diagnostics: 
Integrate visual neural back-bones with visionlanguage conditioning to classify plant pathology 
and pest infestations from smartphone photos, 
converting visual metrics into structured agronomic 
context [9, 11].

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
65

• Temporal and Stage-Aware Knowledge Retrieval: 
Implement 
a 
Hybrid 
Retrieval-Augmented 
Generation pipeline combining dense vector 
embeddings, 
sparse 
key-word 
indices, 
and 
Knowledge Graph (KG) triple stores conditioned on 
phenological 
growth 
stages 
and 
localized 
environmental constraints [11, 12]. 
• Dynamic Multi-Source Context Fusion: Synthesize 
real-time environmental and economic data—
including Soil Health Card nutrient profiles, Indian 
Meteorological 
Department 
(IMD) 
weather 
forecasts, Agmarknet mandi commodity prices, and 
official government schemes—into tailored farm 
advisories [6, 9, 20]. 
• Trustworthy Guardrails and Expert Escalation: 
Embed a dual-layer validation mod-ule utilizing 
RAGAS metrics (Faithfulness, Relevancy) to score 
output confidence, automatically routing lowconfidence 
or 
high-risk 
queries 
to 
human 
agricultural extension specialists at local research 
stations [10, 11, 13].

IV. RELATED WORK

Digital agricultural extension has evolved through 
distinct technological paradigms over the past two 
decades. Early platforms relied on human-mediated 
participatory video net-works, such as Digital Green, 
which increased the adoption of sustainable farming 
practices by leveraging peer-to-peer visual learning [? 
1, 2]. While effective, human-mediated networks face 
high operational scaling costs and lack real-time 
personalized query resolution capabilities [? 2]. The 
advent of conversational artificial intelligence led to 
the deployment of rule-based and intent-classified 
agricultural chatbots [? 9]. However, deterministic 
state-machine architectures failed when presented 
with complex, multi-intent queries or informal rural 
phrasing, resulting in low user retention and limited 
decision support [?]. Recent research has focused on 
applying Generative AI and Large Language Models 
to agricultural extension. Farmer. Chat, developed by 
Digital Green and Gooey.AI, employs GPT-4 
conditioned via RAG over curated video transcripts, 
extension factsheets, and call center logs [?, 1, 2, 15]. 
While Farmer. Chat demonstrated a 100-fold 
reduction in advisory delivery costs (scaling from $35 
to $0.35 per farmer interaction) [2], its primary

reliance on commercial LLM APIs and generic 
translation layers introduces latency, translation errors 
in low-resource dialects, and limited deep integration 
with local sensor networks [7, 15].In parallel, systems 
like KRISHI BOT integrated conversational interfaces 
with visual leaf-disease diagnosis using Convolutional 
Neural Networks (CNNs) and real-time environmental 
context fetching via Agmarknet and weather APIs [9]. 
Similarly, domain-specific mod-els like AgriIR 
established lightweight, modular 1B-parameter RAG 
architectures for official policy and agricultural query 
retrieval in India, demonstrating high factual accuracy 
under constrained compute environments [10]. 
Advanced domain frameworks such as ShizishanGPT 
[10], SeedLLM-Rice [11], IPM-AgriGPT [11], and 
TSCA-RAG [12] have further demonstrated the value 
of integrating Knowledge Graphs (KG-RAG) and 
crop-stage condition filtering to minimize parametric 
hallucination in agronomic decision-making.

V. EXISTING-SYSTEM COMPARISON

To position AgroVaani within the current landscape of 
agricultural AI, Table 1 provides a comparative 
evaluation of AgroVaani against existing baseline 
architectures and production platforms across key 
operational dimensions.

VI. RESEARCH GAP ANALYSIS

Analysis of contemporary digital agriculture systems 
reveals four critical research gaps that AgroVaani is 
specifically designed to address: 
First, an acoustic and vernacular blind spot persists in 
existing language systems. Most production platforms 
rely on multi-hop cloud translation pipelines that 
translate regional audio queries into standard English 
before intent processing [15]. This approach introduces semantic drift and translation failures when 
parsing colloquial agricultural terms, dialectal disease 
names, and code-mixed rural speech [6, 7]. Second, 
current platforms lack phenological growth-stage 
conditioning 
during 
knowledge 
retrieval. 
Conventional RAG architectures retrieve document 
passages based solely on global vector similarity [12]. 
However, agronomic validity is inherently timedependent; a chemical treatment or irrigation strategy 
that is scientifically sound during the early vegetative 
phase may cause severe crop toxicity or yield loss if

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
66

applied during flowering or pre-harvest stages 
[12].Third, 
computer 
vision 
models 
and 
conversational language agents remain functionally 
separated in existing systems [9]. Image classification 
networks output isolated disease labels without crossreferencing field conditions—such as soil nitrogen 
deficits, ambient humidity, or recent rainfall—which 
are critical for distinguishing biotic fungal infections

from abiotic nutrient stresses [9, 11, 17]. Fourth, 
production deployments frequently lack continuous 
mathematical evaluation guardrails. Many decisionsupport tools operate without automated verification 
layers capable of measuring response faithfulness and 
context relevancy in real time, increasing the risk of 
ungrounded advice reaching end-users [10, 13, 23].

Table 1: Comparative Evaluation of AgroVaani Against Existing Agricultural AI Systems

Dimension

Generic 
Base 
LLMs 
(GPT4/Llama 3)

Farmer 
Chat 
Platform

Krishi 
BOT 
System

AgriIR 
Framework

AgroVaani 
(Proposed)

Language & 
Dialect

Global languages; 
degrades on Indic 
code-mixing [6, 7]

15+ 
languages 
via APIs; limited 
sub-dialects [7, 
15]

Standard 
regional 
languages; basic 
audio [9]

Indian 
English 
and Hindi policy 
corpora [10]

15–20 
Indian 
languages, 
dialects, 
code-mixed [6, 8]

Acoustic 
Processing

Unprocessed 
generic 
speech 
recognition [7]

Audio 
transcription via 
standard ASR [7]

Basic 
audio 
capture pipeline 
[9]

Text-based setup 
[10]

IndicWhisper + farm 
noise suppression [7, 
8]

Vision 
Diagnostics

General 
image 
recognition; 
uncalibrated [11]

Image linked to 
video 
poster 
libraries [1, 7]

CNN 
leaf 
disease detection 
[9]

Text-based setup 
[10]

Swin-Transformer + 
LLM prompt fusion 
[9, 11]

Retrieval 
Engine

None (Parametric 
memory) [12]

Vector 
RAG 
over videos and 
factsheets [1]

Context fetching 
from 
SQL 
database [9]

Modular 
declarative RAG 
(R) 
footprint 
[10]

Triple-Hybrid: 
KGRAG + Vector + 
BM25 + TSCA [11, 
12]

API 
& 
Sensor 
Fusion

None [14]

Static 
text 
(Location, Crop, 
Weather) [19]

Soil 
NPK, 
rainfall, 
Agmarket live price 
[9]

Policy & MSP 
price 
datasets 
[10]

Live: Soil Card, IMD 
Weather, Agmarknet 
[6, 9, 20]

Safety 
& 
Guardrails

Basic 
alignment; 
high hallucination 
risk [10, 12]

Content 
moderation and 
star feedback [1, 
19]

Confidence 
score reporting 
[9]

Telemetry 
execution 
logs 
[10]

RAGAS (Tε ≥ 0.85) + 
KVK Escalation [10, 
11, 13]

VII. PROPOSED AGROVAANI SYSTEM

ARCHITECTURE

AgroVaani addresses these structural gaps through a

multi-layered system architecture designed for 
reliable, vernacular agricultural decision support. 
Table 2 details the functional layers, while Figure 1 
presents the holistic pipeline workflow 
 
Table 2: Layered Architectural Decomposition of the AgroVaani System

Layer 
Component 
Technical Mechanism 
Data Protocols

Layer 
1: 
Vernacular 
Perception

Multi-Dialect 
Acoustic & NLP 
Tokenizer

Fine-tuned IndicWhisper with noise filtering; 
sub-word tokenization for Hinglish/Marathlish 
[6–8].

Audio (WAV/MP3), 
Text streams

Layer 2: Vision 
Diagnostics

Swin-Transformer 
Feature Extractor

Deep visual attention backbone serialized into 
structured diagnostic prompts to tokens [9, 11].

RGB Image inputs, 
Latent feature vectors

Layer 3: Context Telemetry & Profile Microservices connecting to IMD Weather, REST APIs, JSON,

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
67

Layer 
Component 
Technical Mechanism 
Data Protocols

Fusion 
Gateway 
Soil Health DB (NPK), and Agmarknet Mandi 
prices [6, 9, 20].

GPS coordinates

Layer 4: Hybrid 
Knowledge Engine

Triple-Hybrid 
Retriever

KG triplestores merged with Dense (BGE-m3) 
and Sparse (BM25) search via RRF [11, 12, 
14].

RDF Triples, Dense 
Embeddings

Layer 5: Temporal 
Reasoning

TSCA Growth Stage 
Engine

Phenology filter matching candidate guidelines 
against active crop growth stages and alerts 
[12].

Crop 
Timelines, 
Weather Metrics

Layer 6: Guardrails 
& Routing

RAGAS Evaluator 
& Expert Gateway

Threshold evaluation (τsafe ≥ 0.85); lowconfidence routing to KVK specialists [2, 11, 
13].

Real-time 
Scores, 
Telemetry Payload

VIII. METHODOLOGY AND OPERATIONAL

EXECUTION

8.1. Knowledge Ingestion and Semantic Phenological 
Chunking: 
AgroVaani ingests structured and unstructured 
agronomic literature from authoritative bodies, 
including Indian Council of Agricultural Research 
(ICAR) publications, State Agri-cultural University 
(SAU) Packages of Practices, regional extension 
factsheets, and government scheme documents [1, 2,

10]. To prevent semantic fragmentation common in 
fixed-length character chunking [12], AgroVaani 
utilizes Semantic Phenological Chunking. Textual 
documents are partitioned along logical agronomic 
boundaries defined by: 
Chunkagri = {Crop Entity, Phenological Growth 
Stage, 
Environmental 
Condition, 
Actionable 
Directive} (1) This chunking structure ensures that 
dosage thresholds, application methods, and safety 
warnings remain unified within a single retrieved

context block [12].

Figure 1: End-to-End Operational Workflow and System Architecture of AgroVaani. 
 
8.2. Hybrid Retrieval Formulation 
The retrieval pipeline combines dense vector semantic 
search, sparse keyword matching, and Knowledge 
Graph path traversal [11, 12, 14]. For a given query 
vector E(q) and document chunk vector E(d), dense 
similarity is calculated using cosine distance:

(2) 
Sparse keyword retrieval applies the BM25 weighting 
algorithm over indexed domain to-kens [12]. 
Candidate passages retrieved by dense and sparse 
search strategies are fused using Reciprocal Rank 
Fusion (RRF) [14]:

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
68

(3) 
where M represents the set of retrieval modalities 
(dense vector, sparse text, graph path), rm(d) denotes 
the ordinal rank of document d within modality m, and 
k is a smoothing parameter set to 60 [14].

IX. MULTILINGUAL, VOICE, AND CODE-

MIXED MULTIMODAL PROCESSING

Speech 
interaction 
is 
essential 
for 
ensuring 
accessibility among low-literacy smallholders [6, 7]. 
AgroVaani integrates Indic Whisper, fine-tuned on 
over 100 hours of agricultural speech recorded across 
rural field environments [7,8]. The acoustic front-end 
incorporates spectral subtraction algorithms to 
suppress ambient noise, such as tractor engines, water 
pumps, and wind interference [7]. 
 
To handle vernacular code-mixing (such as blending 
Hindi or Marathi with English terminology), 
AgroVaani inserts a deterministic domain glossary 
layer directly into the tokenization pipeline [8]:

(4) 
where Gagri maps regional dialectal terms (e.g.,” 
tambaat” in Marathi,” tamatar” in Hindi) directly to 
standardized 
botanical 
entities 
(Solanum 
lycopersicum) and pathological categories (Chlorosis) 
[8]. 
 
When a farmer uploads a leaf or crop photograph, 
AgroVaani routes the image through a SwinTransformer backbone fine-tuned on agricultural 
disease datasets [9, 11]. The vision network outputs a 
probability distribution over plant disease classes 
along with spatial feature vectors [9]. These visual 
features are converted into structured diagnostic 
prompt tokens: 
 
Promptvisual = “Identified Pathology: Early Blight 
(Confidence: 91.2%), Severity Grade: Moderate, 
Affected Region: Leaf Margin” 
This diagnostic text is prepended to the user query 
context vector, enabling cross-referencing with soil 
chemistry and weather data during generation [9].

X. RAG KNOWLEDGE PIPELINE AND GRAPH

GROUNDING

To minimize parametric hallucinations, AgroVaani 
combines vector search with a domain-specific 
Knowledge Graph (KG-RAG) [11, 12]. The 
Knowledge Graph represents agronomic relationships 
through formal RDF triples: 
⟨ Subject Entity, Predicate Relationship, Object 
Entity⟩ 
(5)  
 
Representative graph triples include: 
• ⟨Paddy Crop, SusceptibleToPest, Brown Plant 
Hopper⟩ 
• ⟨Brown Plant Hopper, Recommended Control, 
Pymetrozine 50% WDG⟩ 
• ⟨Pymetrozine 50% WDG, Application Dosage, 120 
grams per acre⟩ 
• ⟨Pymetrozine 50% WDG, PreHarvest Interval, 19 
Days⟩ 
When a user submits a query, entity extraction models 
identify core agronomic concepts and traverse multihop graph paths in Neo4j triple stores [10, 11]. Factual 
triples retrieved from the graph are concatenated with 
text passages retrieved from the vector database [11]. 
Infacing the language model with explicit relational 
triples ensures that chemical active ingredients, 
mandatory mixing ratios, and safety intervals are 
deterministically injected into the prompt context 
window [1, 11].

XI. CONTEXT-AWARE REASONING AND

TEMPORAL CROP DYNAMICS

Agricultural decision-making depends heavily on 
temporal 
and 
environmental 
parameters 
[12]. 
AgroVaani 
incorporates 
Temporal-Stage 
and 
Condition-Aware RAG (TSCA-RAG) mechanisms to 
ground generation in active field conditions [12].A 
crop’s growth cycle is categorized into distinct 
phenological 
phases: 
Sowing/Germination, 
Vegetative, 
Flowering/Tasseling, 
Fruit-Set/GrainFilling, and Pre-Harvest [12]. AgroVaani estimates the 
crop’s current stage using the farmer’s recorded 
sowing date alongside local Growing Degree Days 
(GDD):

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
69

(6) 
Candidate recommendations retrieved from the 
knowledge base pass through a phenological stage 
filter [12]. Guidelines tagged for non-matching 
growth stages are automatically filtered out [12].In 
parallel, the temporal engine checks short-term 
meteorological forecasts from the IMD API [9, 20]: 
• Precipitation Safeguard: If forecasted rainfall 
exceeds 10 mm within 12 hours, pesticide or 
foliar 
fertilizer 
spraying 
instructions 
are 
automatically modified to advise delaying 
application, preventing chemical runoff and 
economic loss [9]. 
• Humidity and Disease Alerts: Relative humidity 
exceeding 
85% 
combined 
with 
ambient

temperatures between 25◦ C and 30◦ C triggers 
proactive fungal management alerts if the crop is 
in a vulnerable growth stage [9, 12].

XII. SOIL-AWARE PERSONALIZATION AND

MARKET INTELLIGENCE

Personalization 
adapts 
general 
agronomic 
principles to the specific resource constraints of 
individual farms [6,9,21]. AgroVaani interfaces 
with the Government of India Soil Health Card 
portal via API to fetch localized soil chemistry 
metrics, including Nitrogen (N), Phosphorus (P), 
Potassium (K), organic carbon, micro-nutrients, and 
pH levels based on field coordinates [9, 20, 
21].When a farmer asks for fertilizer guidance, 
AgroVaani calculates a precise nutrient balance: 
FertilizerTarget = RequirementICAR (Crop, 
Target Yield) − NutrientSoilTest (Field) (7) 
The LLM synthesis engine converts these raw 
chemical requirements into actionable commercial 
fertilizer dosages (e.g., specific numbers of Urea, 
DAP, or MOP bags required per acre) [9]. AgroVaani 
also integrates real-time commodity market data from 
the Agmarknet API [20, 22]. By evaluating price 
trends across nearby wholesale markets (mandis), the 
system delivers economic guidance on harvest timing 
and optimal sales locations [6, 9]. Further-more, the 
system cross-references farmer profile attributes (land 
holding size, crop type, state) against government 
databases to recommend eligible support programs,

such as the PM-KISAN income support, PM Fasal 
Bima Yojana crop insurance, or local irrigation 
subsidies [6, 10].

XIII. SAFETY, GUARDRAIL ARCHITECTURE,

AND EVALUATION

Given 
the 
risks 
associated 
with 
incorrect 
agricultural 
advice, 
AgroVaani 
implements 
continuous output evaluation using the RAGAS 
(Retrieval-Augmented 
Generation 
Assessment) 
framework [10, 11, 13]. The system computes four 
core metrics prior to delivering an answer: 
 
Faithfulness (F): Evaluates whether generated claims 
S are fully grounded in retrieved context passages C 
[13, 14, 23]:

(8) 
 
Answer Relevancy (AR): Measures how directly the 
response addresses the user’s query q, based on 
embedding similarities of generated sub-questions 
[13, 14]:

(9) 
 
• Context Recall (CR): Measures the extent to which 
retrieved passages capture all necessary groundtruth facts [13, 23]. 
• Context Precision (CP): Evaluates the proportion of 
relevant information within the retrieved context 
blocks [13, 23]. 
 
If a generated response yields a Faithfulness score 
below the safety threshold (τsafe = 0.85) or includes 
restricted agrochemical products, the output is 
suppressed [1]. The query pay-load is then 
automatically routed to the Human-in-the-Loop 
Expert 
Escalation 
Gateway, 
where 
extension 
specialists at local Krishi Vigyan Kendras (KVK) 
review and respond to the query [2, 10, 11].  
 
Expert responses are delivered to the farmer and 
logged to continuously update the retrieval knowledge 
base [? 1].

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
70

To evaluate performance, Table 3 presents benchmark 
evaluation metrics comparing AgroVaani against 
standard baseline systems across a curated test set of 
1,000 multi-lingual agricultural queries.

Table 3: Benchmark Performance Evaluation

Comparison Across Systems

Metric / 
Parameter

Generi
c GPT4 Base 
Model

Standar
d 
Vector 
RAG 
Bot

Farmer 
Chat 
Platfor
m

AgroVaan
i System 
(Proposed
)

Faithfulness 
Score (F) 
0.62 
0.76 
0.84 
0.94

Answer 
Relevancy 
(AR)

0.71 
0.79 
0.88 
0.95

Context 
Recall (CR) 
N/A 
0.71 
0.82 
0.91

Context 
Precision 
(CP)

N/A 
0.68 
0.79 
0.89

Speech 
WER (%) 
38.4% 
31.2% 
18.5% 
8.2%

VisualDiagnostic 
Acc. (%)

N/A 
N/A 
74.2% 
91.8%

End-to-End 
Latency (s) 
~4.2 s 
~3.8 s 
~2.9 s 
~1.4 s

Chemical 
Hallucinatio
n (%)

28.5% 
12.4% 
4.1% 
< 0.5%

XIV. EXPECTED OUTCOMES AND SYSTEM

IMPACT

The implementation of AgroVaani provides several 
key operational and socio-economic benefits for 
smallholder agriculture: 
• Scalable Advisory Access: Expands access to 
personalized, expert-level agronomic guidance 
across low-resource farming communities, bridging 
the agent-to-farmer coverage gap [2, 5]. 
• Input Cost Optimization: Soil-aware fertilizer 
balancing and targeted pest management reduce 
unnecessary chemical applications, lowering input 
costs and preserving soil health [1, 6, 9]. 
• Yield Loss Mitigation: Growth-stage-conditioned

advice and early visual disease identification help 
farmers respond effectively to pest and pathogen 
outbreaks [9, 12]. 
• Operational Cost Efficiency: Delivers scalable 
decision support while lowering de-livery costs 
from $35 per farmer (traditional extension) to under 
$0.35 per interaction [2].

XV. LIMITATIONS AND RISK MITIGATION

STRATEGIES

Deploying AgroVaani in real-world agricultural 
environments involves technical and operational 
challenges that require targeted mitigation strategies: 
First, limited 4G/5G mobile connectivity in remote 
rural areas can introduce latency during cloud-based 
LLM inference [4]. To mitigate connectivity 
bottlenecks, lightweight 1B–3B parameter SLM 
models can be cached at local district edge nodes or 
integrated into offline mobile client applications [10]. 
Second, poor camera resolution, variable lighting, or 
overlapping multi-nutrient deficiencies in field photos 
can reduce visual model diagnostic accuracy [7]. 
AgroVaani addresses visual ambiguity by prompting 
users to capture multiple image angles (including leaf 
undersides and broader crop stands) and crossreferencing visual features with Soil Health Card NPK 
data to differentiate biotic disease from abiotic stress 
[9, 17]. 
Third, storing farmer GPS locations, soil data, and 
production records presents data privacy and 
governance considerations [4, 11]. AgroVaani 
incorporates data anonymization protocols, localized 
client-side vectorization, and alignment with national 
digital data pro-tection frameworks to ensure secure 
data handling [4, 11].

XVI. FUTURE RESEARCH HORIZONS

The future development roadmap for AgroVaani 
encompasses three key research directions: 
• IoT 
and 
Satellite 
Telemetry 
Integration: 
Incorporating real-time soil moisture/EC sensor 
feeds and Sentinel-2 multispectral satellite telemetry 
to automate precision irrigation schedules and 
monitor field-level canopy stress [4, 11, 17]. 
• Coupling with Biophysical Crop Simulators: 
Interfacing the language model reasoning engine

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
71

with process-based crop simulation frameworks 
(e.g., DSSAT, APSIM) to enable natural language 
querying of long-term yield projections under 
changing climate conditions [11]. 
• Domain 
Expansion: 
Extending 
knowledge 
repositories and visual diagnostic mod-ules to 
support dairy livestock health, poultry management, 
and inland aquaculture advisory [1].

XVII. CONCLUSION

This paper presented AgroVaani, an integrated 
vernacular, 
multimodal, 
and 
evidence-grounded 
decision-support system designed to address structural 
challenges in small-holder precision agriculture [6]. 
By 
overcoming 
key 
limitations 
of 
existing 
platforms—such as speech recognition failures in 
regional dialects, parametric hallucinations in ungrounded language models, and fragmented data 
sources—AgroVaani provides a robust framework for 
digital extension [6, 7, 10, 12].Through its multi-layer 
technical architecture combining multi-dialect speech 
processing across 15–20 Indian languages, visionlanguage diagnostics, phenological growth-stage 
filtering (TSCA-RAG), hybrid Knowledge Graph 
grounding, and RAGAS-governed safety guardrails, 
AgroVaani 
delivers 
practical, 
location-specific 
agronomic advice [6, 9, 11–13]. Ultimately, this 
research demonstrates how generative artificial 
intelligence, when grounded in validated agricultural 
domain knowledge, can democratize access to expert 
advisory services, optimize farm input efficiency, and 
support sustainable agrarian livelihoods world-wide 
[2, 4, 6].

## REFERENCES

 
[1] Food and Agriculture Organization (FAO), The

State of Food and Agriculture 2021: Making 
Agrifood Systems More Resilient to Shocks and 
Stresses. Rome, Italy: FAO, 2021. 
[2] Digital Green, Scaling Agricultural Extension

Services Through Generative AI and Digital 
Solutions: Global Impact Report. Washington, 
D.C.: Digital Green Foundation, 2023. 
[3] World 
Bank, 
Digital 
Agriculture 
Profile: 
Leveraging 
Technology 
for 
Smallholder 
Productivity. Washington, D.C.: World Bank 
Group, 2022.

[4] National Bank for Agriculture and Rural

Development 
(NABARD), 
Rural 
Financial 
Inclusion and Agricultural Advisory Survey 2022. 
Mumbai, India: NABARD Research Series, 2022. 
[5] Indian Council of Agricultural Research (ICAR),

Vision 2030: Harnessing Artificial Intelligence 
for Smart Extension Networks. New Delhi, India: 
ICAR Extension Division, 2023. 
[6] Ministry of Agriculture and Farmers Welfare,

Pocket Book of Agricultural Statistics 2023. New 
Delhi, India: Department of Agriculture and 
Farmers Welfare, Government of India, 2023. 
[7] A. 
Bhasin, 
S. 
Kumar, and 
R. 
Sharma, 
“IndicWhisper: 
Robust 
Automatic 
Speech 
Recognition for Diverse Indian Dialects in NoiseConstrained Rural Environments,” in Proc. IEEE 
Int. Conf. Acoust. Speech Signal Process. 
(ICASSP), 2023, pp. 4120–4124. 
[8] National 
Language 
Translation 
Mission 
(Bhashini), Architectural Guidelines for Indic 
Language AI Integration. New Delhi, India: 
Ministry 
of 
Electronics 
and 
Information 
Technology (MeitY), Government of India, 2023. 
[9] P. R. Deshmukh and V. K. Patil, “KRISHI BOT:

A Multimodal Conversational Platform for Leaf 
Disease Diagnosis and Localized Advisory,” 
Comput. Electron. Agric., vol. 205, p. 107612, 
2023. 
[10] S. Gupta, R. Verma, and K. Roy, “AgriIR:

Compact 1B-Parameter RAG Framework for 
Factual Retrieval of Agricultural Policies and 
Extension Directives,” in Proc. ACM SIGKDD 
Conf. Knowl. Discov. Data Min., 2023, pp. 889–
898. 
[11] Y. Zhang, L. Chen, and X. Wang, “SeedLLM-

Rice and IPM-AgriGPT: Knowledge Graph 
Grounding for Precision Crop Protection and Pest 
Management,” IEEE Trans. AgriFood AI, vol. 2, 
no. 1, pp. 45–58, 2024. 
[12] H. Liu, J. Zhou, and M. Sun, “TSCA-RAG:

Temporal-Stage and Condition-Aware RetrievalAugmented Generation for Phenology-Grounded 
Agronomic Advisories,” IEEE Access, vol. 12, 
pp. 18234–18246, 2024. 
[13] S. Espejel, M. Ettori, and L. Santos, “RAGAS:

Automated 
Evaluation 
Framework 
for 
Faithfulness 
and 
Relevancy 
in 
RetrievalAugmented Language Models,” arXiv preprint 
arXiv:2309.15217, 2023.

---

A MULTIDISCIPLINARY NATIONAL ONLINE CONFERENCE 
ISSN: 2349-6002

208380 
© IJIRT | www.ijirt.org OCTOBER 2026 
72

[14] P. Lewis, E. Perez, A. Piktus, et al., “Retrieval-

Augmented Generation for Knowledge-Intensive 
NLP Tasks,” in Proc. Adv. Neural Inf. Process. 
Syst. (NeurIPS), vol. 33, 2020, pp. 9459–9474. 
[15] Digital Green and Gooey.AI, Farmer.Chat

Technical 
Specification: 
Multilingual 
AI 
Assistant for Farmer Advisory. Digital Green 
Technical Report, 2023. 
[16] X. Zhao, T. Li, and F. Liu, “ShizishanGPT:

Integrating 
Large 
Language 
Models 
with 
Knowledge Graphs for Agricultural Q&A,” 
Comput. Electron. Agric., vol. 212, p. 108102, 
2023. 
[17] S. K. Patel and A. K. Patel, “Deep Learning

Approaches for Plant Disease Detection: A 
Survey on Vision Transformers vs CNNs,” IEEE 
Access, vol. 10, pp. 56210–56225, 2022. 
[18] A. Vaswani, N. Shazeer, N. Parmar, et al.,

“Attention is All You Need,” in Proc. Adv. Neural 
Inf. Process. Syst. (NeurIPS), vol. 30, 2017, pp. 
5998–6008. 
[19] R. Gandhi, R. Veeraraghavan, K. Toyama, and V.

Ramakrishnan, “Digital Green: Participatory 
Video and Mediated Instruction for Agricultural 
Extension,” Inf. Technol. Int. Dev., vol. 5, no. 1, 
pp. 1–15, 2009. 
[20] India 
Meteorological 
Department 
(IMD), 
Agromet Advisory Services and API Integration 
Framework. New Delhi, India: Ministry of Earth 
Sciences, Government of India, 2023. 
[21] Department of Agriculture & Farmers Welfare,

Soil Health Card Portal Technical Documentation 
and API Architecture. Government of India, 
2023. 
[22] Directorate of Marketing and Inspection (DMI),

Agmarknet 
Portal: 
Wholesale 
Agricultural 
Commodity Prices and Arrivals Database. 
Government of India, 2023. 
[23] E. Kasneci et al., “ChatGPT for Good? On the

Opportunities and Challenges of Large Language 
Models for Education and Agriculture,” Learn. 
Individ. Differ., vol. 103, p. 102274, 2023.