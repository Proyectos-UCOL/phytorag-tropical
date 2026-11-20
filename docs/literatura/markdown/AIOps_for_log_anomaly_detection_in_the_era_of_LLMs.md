Contents lists available at ScienceDirect

Intelligent Systems with Applications

journal homepage: www.journals.elsevier.com/intelligent-systems-with-applications

Review

AIOps for log anomaly detection in the era of LLMs: A systematic literature 
review

Miguel De la Cruz Cabello a
, Tiago Prince Sales b
, Marcos R. Machado a
,∗

a Department of Industrial Engineering and Business Information Systems, University of Twente, 7522 NB Enschede, The Netherlands
b Department of Semantics, Cybersecurity & Services, University of Twente, 7500 AE Enschede, The Netherlands

A R T I C L E  I N F O

Keywords:
AIOps
Log anomaly detection
Large Language Models
Retrieval Augmentation Generation

A B S T R A C T

Modern IT systems generate large volumes of log data that challenge timely and effective anomaly detection. 
Traditional methods often require intensive feature engineering and struggle to adapt to dynamic operational 
environments. This Systematic Literature Review (SLR) analyzes how Artificial Intelligence for IT Operations 
(AIOps) benefits from advanced language models, emphasizing Large Language Models (LLMs) for more 
effective log anomaly detection. By comparing state-of-art frameworks with LLM-driven methods, this study 
reveals that prompt engineering – the practice of designing and refining inputs to AI models to produce accurate 
and useful outputs – and Retrieval Augmented Generation (RAG) boost accuracy and interpretability without 
extensive fine-tuning. Experimental findings demonstrate that LLM-based approaches significantly outperform 
traditional methods across evaluation metrics that include F1-score, precision, and recall. Furthermore, the 
integration of LLMs with RAG techniques has shown a strong adaptability to changing environments. The 
applicability of these methods also extends to the military industry. Consequently, the development of 
specialized LLM systems with RAG tailored for the military industry represents a promising research direction 
to improve operational effectiveness and responsiveness of defense systems.

## 1. Introduction



This study draws its foundations in the advancement of Artificial 
Intelligence for IT Operations (AIOps), a concept first introduced by 
Gartner in 2018 (Prasad & Rich, 2019). AIOps platforms leverage 
Machine Learning (ML) and deep learning algorithms to process and 
analyze vast volumes of operational data from multiple sources, automatically detecting and responding to system issues in real-time 
(Prasad & Rich, 2019). The adoption of these platforms is driven by 
the increasing complexity and scale of modern IT environments, which 
require advanced analytical capabilities beyond traditional methods to 
ensure service availability, optimize operational efficiency, and minimize downtime  (Prasad & Rich, 2019). Recent investments by leading 
industry vendors such as IBM,1 BigPanda,2 ServiceNow,3 Splunk,4 
Dynatrace,5 and Datadog6 underscore the importance and growing

∗Corresponding author.

E-mail addresses: m.delacruzcabello@student.utwente.nl (M. De la Cruz Cabello), t.princesales@utwente.nl (T.P. Sales), m.r.machado@utwente.nl 
(M.R. Machado).

1 IBM (International Business Machines Corporation) is a multinational technology company specializing in AI, cloud computing, and enterprise IT solutions. 
More information: https://www.ibm.com

2 BigPanda provides AI-driven IT operations and incident automation solutions. More information: https://www.bigpanda.io
3 ServiceNow offers AI-powered IT service management and workflow automation solutions. More information: https://www.servicenow.com
4 Splunk provides data analytics and AI-powered monitoring solutions for IT and security operations. More information: https://www.splunk.com
5 Dynatrace specializes in AI-driven observability and performance monitoring. More information: https://www.dynatrace.com
6 Datadog offers cloud monitoring and security analytics powered by AI. More information: https://www.datadoghq.com

recognition of AIOps. Within this context, the emergence of Large 
Language Models (LLMs) has introduced novel opportunities to integrate AI-driven automation into production processes by enabling more 
efficient processing of vast amounts of unstructured data  (Vitui & Chen, 
2025).
This research primarily focuses on the use of LLMs in IT operations, 
assessing their efficacy in enhancing anomaly detection, which is one of 
the core tasks within AIOps. By anomaly, we define it as any abnormal 
log message within the internal logic of a system. Through a comprehensive analysis of current research, methods, and challenges, this 
Systematic Literature Review (SLR) aims to provide valuable insights 
into the evolving landscape of AIOps.

The evolution of AIOps marks a transformative shift in the management of complex IT systems. AIOps leverages advanced AI techniques 
to transform raw operational data (e.g., logs, metrics, incident reports)

https://doi.org/10.1016/j.iswa.2025.200608
Received 13 July 2025; Received in revised form 16 October 2025; Accepted 9 November 2025

Intelligent Systems with Applications 28 (2025) 200608

Available online 19 November 2025 
2667-3053/© 2025 The Authors. Published by Elsevier Ltd. This is an open access article under the CC BY license ( http://creativecommons.org/licenses/by/4.0/ ).

---

M. De la Cruz Cabello et al.

into actionable insights that allow systems to detect, find root causes, 
and remediate anomalies proactively (Zhang, Jia et al., 2024). This approach improves the availability and reliability of services and reduces 
the need for manual intervention from IT professionals. In the end, this 
drives down operational costs and improves overall system efficiency 
(Notaro et al., 2021; Poenaru-Olaru et al., 2024).

The core tasks within AIOps revolve around data preprocessing 
(e.g., log parsing, metrics imputation, input summarization), failure 
perception (e.g., anomaly detection, failure prediction), root cause 
analysis (e.g., failure localization, failure category classification, root 
cause report generation), and automated remediation (e.g., assisted 
questioning, mitigation solution generation, command recommendations, script generation, automatic execution) (Zhang, Jia et al., 2024). 
Data preprocessing involves structuring operational data to enhance its 
usability for AI-driven analysis, particularly through log parsing and 
data filtering techniques (Zhang, Jia et al., 2024). Anomaly detection 
aims to identify abnormal patterns that indicate potential issues or 
failures (Zhang, Jia et al., 2024). Root cause analysis serves as a critical 
component in diagnosing failures, pinpointing their origins, and suggesting corrective actions (Zhang, Jia et al., 2024). Automated remediation, which represents the most advanced stage of AIOps, employs 
AI-driven decision-making to execute predefined mitigation strategies, 
reducing the need for manual intervention (Zhang, Jia et al., 2024).

The methodologies employed in AIOps are diverse, encompassing 
a range of AI and data-driven techniques. For anomaly detection, 
traditional ML, such as tree-based, clustering and PCA, RNNs, and 
GANs have long been used, typically relying on either supervised or 
unsupervised learning (He et al., 2017; Notaro et al., 2021; Vitui & 
Chen, 2025; Zhang, Jia et al., 2024). More recent advancements have 
integrated Natural Language Processing (NLP) to analyze log files and 
incident reports. Transformer-based architecture such as BERT7 and 
GPT8 have been leveraged for processing unstructured log data, improving anomaly detection significantly (Guan et al., 2024; Guo et al., 
2024, 2021; Hadadi et al., 2024). A particularly innovative technique in 
AIOps has been the integration of LLMs into IT operations management. 
Unlike traditional models that require extensive feature engineering 
and retraining, LLMs have robust reasoning capabilities to interpret and 
extract meaningful insights from natural language data (Vitui & Chen, 
2025; Zhang, Jia et al., 2024). LLMs have shown strong capabilities 
in interpreting unstructured data, making them highly effective for 
log analysis and system diagnosis (Vitui & Chen, 2025). In addition, 
LLMs have been trained on vast amounts of cross-platform data, which 
gives them a strong degree of generality (Zhang, Jia et al., 2024). 
Nonetheless, LLMs are still too general to be adaptive to multi-tasks, 
and companies exhibit significant limitations in developing these LLMs 
primarily due to data confidentiality (Chen et al., 2024). This is why 
the adoption of Retrieval-Augmented Generation (RAG), fine-tuning 
and prompt engineering techniques has increased recently (Chen et al., 
2024; Zhang, Jia et al., 2024).
The integration of LLMs has also reached military and defense 
applications, where AIOps play a crucial role in ensuring cybersecurity, 
operational resilience, and decision-making  (Loevenich et al., 2024). 
For instance, research shows that combining LLMs with reinforcement 
learning and rule-based systems enables autonomous cyber defense 
agents to analyze security breaches in real-time (Loevenich et al.,

7 BERT (Bidirectional Encoder Representations from Transformers) is a pretrained language model developed by Google that uses deep bidirectional 
transformers to understand the context of words in a sentence. It serves as 
the foundation for many state-of-the-art NLP tasks. More information: https:
//arxiv.org/pdf/1810.04805

## 8 GPT (Generative Pre-trained Transformer) is a series of autoregressive

language models developed by OpenAI that generate human-like text by 
predicting the next token in a sequence. The models are pre-trained on large 
text corpora and fine-tuned for various natural language processing tasks. More 
information: https://openai.com/research/gpt

2024). Moreover, LLMs contribute to intelligence gathering and battlefield awareness as they are able to synthesize vast amounts of data from 
satellite imagery, communications, or sensor inputs, and this improves 
strategic planning (Cui & Gao, 2024).

The increasing digitization of military operations has resulted in 
the generation of large volumes of operational logs and telemetry data 
from systems such as radar, drones, communication equipment, and 
command-and-control platforms. As defense infrastructure becomes 
more reliant on complex IT ecosystems, the ability to detect anomalies 
– whether technical faults or signs of cyber intrusion – is becoming 
mission-critical. Traditional rule-based systems lack the adaptability 
and speed to manage these dynamic threats, necessitating the application of more intelligent, context-aware techniques such as LLMs 
combined with retrieval-based architectures.

The decision to emphasize the military domain in this study stems 
from the increasing strategic importance of AI-driven infrastructure 
within defense operations, where the stakes for anomaly detection 
are significantly higher than in conventional IT environments. In military contexts, log anomalies can indicate not only system failures 
but also potential cyberattacks, intelligence disruptions, or operational 
sabotage—events that can compromise mission-critical operations and 
national security. Unlike general IT systems, where anomalies may 
affect service delivery or performance, in military operations such disruptions can have immediate and irreversible consequences. Therefore, 
AIOps techniques and LLM-based anomaly detection solutions play 
a pivotal role in maintaining resilience, situational awareness, and 
proactive threat mitigation. That said, the methodological approach 
used in this review – particularly the inclusion criteria, paper selection, 
and analysis – was designed with a focus on military applications but is 
not limited to them. The identified patterns, frameworks, and insights 
are applicable across a wide range of high-stakes industries, such as 
finance, healthcare, and critical infrastructure, where reliability and 
anomaly detection are equally essential.

This study explores the use of LLMs for log anomaly detection and 
investigates the usefulness of the implementation of RAG to improve 
the specialization of LLMs. Thus, this literature aims to answer the 
following knowledge questions:

## 1. What are the main challenges and benefits of implementing

AIOps in IT systems?
2. What AIOps techniques are being used for automating anomaly 
detection in IT systems?
3. What are the main evaluation metrics used for log anomaly 
detection using LLMs?
4. How does RAG improve the knowledge and reasoning capabilities of LLMs?

The insights gained from this systematic literature review explain 
the current state of research and gaps in the literature to bring future 
advancements in the field of AIOps. To the best of our knowledge, 
this is the first study that systematically investigates the intersection of 
AIOps, LLM-based log anomaly detection, and RAG integration. While 
prior works have primarily focused on traditional anomaly detection 
methods, such as statistical techniques, rule-based systems, or classical 
machine learning models, these approaches often suffer from scalability 
issues, limited contextual awareness, and reduced adaptability to new 
types of anomalies (Gao et al., 2023; He et al., 2017; Wang et al., 2024; 
Xu & Ding, 2024).

In contrast, our review highlights how LLMs, especially when augmented with RAG, offer a more robust and dynamic foundation for 
handling unstructured and semantically complex log data. This work 
contributes novel insights into how RAG can compensate for LLM 
limitations, such as hallucinations or domain drift, by incorporating 
external, up-to-date, and task-specific knowledge at inference time. By 
bridging these research areas, our study offers a comprehensive perspective that advances the understanding of next-generation anomaly 
detection frameworks within the broader AIOps ecosystem.

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Table 1
Article selection criteria.
 Criteria
Decision 
 Pre-defined keywords list
Inclusion 
 Document type: conference paper, article
Inclusion 
 Subject area: computer science, engineering
Inclusion 
 Article written in English
Inclusion 
 Article published before 2021a
Exclusion 
 Unavailability of free article version
Exclusion

a For the initial inclusion/exclusion criteria in the Scopus database, only articles 
published from 2021 onwards were included. However, through the snowball process, 
additional articles published before 2021 were collected.

This paper is structured in the following way: Section 2 discusses 
the methodology developed to carry out this review, explaining the 
steps to extract relevant articles. Section 3 deconstructs the research 
landscape to identify trends, academic contributions, and emerging 
themes in AIOps research. Section 4.1 focuses on the current techniques, challenges, and benefits of AIOps. Section 4.2 addresses the use 
of LLMs in anomaly detection, and Section 4.3 explains what RAG is 
and how it can be implemented to improve reasoning capabilities in 
LLMs. Section 4.4 describes some recommendations for future work in 
the field of log anomaly detection and proposes a framework for log 
anomaly detection using LLMs and RAG. Finally, Section 5 concludes 
the paper.

## 2. Methodology



In this section, we detail the methodology used for conducting the 
systematic literature review. We describe the paper selection process, 
including inclusion and exclusion criteria, as well as the search queries 
and academic databases employed to ensure comprehensive coverage 
of the relevant literature.

The methodology employed in this study follows a structured approach to conducting a literature review on AIOps, the use of LLMs for 
anomaly detection, and the implementation of RAG to ensure unbiased 
outcomes (Amato et al., 2024; Firmansyah et al., 2024).

First, we established a set of knowledge questions that the literature 
review aims to answer (see Section 1). These questions served as the 
foundation of the research to ensure that the study remained focused 
on the targeted areas. Following this, we conducted a comprehensive 
exploration and analysis of the existing literature to gain a broader perspective on the field of AIOps. The goal was to map out the landscape of 
current research, identifying common methodologies, data-driven techniques, and evaluation methods to highlight emerging trends. During 
this phase, we defined inclusion and exclusion criteria (see Table 1) 
to filter out studies that did not meet certain standards. We selected 
studies based on parameters such as publication year, document type, 
language, pre-defined keywords list, and unavailability of a free article version. Next, we assessed the quality of the collected papers by 
reading their titles and abstracts, evaluating their credibility based on 
the rigor of the research rather than speculative ideas. Subsequently, 
we extracted data and compiled a table (see Appendix) with relevant 
information about each paper such as topic, professional setting, main 
purpose, data-driven techniques used, and evaluation metrics. Lastly, 
we summarized and discussed the most important outcomes of each 
paper in this review. Throughout the entire process, we ensured rigor, 
reliability, and reproducibility of the methodology, following other 
SLRs presented in the literature (Amato et al., 2024; Firmansyah et al., 
2024; Notaro et al., 2021).

Fig. 1. Selection process of articles.

Scopus9 was selected as the primary database, and arXiv10 repository was used when some references of the papers were relevant 
to add in the literature review.11 The advanced search feature was 
used to create custom queries to focus on the applications of LLMs 
with a base knowledge in log anomaly detection. Important keywords 
included ‘‘AIOps’’, ‘‘anomaly detection’’, ‘‘large language models’’, and 
‘‘retrieval-augmented generation’’, in combination with ‘‘AND’’ and 
‘‘OR’’ operators. The final search queries used were:

• (‘‘artificial intelligence for IT operations’’ OR ‘‘AIOps’’) OR (‘‘incident detection’’ OR ‘‘anomaly detection’’) AND (‘‘large language 
models’’ OR ‘‘LLMs’’) AND (‘‘military’’ OR ‘‘transport’’ OR ‘‘ship’’)
• (‘‘artificial intelligence for IT operations’’ OR ‘‘AIOps’’) AND (‘‘incident detection’’ OR ‘‘anomaly detection’’)
• (‘‘LLMs’’ OR ‘‘large language models’’) AND (‘‘RAG’’ OR ‘‘rag’’ OR 
‘‘retrieval-augmented generation’’) AND (‘‘anomaly detection’’ OR 
‘‘incident detection’’)

Fig. 1 shows a total of 33 articles gathered through the five-step 
strategy. We retrieved 23 articles by the search queries in Scopus. The 
manual inclusion followed a snowballing process (Wohlin, 2014) from 
references of the articles gathered.

9 Scopus is a comprehensive bibliographic database that indexes peerreviewed literature across multiple disciplines, including AI, technology, and 
computer science. More information: https://www.scopus.com

10 arXiv is an open-access repository of research articles, particularly in 
computer science, physics, and AI, providing preprints before formal peer 
review. More information: https://arxiv.org

## 11 While Scopus and arXiv provide extensive coverage of peer-reviewed

and preprint literature, they are not entirely exhaustive. Their scope may 
omit relevant studies from smaller or non-indexed venues, and the diversity 
and completeness of indexed content can vary across subfields, potentially 
introducing selection bias.

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Fig. 2. Selection process: Inclusion and exclusion of papers.

Table 1 and Fig. 2 summarize the inclusion and exclusion criteria 
used in this study to ensure a rigorous and systematic selection of 
relevant literature. We included only publications that matched a predefined list of keywords, were classified as conference papers or journal 
articles, and belonged to the subject areas of computer science and 
engineering. To maintain consistency and interpretability, only articles 
written in English were considered. Furthermore, for the initial search 
in the Scopus database, we limited the selection to articles published 
from 2021 onwards to capture the most recent developments in the 
field; however, earlier publications were included through a backward 
and forward snowballing process when deemed relevant. Finally, we 
excluded papers for which no freely accessible version was available, 
as this would limit reproducibility and independent verification of the 
review process.

## 3. Deconstructing the research landscape



This section presents a structured analysis of the research landscape 
surrounding the applications of AIOps techniques for anomaly detection 
in three parts. First, we provide an overview of the distribution of 
articles over recent years. Second, we categorize the reviewed articles 
according to their research domain. Understanding this distribution 
helps determine which platforms are actively exploring AIOps and 
where new approaches are emerging. Last, we delve into the recurring 
keywords that define the current state of AIOps research within the 
collected articles. It is also important to highlight that the Appendix

shows an overview of each article, ensuring transparency and clarity 
in the selection and evaluation of relevant articles.

3.1. Temporal distribution of articles

We start by analyzing the chronological timeline of articles in 
AIOps, RAG, AI in military, and anomaly detection. By tracking publication trends from 2021 to 2025, this analysis highlights periods of rapid 
growth in certain fields to better understand how the focus on AIOps 
research has adapted to new trends and technological advancements. 
Fig. 3 illustrates the increase in the number of articles published in 
recent years, particularly in the fields of RAG and anomaly detection. 
The rise in RAG-related articles reflects a growing interest in leveraging 
LLMs with external knowledge to mitigate hallucinations and improve 
performance in domain-specific tasks. AIOps articles have maintained 
a stable publication rate over the past years, which suggests that it 
still remains a significant area of interest in the software industry. In 
addition, the implementation of AI has been increasing in the defense 
and military industries in the past year, despite challenges related to 
classified information, indicating expanding roles for AI in operational 
domains such as image recognition and decision-making.

3.2. Journal distribution of articles

The analysis focused on a single table (see Table 2), which included 
the topic, author/s, journal of publication, number of citations, and 
Field-Weighted Citation Impact (FWCI). Understanding this distribution 
helped identify the platforms that actively explored AIOps and revealed 
where new approaches emerged. This information was important for 
assessing the quality and academic impact of each article, as it provided 
insight into the credibility and reach of the publications.

Table 2 summarizes the journal distribution across all selected 
articles, covering topics such as AIOps, anomaly detection, RAG, and 
AI applications in the military. The works by Notaro et al. (2021) and 
Dang et al. (2019) stand out with the highest number of citations within 
AIOps, suggesting their strong influence in the field. Similarly, He et al. 
(2017), Guo et al. (2021), and Zhu et al. (2018) received notable 
citations in the anomaly detection category, while Fan et al. (2024) was 
the most cited work in RAG-related research. The analysis also revealed 
that all articles were published in different journals, highlighting the 
diverse range of sources contributing to these topics.

Since the AIOps, and RAG with LLMs domains are relatively new 
and emerging topics, it is understandable that many studies are available as preprints in arXiv, lacking peer-review (Gao et al., 2023; Guan 
et al., 2024; Hadadi et al., 2024; Prasad & Rich, 2019; Su et al., 2024; 
Vitui & Chen, 2025; Xu & Ding, 2024; Zhang, Jiang et al., 2024). 
Furthermore, we can also notice from Table 2 that most of these articles 
are from the last two years, which explains why they do not yet have 
many citations, as they typically accumulate over time as research gains 
visibility within the community.

3.3. Keywords distribution across articles

Keywords analysis provides a clear vision of the main theme and the 
predominant topic and allows for a better understanding of the research 
landscape, facilitating future studies and supporting the identification 
of gaps within the literature.

Figs. 4 and 5 illustrate the keyword network graphs built for this 
study. These graphs show relationships between key terms extracted 
from the articles, providing insights into predominant themes and their 
connections over time. We focused on building keyword graphs across 
all articles, instead of concentrating on individual topics, to get an 
overall picture of the research landscape. We used VOSviewer12 to

## 12 VOSviewer is a software tool for constructing and visualizing bibliometric

networks, commonly used for analyzing citation networks and co-authorship 
relations. More information: https://www.vosviewer.com

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Fig. 3. Yearly distribution of collected papers.

Table 2
Journal distribution of articles.
 Topic
Study
Journal/Conference
# Citations
FWCI 
 AIOps
Zhang, Jia et al. (2024)
Preprint on arXiv
–
–
 
 AIOps
Poenaru-Olaru et al. (2024)
2024 IEEE/ACM CAIN Conference
1
–
 
 AIOps
Notaro et al. (2021)
ACM Trans. on Intelligent Systems
49
3.30 
 AIOps
Diaz-De-Arcaya et al. (2023)
ACM Computing Surveys
18
10.18 
 AIOps
Mansour et al. (2024)
Int. J. of Engineering Trends
–
–
 
 AIOps
Prasad and Rich (2019)
Gartner
21
–
 
 AIOps
Duan et al. (2024)
Electronics (Switzerland)
–
–
 
 AIOps
Vitui and Chen (2025)
Preprint on arXiv
–
–
 
 AIOps
Dang et al. (2019)
2019 IEEE/ACM ICSE-Companion
160
17.03 
 Anomaly Detection
Wang et al. (2024)
IEEE Int. Conf. on Software Eng.
–
–
 
 Anomaly Detection
Su et al. (2024)
Preprint on arXiv
–
–
 
 Anomaly Detection
No et al. (2024)
Eng. Applications of AI
2
1.01 
 Anomaly Detection
Guo et al. (2021)
Proc. Int. Joint Conf. on Neural Networks
171
16.54 
 Anomaly Detection
Guan et al. (2024)
Preprint on arXiv
–
–
 
 Anomaly Detection
He et al. (2017)
IEEE ICWS 2017
586
19.24 
 Anomaly Detection
Zhu et al. (2018)
IEEE ICSE-SEIP 2019
382
44.98 
 Anomaly Detection
Guo et al. (2023)
12th Int. Conf. on Learning Representations
4
7.61 
 Anomaly Detection
Mehrabi et al. (2024)
IEEE ICSME 2024
–
–
 
 Anomaly Detection
Guo et al. (2024)
AAAI Conf. on AI
9
20.04 
 Anomaly Detection
Hadadi et al. (2024)
Preprint on arXiv
–
–
 
 Anomaly Detection
Xu and Ding (2024)
Preprint on arXiv
–
–
 
 Anomaly Detection
Liu et al. (2023)
IEEE Int. Conf. on Program Comprehension
3
5.74 
 Anomaly Detection
Almodovar et al. (2024)
IEEE Trans. Netw. Serv. Manag.
15
7.33 
 RAG
Vizniuk et al. (2024)
J. of AI and Soft Comp. Research
–
–
 
 RAG
Arslan et al. (2024)
Procedia Computer Science
–
–
 
 RAG
Fan et al. (2024)
ACM SIGKDD Int. Conf. on KDD
27
63.57 
 RAG
Jeon et al. (2025)
J. of Manufacturing Systems
–
–
 
 RAG
Chen et al. (2024)
Proceedings of Science
–
–
 
 RAG
Gao et al. (2023)
Preprint on arXiv
–
–
 
 RAG
Zhang, Jiang et al. (2024)
EMNLP 2024 - Industry Track
–
–
 
 RAG
Ovadia et al. (2023)
EMNLP 2024 - Main Conference
–
–
 
 AI in Military
Cui and Gao (2024)
Lecture Notes in Electrical Eng.
–
–
 
 AI in Military
Loevenich et al. (2024)
IEEE MILCOM
–
–

create the graphs. First, we constructed a network graph to visualize the 
relationships and connections between keywords, organizing them into 
clusters. Then, we overlaid an additional graph on top of the network 
graph to incorporate publication years to identify how research interests have evolved over time and how they can be connected with each

other. The analysis unveiled ‘‘large language model’’, ‘‘anomaly detection’’, ‘‘AIOps’’, and ‘‘retrieval-augmented generation’’ as the recurring 
themes within the literature, followed by other interesting keywords 
such as ‘‘It operations’’, ‘‘log analysis’’, ‘‘fine-tuning’’, and ‘‘prompt 
engineering’’.

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Fig. 4. Keyword network across all articles.

Fig. 5. Keyword overlay timeline.

Keyword networks revealed that research in recent years intersects 
around LLMs and anomaly detection within the AIOps domain, suggesting a shift from traditional models toward advanced NLP techniques in 
IT operations.

## 4. Qualitative summary and analysis of the literature



This section synthesizes the insights obtained from the reviewed 
studies on AI-driven operations (AIOps) and their role in log anomaly 
detection. We first discuss core AIOps techniques, associated challenges, and emerging trends. Next, we examine the application of 
Large Language Models (LLMs) in log anomaly detection, followed by a 
review of Retrieval-Augmented Generation (RAG) as a complementary 
approach for context-aware anomaly detection. Finally, we propose a 
theoretical framework and highlight promising directions for future 
research and applications.

4.1. AIOps: Techniques, challenges, benefits, and future trends

This section provides an overview of AIOps, focusing on the key 
techniques used in practice, the challenges faced during implementation, and the associated benefits. We also highlight emerging trends and 
future directions shaping the evolution of AIOps in modern IT systems.

AIOps represents an innovative approach to managing and monitoring new IT environments. By leveraging machine learning, big data 
analytics, and visualization techniques, AIOps platforms are designed to 
enhance efficiency and reliability in IT systems, providing operational 
insights that were not feasible with traditional methods (Prasad & 
Rich, 2019). The cycle follows a continuous three-stage process that 
observes data, engages with it to find patterns and root causes, and 
acts to resolve issues (Prasad & Rich, 2019). These capabilities not 
only improve customer satisfaction but also allow companies to shift towards more predictive approaches, instead of traditional management 
methods, reducing operational costs and downtime of IT services (Dang 
et al., 2019).

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Fig. 6. AIOps operational cycle (Prasad & Rich, 2019).

At its core, AIOps integrates large amounts of operational data, 
from logs, metrics, traces, alerts, incident reports, and Q&A, to facilitate data preprocessing, failure perception, root cause analysis, failure 
prediction, and auto-remediation. These tasks are sequentially related, 
meaning that failure perception is based on preprocessed data, and once 
the anomaly has been identified in the system, a root cause analysis 
is performed to trace the anomaly and, in the end, appropriate auto 
remediation methods are implemented to mitigate the issue from the 
system (Zhang, Jia et al., 2024)), completing the operational cycle (see 
Fig. 6).

This systematic literature review mainly focuses on anomaly detection within AIOps because it precedes subsequent tasks. Emphasizing 
the initial techniques within AIOps allows for a more structured exploration of its processes. The preprocessing phase involves tasks such as 
log parsing for extracting meaningful information from logs, metrics 
imputation to estimate incomplete or missing data, and input summarization to highlight the most important information in the prompt 
(Zhang, Jia et al., 2024). Once the data is preprocessed, the datasets are 
ready to enable an effective failure perception, which involves predicting failures or detecting anomalies from historical trends (Zhang, Jia 
et al., 2024). Anomaly detection, as one of the core tasks in AIOps, is 
lately using advanced machine learning and deep learning techniques. 
Previous work has focused on unsupervised or semi-supervised models, but the best-performing and most popular techniques to detect 
anomalies in univariate data belong to signal reconstruction models 
(Poenaru-Olaru et al., 2024). Statistical methods such as Spectral Residuals (SR), Fast Fourier Transform (FFT), and Prediction Confidence 
Interval (PCI) identify strange behaviors in systems by encoding the 
time series into a latent space (Poenaru-Olaru et al., 2024). These techniques have low computational costs, but lose information during the 
encoding process (Poenaru-Olaru et al., 2024). In addition, to preserve 
more information, deep learning methods such as autoencoders, LSTMs, 
DONUT, and CNNs have proven strong performance when detecting 
anomalies (Notaro et al., 2021; Poenaru-Olaru et al., 2024).

Despite these advancements, real-world implementation of AIOps 
still faces significant challenges. Poenaru-Olaru et al. (2024) introduce 
the phenomenon of concept drift. Concept drift occurs when the properties of the incoming data change over time, meaning that the patterns 
the model originally learned no longer fully represent the current 
reality. For example, a system log model trained on older software 
versions may fail to detect anomalies once the software is updated and 
generates new types of logs. If models are not periodically retrained, 
this drift causes their performance to degrade. Other major challenges 
of AIOps include the complexity of getting high-quality and quantity 
labeled datasets, a difficult mindset shift towards new technologies, a 
gap in innovation that could guide people in different disciplines to 
build AIOps solutions, and limitations in model adaptability to specific 
tasks and across different software systems, as integration of AIOps

with existing systems may be challenging (Dang et al., 2019; Zhang, 
Jia et al., 2024).

Conversely, adopting AIOps provides numerous substantial benefits. 
These include improved service quality and reliability, increased customer satisfaction, enhanced productivity of engineering teams, and 
significant reductions in operational costs due to proactive issue detection and management (Dang et al., 2019). Additionally, AIOps fosters 
improved collaboration among traditionally siloed IT teams, creating 
more streamlined operations and faster incident resolution (Mansour 
et al., 2024). Moreover, AIOps contributes to better scalability and 
agility in managing IT infrastructures by automating routine processes 
and minimizing complexities associated with managing large-scale systems (Notaro et al., 2021). Real-time data analytics and operational 
insights further allow rapid detection, diagnosis, and resolution of performance bottlenecks, enhancing overall operational efficiency (Prasad 
& Rich, 2019).

A recent study from Duan et al. (2024) shows that meta-learning has 
been introduced to further enhance the adaptability and effectiveness 
of anomaly detection. Meta-learning involves using prior knowledge to 
enable AI to autonomously learn new tasks, with the goal of making a 
model generalizable by ‘learning how to learn’. Typically, there are few 
examples of specific types of anomalies, making traditional learning 
methods less effective (Duan et al., 2024). To address this issue, Duan 
et al. (2024) apply the Model-Agnostic-Meta-Learning (MAML) framework to facilitate the model’s ability to quickly update its parameters 
when encountering new anomalies. The experimental results demonstrate that the MAML-based approach achieves better performance than 
traditional methods, validating its effectiveness for enhancing model 
adaptability and efficiency in few-shot AIOps scenarios, addressing the 
challenge related to limited labeled data and the necessity of frequent 
model updates.

Additionally, AIOps methodologies have found implications in other 
IT scenarios, intersecting notably with DevOps, DataOps, GitOps, and 
MLOps methodologies as explained in Mansour et al. (2024). These integrations promote automation, agility, and collaboration, helping enterprises reduce complexity and support continuous innovation (DiazDe-Arcaya et al., 2023).

The integration of LLMs represents a particularly transformative advancement in the AIOps domain, specifically addressing tasks involving 
complex and unstructured data such as logs and incident reports  (Vitui 
& Chen, 2025). Unlike traditional anomaly detection methods, which 
often require extensive manual feature engineering and retraining, 
LLMs have been trained on large amounts of cross-platform data and 
inherently possess robust capabilities for interpreting and extracting 
meaningful insights from natural language data (Vitui & Chen, 2025; 
Zhang, Jia et al., 2024). Their sophisticated NLP techniques allow them 
to efficiently analyze and understand context, semantics, and patterns 
within textual operational data, significantly streamlining anomaly 
detection and root cause analysis tasks (Vitui & Chen, 2025; Zhang, Jia

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Fig. 7. Example log entry from var/log/messages.

et al., 2024). However, despite these advantages, LLMs still face notable 
limitations, including computational efficiency, constraints on crosstask adaptability and the need for careful model tuning and adaptation 
to specific operational contexts (Zhang, Jia et al., 2024). Nonetheless, 
their advanced NLP capabilities continue to offer substantial potential 
for enhancing the accuracy, interpretability, and adaptability of AIOps 
systems, making them a promising area for ongoing research and development (Vitui & Chen, 2025; Zhang, Jia et al., 2024). The importance 
of deploying these techniques in military contexts cannot be overstated. 
Military IT systems increasingly rely on autonomous platforms, secure 
communication infrastructures, and integrated cyber–physical operations that produce complex, mission-critical logs. These systems require 
not only accurate but also explainable and rapid anomaly detection 
methods to mitigate cyber threats, detect system failures, and maintain 
operational continuity under constrained conditions. Thus, the military 
sector presents both a high-need and high-impact setting for applying 
AIOps and LLM-based solutions.

4.2. LLMs in log anomaly detection

This section examines the application of Large Language Models 
(LLMs) in log anomaly detection. We discuss their capabilities, current 
use cases, and limitations, as well as how they compare to traditional 
anomaly detection methods.

Log anomaly detection refers to the process of automatically identifying unexpected patterns within log data generated by software 
systems (Guo et al., 2024). The problem is defined as a binary classification task, and the models are supposed to determine whether an 
input log is normal or abnormal (Guo et al., 2024). Logs are semistructured or unstructured text generated by logging statements in 
source code (Hadadi et al., 2024; Mehrabi et al., 2024). They are used 
to monitor system performance and diagnose errors. An example log 
from /var/log/messages file on a Linux13 server is included in Fig. 7.

As IT systems grow in complexity, generating large amounts of 
data that record the internal logic of systems and events, log anomaly 
detection has grown in importance. Effective anomaly detection within 
these logs is crucial for system reliability, security, and operational 
efficiency (Guan et al., 2024; Guo et al., 2024, 2023; Hadadi et al., 
2024). The techniques used for log anomaly detection have evolved 
substantially, incorporating traditional ML, deep learning, and, most 
recently, leveraging LLMs to address the challenges of log data.

Logs typically contain diverse event types, unstructured messages 
that often contain noise (e.g., irrelevant information, typos, ambiguous 
expressions), which complicates the preprocessing for effective analysis 
(Su et al., 2024). Class imbalance is another significant challenge, as 
anomalous events occur less often than normal events. This imbalance 
can bias model training, where strategies such as minority class oversampling may be needed to ensure balanced learning (Guan et al., 
2024). Furthermore, the availability of labeled datasets for supervised 
ML is limited in real-world scenarios, as anomalies are inherently rare 
and labeling is resource-intensive (Su et al., 2024). To address this 
challenge, log parsing has been proposed as a prerequisite for many 
log analytics tasks (Mehrabi et al., 2024). However, the challenge of 
log parsing is to distinguish automatically between static and dynamic

## 13 More

information: 
https://github.com/logpai/loghub/blob/master/
Linux/README.md

tokens (Mehrabi et al., 2024). A possible solution could be the use of 
regular expressions (Mehrabi et al., 2024). Still, the problem is that 
log files may contain thousands of events, and any modifications to 
the system would require constant changes to the regular expressions 
(Mehrabi et al., 2024). Additionally, it is common for companies to 
have multiple types of log files, which complicates the development of 
regular expressions to parse the data (Mehrabi et al., 2024). Another 
challenge is the requirement for models to process logs in real-time. 
Logs are produced continuously, demanding anomaly detection models 
to balance accuracy with computational efficiency (No et al., 2024). 
Moreover, these logs frequently evolve as software gets updated. This 
needs models that can adapt quickly and generalize to new log patterns 
without extensive retraining (Hadadi et al., 2024).

Traditional methods for log anomaly detection often rely on statistical or rule-based approaches, such as Support Vector Machines (SVM), 
Isolation Forests (IF), Principal Component Analysis (PCA), SR, FFT, 
and PCI (Hadadi et al., 2024; Poenaru-Olaru et al., 2024). These methods require manual feature engineering, so they limit the scalability 
and generalization for new logs (Hadadi et al., 2024; Poenaru-Olaru 
et al., 2024). Additionally, there are deep-learning methods, including 
LSTMs and transformers, that automate feature extraction to capture 
the sequential nature of the log (Hadadi et al., 2024; Poenaru-Olaru 
et al., 2024). For example, LogBERT (Guo et al., 2021) is a selfsupervised framework for log anomaly detection based on transformer 
architecture (BERT). The objective of LogBERT is to predict masked log 
keys in log sequences, where they are randomly masked and predicted, 
and hypersphere minimization to cluster the distribution of normal log 
sequences in the embedding space. The model is trained on normal logs 
and flags sequences with many incorrectly predicted log keys as anomalies. They use Drain (He et al., 2017) for parsing the log messages. Drain 
structures messages into a tree-based representation to facilitate online 
parsing, which is critical for real-time anomaly detection (He et al., 
2017). Also, the authors do evaluations on three datasets (Hadoop 
Distributed File System (HDFS), BlueGene/L (BGL), and Thunderbird), 
and demonstrate that LogBERT outperforms other traditional methods 
such as PCA, IF, OCSVM, DeepLog,14 and LogAnomaly15 with higher 
F1-scores on the three datasets. Other evaluation metrics they use are 
precision and recall. Since automated log parsing is an essential part of 
this traditional pipeline to detect anomalies, Zhu et al. (2018) show a 
comprehensive evaluation of different automated parsing tools such as 
Drain (He et al., 2017), Spell, LogCluster, or MoLFI,16 among others, 
across 16 log datasets from different domains, including distributed 
systems, operating systems, supercomputers, and server applications. 
They define log parsing as a step to convert raw logs into a structured

## 14 DeepLog is a deep learning-based model for anomaly detection in system

logs, which uses LSTM networks to learn log sequence patterns under normal 
conditions and identify anomalies as deviations from those patterns. More 
information: https://github.com/Thijsvanede/DeepLog

15 LogAnomaly is a deep learning-based framework for log anomaly detection that combines semantic and sequential modeling by using template 
embeddings and an LSTM network to identify abnormal log patterns. More 
information: https://www.ijcai.org/proceedings/2019/0658.pdf

## 16 MoLFI (Multi-objective Log pattern Finder) is a search-based algorithm

designed to discover log patterns from unstructured log messages using 
multi-objective optimization. It aims to balance quality and coverage. More 
information: https://github.com/SNTSVV/MoLFI

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

template. They base their findings on accuracy, robustness, and computational efficiency when determining anomalies within the log files, so 
future researchers can select an optimal parser based on their specific 
use case.

New strategies have emerged with the advancements of LLMs in 
anomaly detection through improved semantic understanding. For example, LogLLM  (Guan et al., 2024) integrates BERT for extracting semantic vectors from log messages, and LLaMa17 for classification of the 
log sequences. Additionally, Guan et al. (2024) introduce a projector 
for vector representation to achieve a cohesive semantic interpretation. 
Log messages are grouped into sequences based on session windows. 
Instead of relying on log parses such as Drain (He et al., 2017), the 
approach replaces specific objects in the log message with regular 
expressions. This technique is chosen for its simplicity and because 
existing parsers often struggle with out-of-vocabulary (OOV) words 
(Guan et al., 2024). Evaluation on four datasets (HDFS, BGL, Thunderbird, and Liberty) shows that on average LogLLM’s F1-scores are 
6.6% better than other existing methods such as DeepLog, LogAnomaly, 
PleLog, FastLogAD,18 RAPID (No et al., 2024), and LogBERT (Guo 
et al., 2021). Other evaluation metrics they use are precision and 
recall. Similarly, LogFormer (Guo et al., 2024) employs a new attention 
mechanism and adapter-based tuning strategy to maintain semantic 
information across multiple log domains, enabling effective transfer 
learning. First, the pre-trained model learns the commonalities among 
different anomalies through a supervised classification task. Then, the 
parameters of the attention encoder are used in the tuning stage, where 
they prove the knowledge obtained from pre-training. In the preprocessing stage, Guo et al. (2024) also use Drain (He et al., 2017) to do 
log parsing of the sliding windows and select 80% of the messages for 
training and the remaining 20% for testing. Another approach is OWL 
(Guo et al., 2023), which shows the advances of LLMs in log anomaly 
detection by training a model on Operations and Maintenance (O&M) 
data. The authors employ a Homogeneous Markov Context Extension 
(HMCE) method to extend the context processing capabilities of LLMs. 
OWL uses a tunning technique called Low-Rank Adaptation (LoRA), 
which involves fine-tuning a small set of parameters in the model to 
reduce computational costs while maintaining performance. Then, it 
is evaluated on multiple benchmarks, including datasets from system 
architecture, application logs, infrastructure, and information security, 
showing higher performance in terms of F1-score when compared 
to other baseline models such as GPT-4, Qwen,19 LLaMa, DeepLog, 
LogAnomaly, and LogRobust. (Xu & Ding, 2024) further provide a 
taxonomy for anomaly and OOD detection using LLMs and categorize 
their approaches into prompt-based and contrast-based methods. They 
describe prompt-based methods as creating constructed prompts that 
guide the LLM to directly output detection results using techniques 
such as role-play prompting, in-context learning, and CoT. Furthermore, they describe contrast-based methods as using multimodal LLMs 
to extract and compare embeddings for anomaly detection. Another 
novel method is LogFiT (Almodovar et al., 2024), which leverages 
a pre-trained BERT model fine-tuned on normal log data to detect 
anomalies. LogFiT eliminates the need for log parsing and instead

## 17 LLaMA (Large Language Model Meta AI) is a family of open-source

foundational language models developed by Meta, designed for efficient 
training and deployment in various natural language processing tasks. More 
information: https://ai.meta.com/llama/

## 18 FasLogAD is a lightweight and efficient anomaly detection framework for

log data that leverages statistical and semantic features to identify anomalies 
in real time, without relying on deep learning models. More information: 
https://arxiv.org/pdf/2404.08750

## 19 Qwen is a series of large language models developed by Alibaba Cloud,

designed for tasks such as text generation, reasoning, and code completion. The 
models are open-source and optimized for both general and domain-specific 
applications. More information: https://github.com/QwenLM

uses a masked sentence prediction for self-supervised tuning. The authors state that log parsers could make inaccurate parsing due to 
misinterpretation of the semantic meaning of the log analysis and not 
handle OOV words well so which is why they propose this strategy. 
LogFiT detects anomalies based on the top-k token prediction accuracy, 
making it highly adaptable to different logs. Evaluations on HDFS, 
BGL, and Thunderbird datasets demonstrate that LogFiT outperformed 
baseline methods such as DeepLog and LogBERT (Guo et al., 2021) in 
terms of F1-score, precision, and recall. Lastly, LogPrompt (Liu et al., 
2023) builds on these advancements by introducing a set of prompting 
strategies for interpretable online log analysis. These strategies include 
self-prompt, which leverages the intrinsic capabilities of the LLM to 
generate the output, chain-of-thought (CoT) prompt, which emphasizes 
a step-by-step reasoning process by guiding the LLM to address the 
task, and in-context prompt, which gives the LLM multiple examples to 
establish a contextual understanding, enhancing the interpretability of 
anomaly detection without requiring extensive in-domain training. The 
authors evaluate this model across multiple public datasets (HDFS, BGL, 
Linux,20 Android,21 Spirit) against other baseline models such as Drain 
(He et al., 2017), DeepLog, LogAnomaly, LogRobust, outperforming 
these models in terms of F1-scores, interpretability, and usability.

Another innovative methods that are growing nowadays are the 
ones that explicitly integrate external knowledge into the LLM for log 
anomaly detection. These examples are LogExpert (Wang et al., 2024) 
and RAPID (No et al., 2024). LogExpert leverages domain-specific 
knowledge from technical forums, such as Stack Overflow,22 dynamically retrieving relevant knowledge to generate outputs. Its methodology fine-tunes LLMs on structured logs combined with domain-specific 
text information. LogExpert achieves strong performance of public 
datasets including HDFS, BGL, and Thunderbird, employing lexical 
and human-evaluated metrics to ensure accuracy and interpretability 
(Wang et al., 2024). In addition, RAPID (No et al., 2024) introduces 
a training-free, retrieval-based log anomaly detection method that uses 
LLMs. How RAPID works is that it categorizes logs based on system context and contrasts test logs against similar normal logs. They evaluate 
their experiments on benchmark datasets including BGL, Thunderbird, 
and HDFS, achieving an overall performance of 0.97 in F1-score. This 
model includes token-level information, which is the granular semantic 
details of individual log message tokens, and it is used to identify small 
deviations to detect anomalies. This strategy demonstrates robust performance in real-time scenarios without the need for domain-specific 
training.

However, despite these innovations, the use of LLMs for log analysis 
also poses challenges. Logs often contain private information, so using 
a proprietary LLM would force companies to send their data to a 
third party, with the risk of violating privacy regulations (Mehrabi 
et al., 2024). From a development standpoint, integrating third-party 
LLMs into existing log analysis workflows is also challenging (Mehrabi 
et al., 2024). Additionally, the substantial size of log files leads to high 
processing costs when using LLM-based approaches (Mehrabi et al., 
2024).
Overall, log anomaly detection has evolved over the past years, 
from traditional, manual feature engineering ML methods to more 
advanced techniques employing deep learning and LLMs. These new 
advancements address complex challenges such as data representation, 
class imbalance, label scarcity, stream processing, and generalization

## 20 The Linux dataset consists of logs from a production Linux-based system,

often used for anomaly detection and root cause analysis. Retrieved from 
Loghub: https://github.com/logpai/loghub

21 The Android dataset contains logs collected from an Android smartphone system, primarily used for studying mobile system reliability and crash 
analysis. Retrieved from Loghub: https://github.com/logpai/loghub

## 22 Stack Overflow is a community-driven Q&A website for programmers

where developers ask and answer questions on a variety of topics. More 
information: https://stackoverflow.com

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

to new logs. furthermore, as shown in the examples, LLMs enhance 
accuracy and interpretability when tested against traditional methods. 
Among these new approaches, the use of RAG is a promising technique 
that integrates external knowledge to improve context-awareness to 
further enhance anomaly detection.

A practical adoption decision requires trading off the improved 
semantic understanding of LLM-based solutions against their computational, financial, and operational costs. Computationally, lightweight 
statistical or reconstruction methods (e.g., SR, FFT, PCA) and tree- 
or ensemble-based algorithms (e.g., IF, SVM) have low inference latency and small memory footprints, making them suitable for highthroughput real-time pipelines (Poenaru-Olaru et al., 2024). By contrast, full-sized LLMs incur much higher memory and compute requirements at inference, increasing latency and requiring GPU/TPU 
resources or costly API usage (Brown et al., 2020; Mehrabi et al., 2024). 
Financially, LLM deployments may require cloud GPU instances or paid 
inference APIs, and RAG pipelines add vector-database and embeddingcomputation costs (e.g., FAISS indexing and re-ranking) that further 
increase total cost of ownership. Techniques such as adapter/LoRA tuning (OWL; Guo et al., 2023) and training-free retrieval methods (RAPID; 
No et al., 2024) can substantially lower tuning and training expenses, 
shifting costs toward inference and retrieval. Operational costs differ 
as well: conventional methods are easier to integrate, maintain, and 
explain to operators, whereas LLM/RAG systems add pipeline complexity (retrieval, prompt engineering, vector DB maintenance), pose 
privacy risks when using third-party models, and demand additional 
monitoring to detect model drift and hallucinations (Mehrabi et al., 
2024; Ovadia et al., 2023).
Regardless of whether LLMs or traditional models are used for log 
anomaly detection, certain metrics, such as F1-score, precision, and 
recall, are commonly prioritized when evaluating model performance 
(see Table A1). These metrics are widely adopted because they capture 
key aspects of anomaly detection effectiveness: precision quantifies the 
proportion of correctly identified anomalies among all flagged events, 
recall measures the ability to detect all true anomalies, and the F1score provides a balanced harmonic mean of the two (Almodovar 
et al., 2024). However, these metrics have limitations in the context 
of anomaly detection. For example, precision and recall are sensitive 
to class imbalance, which is common in anomaly detection tasks where 
anomalies are rare. A model may achieve high recall but at the expense 
of many false positives, potentially overwhelming IT operators, while 
high precision with low recall might miss critical anomalies. Moreover, 
the F1-score, by equally weighting precision and recall, may not reflect 
the operational priorities of specific domains, such as military systems, 
where missing an anomaly could have far more severe consequences 
than raising a false alert (Jeon et al., 2025). To address these limitations, future work could incorporate additional metrics, such as 
Matthews Correlation Coefficient (MCC) or area under the PrecisionRecall curve (AUC-PR), and domain-specific cost functions that better 
reflect the criticality of anomalies in high-stakes environments.

4.3. RAG

This section explores Retrieval-Augmented Generation (RAG) as a 
technique to enhance the performance of LLMs in log anomaly detection. We explain the underlying mechanism of RAG, its advantages in 
domain adaptation and contextualization, and its relevance within the 
AIOps landscape.

LLMs show remarkable level of knowledge in various domains 
due to their pre-training datasets. However, there are limitations to 
this knowledge as it does not update and it is non-specific, meaning 
that it may lack expertise in specific domains (Ovadia et al., 2023). 
To solve this, an additional postprocessing step referred as knowledge injection is essential to add knowledge to the pre-trained model 
(Ovadia et al., 2023). There are two main frameworks for knowledge 
injection: fine-tuning and RAG (Ovadia et al., 2023). Fine-tuning is

the process of adjusting a pre-trained model on a specific dataset to 
improve performance on that domain, and it can be classified into 
supervised, unsupervised, and reinforcement learning methods (Ovadia 
et al., 2023). On the other hand, RAG is an advanced method designed 
to improve the capabilities of LLMs by integrating external knowledge 
through the retrieval of databases using a semantic similarity calculation (Gao et al., 2023). It addresses limitations such as hallucinations, 
outdated information, immemorization, or reasoning failure from LLMs 
(Ovadia et al., 2023). RAG follows a process that includes indexing, 
retrieval, and generation (Gao et al., 2023). Indexing consists of cleaning and extracting the raw data and converting them into a uniform 
format, retrieval consists of prioritizing the fragments that contain the 
most similarity to the input query, retrieving them by calculating the 
similarity (e.g. cosine similarity) and using them as context in the 
prompt, and generation is the step where the input query and the 
selected documents are summarized into a prompt to which the LLM 
formulates a response (Gao et al., 2023). Although fine-tuning methods 
can improve LLM performance, Ovadia et al. (2023) show through 
different experiments that RAG outperforms this approach, especially 
when experiencing knowledge outside the original training set. The 
framework that Ovadia et al. (2023) use evaluates RAG against just the 
base model (Mistral-7B, Orca2-7B, and LLama2-7B), and unsupervised 
fine-tuning for the topics of anatomy, astronomy, college biology, college chemistry, and prehistory. Although fine-tuning improves results 
compared to the base model, it is not competitive to RAG, and it 
might be because RAG not only adds knowledge to the model but also 
incorporates context, which is a feature that fine-tuning lacks (Ovadia 
et al., 2023).

RAG employs different retrieval techniques classified as sparse or 
dense retrieval methods. Sparse retrieval methods, such as BM25 or TFIDF, rely on lexical matching between the embeddings of the question 
and document chunks, whereas dense retrieval methods use neural 
embedding models for semantic searches (Gao et al., 2023). For example, Zhang, Jia et al. (2024) employ the Dense Passage Retrieval 
(DPR) framework that uses embedding models to generate dense vectors of queries. Other advanced methods for RAG include pre-retrieval 
query reformulation, where the focus is on optimizing the structure 
of the original query re-ranking based on relevant context retrieved, 
and adding metadata to improve the relevance of the retrieval (Gao 
et al., 2023). Fig. 8 shows a RAG interface pipeline from user input to 
response generation. The user submits a query, which the system may 
refine for clarity. Then it retrieves relevant information using hybrid 
(dense retrieval) or term-based search (sparse retrieval). Lastly, it filters 
and ranks the results, and injects them into the prompt so the LLM can 
generate a context-aware response.

In the specific context of log data, these retrieval techniques show 
different trade-offs. Sparse retrieval is effective for structured tokens 
in logs, such as identifiers, but struggles with semantic variation in 
log messages. Dense retrieval, by contrast, captures semantic similarity 
between log messages better, making it more suitable for heterogeneous or evolving systems, although it requires more computational 
resources and domain-specific tuning. Hybrid retrieval combines both 
approaches, balancing the precision of lexical matching with the semantic coverage of dense embeddings. This could be advantageous 
for logs, as they often contain a mixture of structured identifiers and 
unstructured descriptions, where neither sparse nor dense retrieval 
alone is sufficient.

Regarding evaluation metrics to validate the retrieval quality, Gao 
et al. (2023) identify metrics such as Mean Reciprocal Rank (MRR), 
Hit Rate (HR), and Normalized Discounted Cumulative Gain (NDCG). 
Common metrics for evaluating the quality of the answer include BLEU, 
ROUGE, F1 scores, exact match (EM), and precision (Gao et al., 2023). 
Additionally, frameworks such as RAGAS, ARES, and TruLens employ 
LLMs to also evaluate the quality scores (Gao et al., 2023).

The growing interest in RAG has led to its deployment across 
different domains and industries. Fan et al. (2024) offer a comprehensive taxonomy of RAG along with key applications divided into

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Fig. 8. Rag pipeline (Vizniuk et al., 2024).

three perspectives: NLP applications, downstream tasks, and domainspecific applications. NLP applications include Q&A systems, chatbots, 
and fact verification. In downstream tasks, RAG supports personalized 
recommender systems and software engineering workflows such as 
code generation, data preprocessing, text-to-SQL semantic parsing, and 
program repair. Beyond general-purpose use, domain-specific applications span fields such as AI for science, finance, healthcare, and 
education (Fan et al., 2024). Arslan et al. (2024) also support these observations with a large-scale survey that maps RAG applications across 
two principal categories: task-based classification and discipline-based 
classification. Under task-based classification, there are applications 
in the areas of Q&A, text generation and summarization, information retrieval and extraction, text analysis and processing, software 
development and maintenance, and decision-making (Arslan et al., 
2024). Similarly, discipline-based classification includes domains such 
as medical/biomedical, finance, education, technology and software 
development, social and communication, and literature (Arslan et al., 
2024).
While these taxonomies highlight the breadth of RAG’s potential, 
other studies focus on its concrete implementation in specific domains, 
demonstrating how these general categories translate into real-world 
systems. In agriculture, Vizniuk et al. (2024) show how RAG can 
support decision-making scenarios that require expertise knowledge, 
such as crop cultivation, pest management strategies, or irrigation 
scheduling. The use of RAG in agriculture faces many challenges, 
such as the lack of domain-specific datasets (e.g., crop varieties, soil 
conditions, pest behavior, and climate variability), heterogeneous data 
sources, and ethical concerns around data privacy and security (Vizniuk 
et al., 2024). Vizniuk et al. (2024) also discuss a methodology that 
integrates external databases with regional agricultural knowledge that 
includes pest outbreak records, crop yield data, and weather patterns. 
The approach highlights the importance of expert validation alongside 
retrieved knowledge to minimize risks from potential inaccuracies. In 
industrial machine monitoring, Jeon et al. (2025) introduce ChatCNC, 
a conversational AI system framework that integrates LLMs to enable 
interactions with real-time Computer Numerical Control (CNC) machine data directly from operational databases using SQL queries. The

methodology involves three agents: a Question Identifier that interprets 
questions from users, a Data Retriever that manages data preprocessing 
and connects to the real-time database, and a Response Generator 
that analyzes the retrieved information and gives responses to users. 
Jeon et al. (2025) evaluate ChatCNC by human raters providing scores 
ranging from 1 to 5 in different areas, such as user satisfaction with 
the bot, run time to process each question, and perceived helpfulness 
to operators. Regarding IT operations, the quality of maintenance varies 
depending on the operator’s personal experience (Zhang, Jiang et al., 
2024). Zhang, Jiang et al. (2024) propose the RAG4ITOps framework based on RAG to facilitate Q&A systems for IT operations and 
maintenance. The methodology is composed of two stages: (1) supervised fine-tuning of embedding models and data vectorization, and 
(2) online Q&A system process. After preprocessing the data, the first 
stage vectorizes the text chunks as embeddings and stores them in a 
vector database (FAISS23). The embedding models are fine-tuned using 
contrastive learning enhanced with negative sampling methods, such 
as Homogeneous In-Batch Negative Sampling (HIS) and Auxiliary Hard 
Negative Sampling (AHNS). The LLM is fine-tuned using RAG, where it 
retrieves the top-k relevant chunks based on the input query. In the 
second stage, the operators can ask questions. Then, the embedding 
model transforms the question into an embedding, and it is used 
to retrieve the most relevant context from the database. Finally, the 
LLM can answer the specific question by referring to all the contents 
in the input prompt. Zhang, Jiang et al. (2024) use datasets that 
include operational data (e.g., tool descriptions, operation examples, 
scripts, and system configurations) and maintenance data (error logs 
labeled by humans with solutions) provided by operators. The authors 
evaluate the framework using retrieval accuracy metrics and use GPT4 as a scoring model to evaluate responses on a scale of 1 to 10. 
Similarly leveraging RAG to address operational queries, Chen et al. 
(2024) introduce the OMAI framework, designed as a Q&A system to 
assist operational staff within daily tasks specialized in the domain 
of high-energy physics. OMAI (Chen et al., 2024) uses the Xiwu24 
LLM, fine-tuned using a Helpdesk Q&A dataset by the Institute of High 
Energy Physics (IHEP). The framework retrieves external knowledge 
in the same way as RAG4ITOps (Zhang, Jiang et al., 2024). The evaluation of the framework employs metrics focused on domain-specific 
precision and operational reliability and shows that OMAI outperforms 
Vicuna-13B25 and ChatGPT when handling tasks related to high-energy 
physics.

Overall, the evidence across the different studies, retrieval techniques, evaluation frameworks, and implementations proves that RAG 
has emerged as a robust solution to improve the knowledge limitations 
of pre-trained models. It injects external knowledge and enables models 
to reason with up-to-date information, and domain-specific context. 
Therefore, as the field continues to evolve, RAG not only stands out as 
a complementary alternative to fine-tuning, but also as a foundational 
architecture when building context-aware systems.

Despite promising results, the datasets used across many cited studies (e.g., HDFS, BGL, Thunderbird, Liberty) present limitations that 
challenge the generalizability of findings (Chen et al., 2024; Fan et al., 
2024; Jeon et al., 2025; Zhang, Jiang et al., 2024). These datasets 
often focus on narrow environments such as distributed systems, supercomputers, or infrastructure logs and may lack diversity in terms of 
log structure, anomaly types, and operational contexts. For example,

## 23 FAISS (Facebook AI Similarity Search) is a library developed by Facebook

AI Research for efficient similarity search and clustering of dense vectors. More 
information: https://github.com/facebookresearch/faiss

## 24 Xiwu is a foundational language model architecture that underpins

the development of specialized systems for operational maintenance. More 
information: https://example.com/xiwu

## 25 Vicuna-13B is an open-source chatbot model derived from Meta’s LLaMA,

fine-tuned on user-shared conversation data to enhance chat performance. 
More information: https://vicuna.lmsys.org/

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

BGL and HDFS logs follow consistent formatting and domain-specific 
patterns that may not reflect the variability found in logs from IoT, 
military, or hybrid cloud environments (No et al., 2024). Furthermore, 
labels in these datasets are typically human-annotated post hoc, which 
can introduce bias or inconsistency. These limitations are echoed in 
recent literature outside the AIOps domain, such as the work by Farooq 
et al. (2022), who emphasize that robust cyberattack detection requires 
diverse, representative datasets spanning multiple network types and 
intrusion modalities. Their approach underscores the need to evaluate 
AI-based anomaly detection methods across heterogeneous data sources 
to ensure real-world applicability. As such, future studies applying RAG 
and LLMs for log anomaly detection—especially in mission, critical 
domains, should validate across broader, multi-domain benchmarks 
to mitigate overfitting to curated datasets and enhance deployment 
readiness.

While LLM- and RAG-based approaches offer superior semantic 
understanding and adaptability, they also introduce notable trade-offs. 
Their high computational and memory demands increase inference 
latency and operational costs, which can be problematic for real-time 
anomaly detection (Brown et al., 2020). Traditional methods such as 
PCA or Isolation Forests are more lightweight and easier to deploy 
in resource-constrained settings (Poenaru-Olaru et al., 2024). LLMs 
may also hallucinate, producing plausible but incorrect outputs that 
risk false positives (Ji et al., 2023). Although RAG mitigates this by 
grounding responses in external knowledge, its performance depends 
heavily on retrieval quality and well-curated knowledge bases (Chen 
et al., 2024; Lewis et al., 2020). Moreover, these approaches add 
integration complexity, requiring maintenance of retrieval pipelines 
and fine-tuning, and can raise privacy concerns when logs are shared 
with third-party APIs, particularly in sensitive domains like the military (Jeon et al., 2025; Mehrabi et al., 2024). Hence, while LLMs 
and RAG mark a step forward in anomaly detection, their deployment should be carefully weighed against resource constraints, system 
complexity, and risk tolerance.

Building on the literature reviewed, we propose a taxonomy for 
classifying LLM- and RAG-based approaches for log anomaly detection 
(see Fig. 9). This taxonomy highlights three principal dimensions: (1) 
Model Architecture, (2) Knowledge Augmentation Strategy, and (3) 
Inference Objective.

• Model Architecture:  LLM-based approaches for log anomaly detection can be broadly grouped into three categories: (a)
Transformer-based models, which leverage pre-trained architectures such as BERT or LLaMA and fine-tune them for anomaly 
detection (e.g., LogLLM, LogFormer); (b) Adapter-based or LoRAtuned models, which modify only a small subset of parameters to 
reduce computational overhead while maintaining performance 
(e.g., OWL); and (c) Prompt-based or zero-shot methods, which use 
prompting strategies – such as self-prompting, in-context learning, and chain-of-thought – to guide the model toward anomaly 
detection without task-specific retraining (e.g., LogPrompt).
• Knowledge Augmentation Strategy: Knowledge integration is a 
key differentiator between purely LLM-based and RAG-based approaches. We classify these strategies into (a) No External Knowledge, where the model relies solely on its pre-trained weights 
(e.g., LogFiT); (b) Implicit Knowledge Injection, where domain 
adaptation is achieved via fine-tuning or adapters on domainspecific logs; and (c) Explicit Knowledge Augmentation, which 
uses retrieval-based methods to dynamically incorporate external 
sources such as documentation, technical forums, or knowledge 
bases (e.g., LogExpert, RAPID). RAG methods can be further 
subdivided into sparse retrieval, dense retrieval, and hybrid retrieval
approaches.
• Inference Objective: Finally, LLM/RAG systems differ in how 
they frame the anomaly detection task. We distinguish between

(a) Classification-based methods, which output a binary label indicating normal or anomalous behavior; (b) Ranking-based methods, which score log events according to anomaly likelihood 
and allow operators to set thresholds; and (c) Explanatory methods, which not only flag anomalies but also provide naturallanguage rationales or root-cause explanations (e.g., LogPrompt’s 
interpretability focus).

In line with recent recommendations in the AIOps literature, we also 
emphasize the importance of explainability for deep learning models 
applied to log anomaly detection. Ante-hoc methods, such as modeldriven deep unrolling, offer a way to embed interpretability into the 
learning process itself by unfolding iterative optimization algorithms 
into trainable neural network architectures, enabling operators to understand how individual network layers relate to classical inference 
steps. Post-hoc approaches complement this by providing visual explanations of model predictions, for instance through saliency maps, 
attention heatmaps, or token-level importance scores that highlight 
which log segments contributed most to the anomaly classification. 
Together, these methods enhance trust and transparency in AIOps 
pipelines, which is crucial for operational decision-making, root-cause 
analysis, and compliance with regulations in safety-critical domains. By 
combining these dimensions, researchers and practitioners can better 
map the design space of LLM/RAG-based log anomaly detection systems, identify complementary techniques, and systematically compare 
their performance across datasets and operational constraints.

4.4. Theoretical framework and future applications

This section presents a theoretical framework for leveraging LLMs 
and RAG in log anomaly detection within AIOps environments. We 
outline the key components and interactions of the framework and 
propose directions for future research to validate and extend its practical applicability. Given the growing technological sophistication of 
modern defense systems, future applications in the military domain are 
particularly pressing. Log anomaly detection tools that integrate LLMs 
and RAG are well-positioned to address operational needs in areas such 
as mission planning, battlefield communication, cyber defense, and 
unmanned vehicle diagnostics—domains where the cost of undetected 
anomalies may be catastrophic.

This research aimed to conduct a comprehensive SLR on the advancements of AIOps to use LLMs for log anomaly detection within the 
military industry. However, few studies in the existing literature focus 
on LLM-based approaches for log analysis within the military context. 
For our research, we identified two works that, although not directly 
targeting log anomaly detection, do explore broader aspects of LLMs 
and AI in military scenarios. Loevenich et al. (2024) describe a framework for integrating autonomous cyber defense agents into a simulated 
NATO-inspired network environment. The study integrates Multi-Agent 
Reinforcement Learning (MARL), LLMs, and rule-based systems to automate cybersecurity tasks such as monitoring, detection, and mitigation 
to increase the capabilities of cybersecurity professionals (Loevenich 
et al., 2024). The document includes a segmented network architecture 
in which blue agents are deployed to defend multiple security zones 
against red adversaries operating within an unstructured network. In 
parallel to this development, Cui and Gao (2024) examine the explainability of generative AI in military contexts. Cui and Gao (2024) analyze 
how the ‘‘black-box’’ problem in generative AI conflicts with decisionmaking in military contexts and propose a three-stage framework with 
input, interpretation, and feedback as the main components. The input 
module allows users to provide input to the model, the interpretation 
module aims to explain the decision-making of the model, and the 
feedback module allows users to provide feedback and guidance to 
the system, enabling future improvements of the model (Cui & Gao, 
2024). In addition, Cui and Gao (2024) outline potential military 
applications of generative AI, such as reconnaissance and intelligence

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Fig. 9. Taxonomy of LLM- and RAG-based log anomaly detection methods.

gathering, operational command, and operational control, and provide 
two examples highlighting the principle of explainability: an approach 
that uses LLMs with knowledge graphs to improve military search tasks, 
and a target-strike selection mechanism that combines decision trees 
with generative AI (Cui & Gao, 2024). Despite the limited research 
on log anomaly detection with LLMs in military settings, the insights 
of these applications highlight valuable opportunities. The frameworks 
discussed offer a foundational base to bridge this gap in the literature.

Building upon these papers, future work on the use of LLMs for log 
anomaly detection within the AIOps field can focus on several directions that aim to improve applicability, efficiency, and specialization. 
Real-time anomaly detection, RAG-tailored log datasets, and this new 
application in the military domain represent key areas of exploration.

Most studies analyzed so far operate in an offline mode, which 
can limit the timeliness of anomaly detection. For example, if the 
failure perception time window is set to 10 s (an event is triggered 
every 10 s), the model must infer results within 1 s to promptly 
notify users in case of anomalies, and currently, no LLM-based work 
has adequately tackled this problem (Zhang, Jia et al., 2024). Future 
research can investigate real-time anomaly detection pipelines, where 
logs are continuously ingested, parsed, and analyzed with minimal 
latency to optimize the computational efficiency of LLMs for AIOps. 
One potential direction of research could explore methods that combine 
lightweight feature extraction modules (such as Drain-based parsing) 
to structure logs fast, followed by a fine-tuned or prompt-engineered 
LLM that is capable of handling the log streams. Another promising

direction is applying RAG to log datasets rather than typical Q&A 
systems. RAG improves the LLM’s generative capabilities with external 
context retrieved from documents, enabling more domain-specific insights. To the best of our knowledge, systematic RAG-based frameworks 
for log analysis are still rare, as most existing RAG systems target Q&A 
tasks outside of log analysis. Future implementations could store log 
templates in vector databases, allowing the system to retrieve similar 
entries when a new log template arrives and then consolidate the 
retrieved content within the LLM’s prompt. This could enable the model 
to generate context-aware anomaly classifications, potentially reducing 
hallucinations and improving interpretability. Finally, research on applying LLMs explicitly to military log analytics remains scarce. Future 
studies could investigate how domain-specific knowledge bases may 
be retrieved via RAG to give LLMs specialized context in the military 
industry.

We propose a framework (see Fig. 10) to guide researchers in 
implementing a robust log anomaly detection system using LLMs with 
RAG. The framework has three main stages: definition of the project, 
database construction, and anomaly detection, mapped onto the CRISPML26 methodology, which is designed to provide a structured approach 
to ML projects from initial concept to final deployment. The first stage, 
the definition of the project, aligns with the understanding of the 
business. Researchers formulate a scientific problem that concerns the

## 26 More information: https://ml-ops.org/content/crisp-ml



Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Fig. 10. Framework.

limited capacity of traditional rule-based or statistical systems to detect 
log anomalies in complex and high-volume data environments, as traditional systems struggle to adapt to evolving system behaviors or fail 
to capture the semantic context of log messages. The research use case 
investigates how LLMs can semantically interpret log messages, integrate context via RAG, and deliver more accurate and interpretable log 
anomaly classifications. Specifically, it addresses the needs of environments such as enterprise IT systems in the military domain, where the 
detection of abnormal events is critical for IT operations. Furthermore, 
it identifies key stakeholders, including IT operators, system administrators, and maintainers. This stage also involves data collection, 
preparation, exploration, and visualization analysis to better understand the nature of the datasets. The second stage of the framework 
establishes the vector database. After data preparation, researchers read 
an anomaly log file in chunks and parse the raw logs into a structured 
representation to generate embeddings from the processed logs using 
pre-trained embedding models. These embeddings capture semantic 
patterns and represent the logs in a vector space. Researchers store 
the resulting vectors in a vector database to enable efficient lookups 
during anomaly detection. This infrastructure allows the system to 
extract context from previously processed logs, supporting a RAG-based 
interface. The vector database makes the anomaly detection process 
both context-aware and scalable to evolving requirements. Finally, the 
anomaly detection stage in the framework aligns with the modeling 
and evaluation phases of CRISP-ML. New log messages pass through 
a similar preprocessing pipeline to that used for historical logs. The 
system then leverages the vector database to retrieve any relevant 
context (similar logs, documented incidents, known anomaly patterns) 
and feeds this context along with the incoming log entries and an 
instruction template into the LLM. The LLM receives these merged 
inputs and returns a classification decision, labeling the logs as normal 
or abnormal. This stage incorporates an evaluation methodology to 
validate the LLM output.

To sum up, real-time anomaly detection, specialized RAG for logs, 
and applications in the military domain can mark the next phase of 
innovation in LLM-based log anomaly detection as an integral part 
of future AIOps strategies. The framework proposed follows CRISPML principles by beginning with a clear foundation of the research 
problem and use case, proceeding through data analysis, establishing a 
modeling infrastructure through a vector database, and concluding with 
an anomaly detection phase that includes an LLM and the evaluation 
of the outputs. This framework ensures rigorous technical development 
and continual improvement for building an anomaly detection system 
using LLMs and RAG.

## 5. Conclusion



This paper presented a SLR on how AIOps techniques can benefit 
from LLMs to improve log anomaly detection in modern IT systems. 
First, we described the core tasks of AIOPs (data preprocessing, failure

perception, root cause analysis, and auto remediation) and explain the 
challenges of logs due to their complexity and changing nature. Next, 
we compared traditional anomaly detection methods with advanced 
LLM-based approaches, including fine-tuning, prompt engineering, and 
RAG. These approaches showed more accurate and interpretable results 
in both experimental and enterprise settings.

Regarding the knowledge questions proposed in the introduction, 
we identified several answers. The primary challenges in implementing AIOps include dealing with concept drift, obtaining high-quality 
labeled datasets, and adapting to dynamic environments, while benefits involve increased reliability, scalability of IT infrastructures, fast 
detection and diagnosis, and reduction of manual effort. Common 
techniques used for anomaly detection within AIOps are traditional ML 
methods, deep learning models (LSTM, and transformers), and more 
recently, advanced use of LLMs. The main evaluation metrics in log 
anomaly detection using LLMS encompass precision, recall, F1-score, 
and AUROC. Lastly, the use of RAG substantially improves LLMs capabilities by introducing context from external sources, thereby reducing 
hallucinations or outdated information, and enabling models to reason 
with domain-specific context.

Although LLM-driven solutions show strong potential, organizations 
must address key challenges such as data privacy concerns, computational efficiency of LLMs, and limited application in critical domains 
such as military. Our study highlights domain-specific training and the 
use of RAG as promising strategies to solve these challenges. By using 
LLMs to particular operational contexts, AIOps can accelerate anomaly 
detection and be used as an external tool to help IT operators, system 
administrators, and maintainers. Focusing on the military domain is 
especially relevant given the increasing reliance of defense operations 
on autonomous systems, remote sensing technologies, and AI-driven 
command structures—all of which generate massive and sensitive log 
data. Ensuring resilience and operational integrity in such environments requires anomaly detection systems that go beyond conventional 
methods, leveraging LLMs and RAG to provide context-sensitive and 
timely responses. Although this study emphasizes military applications, 
the proposed approaches and insights are broadly generalizable to 
other high-stakes sectors, including healthcare, finance, and industrial 
systems, where reliability and rapid anomaly detection are equally 
vital.

Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to 
influence the work reported in this paper.

Appendix

See Table A1.

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Table A1
Table reporting all the articles examined to conduct the research and highlighting their main features ( ‘‘/’’ = None).
 Topic
Author
Settings
Main purpose
Data-driven techniques
Metrics for evaluation
 AIOps
Zhang, Jia et al. 
(2024)

AIops for failure management
Comprehensive survey of AIops 
technology for failure management in 
the LLM era. Includes detailed 
definition of AIops tasks for failure 
management, data sources for AIops, 
and LLM-based approaches adopted 
for AIops

Foundational model, fine-tuning 
approach, embedding-based approach, 
prompt-based approach

–

Anomaly

detection

Su et al. (2024)
LLMs for forecasting and anomaly 
detection

Systematic literature review that 
examines the application of LLMs in 
forecasting and anomaly detection, 
highlighting the current state of 
research, challenges, and future 
directions.

Prompt-based, fine-tuning, zero-shot, 
one-shot, and few-shot

Precision, accuracy, recall, F1-score, 
AUROC

AI in military
Cui and Gao 
(2024)

Generative AI in military contexts
Explore the development of 
explainable generative AI in military 
contexts, followed by a framework to 
achieve explainability in generative 
AI.

Knowledge graphs
–

AI in military
Loevenich et al. 
(2024)

Military networks
Development and training of robust 
autonomous cyber defense agents 
within military networks

Multi-Agent Reinforcement Learning, 
LLMs, and a rule-based system

–

AIOps
Dang et al. 
(2019)

AIops challenges and research 
innovations

Real-world challenges in building 
AIOps solutions based on our practice 
and experience in Microsoft. Then 
they propose a roadmap of AIOps 
related research directions

–
–

AIOps
Vitui and Chen 
(2025)

AIops in large-scale enterprise 
environments (RedHat 
Openshift/K8s)

Propose an LLM-powered AIOps 
approach to automate workflows, 
enhance efficiency, and support 
decision-making in modern IT 
Operations. Integrate LLMs (e.g., 
GPT/Claude/Mistral) with a predictive 
ML tool (MLASP) to tackle capacity 
planning and other ITOM tasks.

Use LLMs for reasoning (ReAct 
framework), predictive ML for 
planning (MLASP), and RAG for 
text/document retrieval, plus other 
tools for real-time data queries

Compliance with instructions (how 
effectively the model follows user 
prompts), accuracy (ratio of correctly 
predicted instances to the total number of 
instances), latency and throughput (time 
required for the model to generate 
responses), cost (token usage)

AIOps
Prasad and Rich 
(2019)

Market Guide aimed at 
enterprise-scale IT operations

Provides a market overview of how 
AIops platforms use big data and ML 
to optimize IT operations.

–
–

Anomlay

detection

Liu et al. (2023)
LLMs for log analysis (parsers + 
anomaly detection)

Propose LopPrompt, a 
prompt-enegeering approach that 
leverages LLMs to perform online log 
parsing and anomaly detection, with 
no in-domain training. Emphasizes 
interpretability via chain-of-thought 
and in-context prompts to generate 
explanations along with predictions.

LLMs (ChatGPT and Vicona 13B) for 
zero-shot/few-shot parsing and 
anomaly detection. Advanced prompt 
strategies: self-prompt, 
chain-of-thought, and in-context 
learning

F1-score for log parsing, session-level 
F1-score for anomaly detection, and 
human evaluation for interpretability.

Anomaly

detection

Hadadi et al. 
(2024)

LLMs for anomaly detection on 
unstable logs

Compare fine-tuned GPT-3 vs 
traditional ML/DL baseline models vs 
GPT-4 prompt-engineering for 
detecting anomalies in logs that 
change over time. Investigate how 
LLM pre-training can help mitigate 
data scarcity.

Fine-tuned LLM for sequence 
classification, and prompt-based 
approach (zero/few-shot) for anomaly 
detection. They use multiple baseline 
models: PCA, IM, LogCLuster, 
DeepLog, LogAnomally, PLELog, 
LogRobust, CNN, NeuralLog

Precision, recall, F!-score (session-level 
anomaly detection. Also, they use Fisher’s 
Exact Test for statistical significance of 
differences

Anomaly

detection

Xu and Ding 
(2024)

Anomaly and OOD detection with 
LLMs

Comprehensive survey of how LLMs 
can be leveraged to detect anomalies 
or out-of-distribution samples in 
diverse data. Proposes a taxonomy 
separating ‘‘LLMs for detection’’ vs 
‘‘LLMs for generation’’.

Prompt-based approaches (in-context 
prompting, chain-of-thought), 
Contrasting-based detection, and 
LLM-generated data augmentations 
and explanations

AUROC, AUPR, F1-score, and false 
positive rate.

AIOps
Duan et al. 
(2024)

Meta-Learning for Efficient 
Adaptation in Few-Shot AIOps 
Scenarios

Propose MAML/KAD, a 
meta-learning-based anomaly detector 
for AIOps tasks, focusing on how 
few-shot learning addresses scarcity of 
failure data.

Few-shot learning methods 
(MAML/ANIL) for anomaly detection 
and classification in AIOps.

Accuracy, F1-score, zero-shot adaptation 
metrics (evaluated on log and KPI 
datasets) comparing baseline vs MAML.

Anomaly

detection

Guo et al. 
(2024)

LLms for Log anomaly detection
Propose a transformer-based 
framework for log anomaly detection 
(LogFormer) to improve generalization 
across different domains. The model 
is pre-trained on source domain to 
obtain a general knowledge of log 
data. Then, the knowledge is 
transferred to the target domain

Drain for log parsing, pre-trained 
sentence-bert for feature extraction of 
the template sequence, and 
adapter-based tuning to leverage the 
knowledge obtained during the 
pre-training.

Baseline models: SVM, Deeplog, 
LogAnomaly, LogRobust, PLELog, 2 
variants of LogFormer, and ChatGPT. For 
evaluation they use precision, recall, and 
F1-score. For practical evaluation the 
model was successfully applied to a cloud 
servicice of a company.

Anomaly

detection

Mehrabi et al. 
(2024)

Comptact fine-tunned LLM in log 
parsing

Discuss the challenges of data 
privacy, cost, and tool integration 
regarding LLMs. They explore the 
viability of supervised fine-tuning of 
an open-source compact LLM for log 
parsing.

Fine-tuning Mistral-7B via LoRA for 
log parsing (zero/few-shot vs GPT-4).

Metric-based approach: accuracy (message 
level accuracy and Levenshtein edit 
distance) and F1-score. LLM-based 
approach: use of GPT-4 as a log parser 
evaluator to rate the event templates 
form 0 to 5.

RAG
Zhang, Jia et al. 
(2024)

Retrieval-augmented Q&A for IT 
operations

Proposes RAG4ITOps, a comprehensive 
pipeline that collects enterprise-private 
docs and logs, fine-tunes an 
embedding model using contrastive 
learning with custom negative 
sampling, fine-tunes a generative LLM 
(Qwen-14b) with retrieval-augmented 
fine-tuning for domain Q&A, and 
supports an online Q&A workflow

Fine-tuned dense passage retriever 
(LoRA on a BGE-M3 backbone) plus 
retrieval-augmented instruction tuning 
of Qwen LLM; negative sampling 
(in-batch/hard negatives), chunked 
corpora, and custom instruction 
templates for knowledge acquisition 
and troubleshooting Q&A

Top-k retrieval accuracy, single-score 
mode (select first one model, and 
generate answers based on given 
questions, and then use GPT-4 as a 
scoring model to evaluate responses from 
1 to 10), and pairwise-score (both models 
generate answers to identical questions 
using the same reference chunks and then 
a scoring model asses which models’s 
reponses are better

(continued on next page)

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Table A1 (continued).
 RAG
Gao et al. 
(2023)

Survey paper on RAG
Provide a comprehensive review of 
the evolution and state-of-the-art 
methods in RAG, outlining its 
development from early Naive RAG 
to Advanced and Modular RAG. The 
paper categorizes various techniques, 
discusses the underlying retrieval, 
generation, and augmentation 
processes, and evaluates the practical 
integration of RAG within large 
language models.

Vector-based retrieval: Use sparse 
embeddings to represent and retrieve 
text chunks. Indexing and query 
optimization: Methods such as 
chunking strategies, metadata 
enrichment, query expansion, 
rewriting, and routing. Iterative and 
adaptive retrieval: Approaches that 
refine and enhance context through 
multiple passes. Fine-tuning: Tailoring 
both embedding models and 
generation models on domain-specific 
data.

The paper reviews various metrics used to 
assess RAG systems across two main 
dimensions. Retrieval: Hit Rate, Mean 
Reciprocal Rank, Normalized Discounted 
Cumulative Gain, cosine similarity. 
Generation: Accuracy, Exact Match, F1 
score, BLEU, ROUGE.

Anomaly

detection

Guo et al. 
(2023)

LLM for IT operations
Introduce OWL, a specialized large 
language model for IT operations, 
detailing its custom dataset, novel 
long-context extension (HMCE), and 
parameter-efficient tuning 
(Mixture-of-Adapter), and 
demonstrating its superior 
performance on the Owl-Bench and 
other IT tasks.

Data Augmentation: Owl-Instruct 
constructed via expert seed data and 
GPT-4–aided augmentation with strict 
quality control. Long-Context 
Extension: HMCE method uses a 
homogeneous Markov chain for 
extending input length. Efficient 
Tuning: Mixture-of-Adapter strategy 
for task-specific fine-tuning

Evaluated on Owl-Bench (Q&A and 
multiple-choice), long-context inference 
(perplexity), and downstream IT tasks like 
log anomaly detection and log parsing 
using metrics such as F1-score, precision, 
recall, and RandIndex

Anomaly

detection

Zhu et al. 
(2018)

Automated log parser survey
Present a comprehensive evaluation 
study of automated log parsing 
methods by benchmarking 13 log 
parsers on 16 real-world log datasets, 
and releasing an open-source toolkit 
(logparser).

Reviews a variety of data-driven 
approaches from frequent pattern 
mining, clustering, heuristics (iterative 
partitioning, longest common 
subsequence, parsing trees, and 
evolutionary algorithms) to 
automatically extract event templates 
from unstructured log messages.

Accuracy: Parsing accuracy (PA) that is 
defined as the ratio of correctly parsed 
log messages. Robustness: consistency of 
performance across different log types and 
volumes. Efficiency: processing time.

Anomaly

detection

He et al. (2017)
Online log parsing for web 
service management

The authors propose Drain, an online 
log parsing method that employs a 
fixed depth parse tree with specially 
designed rules to efficiently and 
accurately parse raw log messages in 
a streaming manner, enabling timely 
log analysis and effective anomaly 
detection in large-scale web service 
environments

Fixed-depth parse tree, token 
similarity (simSeq) to match log 
messages with log events.

Parsing Accuracy: Based on how 
well-parsed log messages match the 
ground-truth log events (uses F1-score). 
Efficiency: running time improvements. 
Effectiveness: demonstrated through a case 
study on anomaly detection

RAG
Chen et al. 
(2024)

LLMs for operational maintenance
Introduces OMAI, a specialized LLM 
designed to enhance IT operations at 
IHEP by reducing staff workload 
through a Q&A system. It also uses 
fine-tuning and RAG to deliver more 
accurate responses

Fine-tuning, RAG integration. The 
model is built on Xiwu.

Model evaluated via internal benchmarks 
showing an effective response rate 
exceeding 90% on common operational 
queries, indicating superior performance 
than ChatGPT

Anomaly

detection

Guan et al. 
(2024)

LLMs for log anomaly detection
Introduce LogLLM, a framework that 
leverages both transformer-based 
(BERT) and decoder-based (Llama) 
LLMs to detect anomalies in logs by 
extracting semantic vectors, aligning 
their representations via a projector, 
and classifying the log sequences 
through a novel three-stage training.

Preprocessing: regular expressions 
instead of log parsers. Semantic 
extraction through BERT. Vector 
alignment is done through a projector 
that aligns the embedding spaces of 
BERT and Llama. Classification is 
done with Llama, and training 
requires a three-stage fine-tuning 
process.

Precision, recall, and F1-score

AIOps
Mansour et al. 
(2024)

Integration od new operational 
methodologies in IT MLEs in 
Germany

This article prmarily serves as a 
literature review and analyzes the 
adoption, benefits, challenges, and 
integration strategies of DevOps, 
AIOps, DataOps, GitOps, and MLOps 
in medium-to-large IT enterprises in 
Germany, and offers a holistic 
roadmap to improve operational 
efficienct and competitiveness.

–
–

AIOps
Diaz-De-Arcaya 
et al. (2023)

MLOps and AIOps challenges and 
opportunities

The paper provides a systematic 
survey addressing challenges and 
opportunities associated with MLOps 
and AIOps. The goal is to clarify key 
issues and present frameworks that 
support the development of AI/ML 
solutions.

–
–

AIOps
Notaro et al. 
(2021)

Addressing failure management in 
IT operations through AIOps

The article provides a survey of 
AIOps approaches for failure 
management by categorizing 
contributions into five areas (failure 
prevention, failure detection, failure 
prediction, root-cause analysis, and 
remediation), and discusses future 
trends.

Reviews a wide range of AI and ML 
methods, including statistical models 
(linear/logistic regression, Bayesian 
networks), machine learning classifiers 
(SVM, decision trees, random forests), 
clustering, neural networks (LSTM, 
deep learning), and Markov models.

It summarizes metrics reported in other 
studies such as accuracy, precision, recall, 
F1-score, false-positive/negative rates, 
MSE.

AIOps
Poenaru-Olaru 
et al. (2024)

AIOps for anomaly detection in 
IT operations.

The article investigates the impact of 
concept drift on anomaly detection 
models and compares different 
maintenance strategies. It examines 
blind (periodic) versus informed 
(drift-triggered) retraining, and 
full-history versus sliding window 
retraining approaches to determine 
how best to adapt AIOps solutions to 
real-world data changes.

Some state-of-art anomaly detection 
models(FFT, spectral residual, LSTM), 
and integrate a concept drift detector 
(FEDD) to trigger model updates.

F1-score, precision, and recall.

(continued on next page)

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Table A1 (continued).
 Anomaly

detection

No et al. (2024)
Address challenges in IT 
operations by targeting real-world 
log anomaly detection in 
computer systems

This paper proposes RAPID; a 
retrieval-based log anomaly detection 
method. The goal is to leverage 
pre-trained LLMs and token-level 
information to detect anomalies in 
log files in real time without the 
need of specific training.

BERT as pre-trained models. Anomaly 
detection is reformulated as a 
retrieval problem where each query is 
compared to the normal documents 
using the cosine similarity. A KNN 
algorithm is employed to select a 
’core set’ from the document 
database.

F1-score and AUROC. Also, the authors 
use latency to validate real-time 
applicability.

Anomaly

detection

Wang et al. 
(2024)

Automated log anomaly detection 
to aid site reliability engineers in 
troubleshooting large-scale 
software systems.

The articles proposes a novel 
framework called LogExpert. It 
generates recommended steps to deal 
with anomalous logs. It integrates the 
powerful text comprehension of LLMs 
with domain-specific knowledge 
extracted from Stack Overflow

Log recognizer: It uses a BERT 
classification model to automatically 
identify software logs from noisy 
data. Extractive summarization: the 
authors use ASSORT to summarize 
long posts to reduce the number of 
tokens. Resolution generator: they use 
Faiss vector database to retrieve the 
top-k similar logs and the LLM to 
generate the steps.

Accuracy, precision, recall, F1-score, 
BLEU-4, ROUGE-L, and human 
evaluations.

RAG
Arslan et al. 
(2024)

Survey paper in the academic 
research of RAG

It reviews the key architectures, 
training strategies, application areas, 
and current limitations of 
implementing RAG.

–
–

RAG
Fan et al. (2024)
Survey paper on RA-LLMs in the 
context of digital transformation 
and NLP research.

This paper is a systematic literature 
review about existing research on 
RA-LLMs, examining the architectures, 
applications, and training strategies. 
The goal is to show how RAG can 
augment LLMs to deal with issues 
such as hallucinations, internal 
limitations, and outdated knowledge.

–
–

RAG
Vizniuk et al. 
(2024)

RA-LLMs integration into DSSs 
for agrotechnical monotoring

The goal of this article is to analyze 
the state-of-art research on developing 
and integrating LLMs with RAG for 
agricultural decision making. It 
highlights functional limitations of 
LLMs such as explainability, or biases 
in DSS applications and outlines 
interesting direction to improve 
efficiency and sustainability in the 
future.

–
–

Anomaly

detection

Guo et al. 
(2021)

Anomaly detection for online 
computer systems

The paper proposes LogBERT, a 
self-supervised framework for log 
anomaly detection. It aims to learn 
normal log sequence patterns via two 
training tasks (masked log key 
prediction and volume of hypersphere 
minimization) and then detect 
anomalies as deviations from these 
learned patterns

BERT-based transformer. Masked Log 
Key Prediction (MLKP) where 
randomly masked log keys are 
predicted, and Volume of Hypersphere 
Minimization (VHM) encourages 
normal log sequences to cluster 
together in the embedding space.

Namely precision, recall, and F1 score

Anomaly

detection

Almodovar et al. 
(2024)

System log anomaly detection
The paper introduces LogFiT, which 
is a log anomaly detector that uses 
pre-trained models such as BERT. It 
is designed to work on raw data 
without the need of log parsing. The 
model learns the semantic and 
sequential patterns of normal logs, so 
it flags deviations as anomalies.

Transformer-based LLM with 
self-supervised training. The model 
relies on top-k token prediction 
accuracy to decide whether the new 
log deviates from the normal 
behavior learned

Precision, recall, F1-score. The 
experiments are conducted on three 
datasets (HDFS, BGL, Thunderbird)

RAG
Jeon et al. 
(2025)

Conversational Q&A in 
manufacturing environments using 
RAG

Introduces ChatCNC, a framework 
that uses LLM-based multi-agent 
collaboration to enable natural 
language queries and real-time data 
retrieval from CNC machines. This 
allows operators to access and 
interpret data without specialized 
technical skills.

RAG to retrieve real-time CNC data 
via SQL queries. Use of pre-trained 
models (GPT-4, LLaMa3-8B, Mistral 
7B) to classify questions, generate 
queries, and produce responses. Use 
of prompt engineering (persona, 
context, exemplar) to tailor the LLMs

Response accuracy: categorizing responses 
based on correctness. Failure mode: 
categorizing errors. Human evaluation: 
measure user satisfaction regarding 
helpfulness and runtime performance. 
They rate them using a 1-5 scale.

RAG
Ovadia et al. 
(2023)

LLM Knowledge injection
Compare two ways of adding new or 
specialized knowledge to pre trained 
LLms (Minstral7B, Llama2-7B, 
Orca2-7B): unsupervised fine-tuning 
and RAG. Also, it investigates how 
repeated paraphrasing helps LLMs 
learn new information

Unsupervised fine-tuning (continuation 
of pretraining with domain text), 
Retrieval Augmented Generation 
(retrieving context from a vector 
database), Data Augmentation 
(paraphrases of the same fact)

Accuracy on multiple-choice tasks, relative 
accuracy gain vs baseline, and training 
loss curves

Data availability

Data will be made available on request.

## References



Almodovar, C., Sabrina, F., Karimi, S., & Azad, S. (2024). LogFiT: Log anomaly de-

tection using fine-tuned language models. IEEE Transactions on Network and Service 
Management, 21, 1715–1723. http://dx.doi.org/10.1109/TNSM.2024.3358730.
Amato, A., Osterrieder, J. R., & Machado, M. R. (2024). How can artificial intelligence

help customer intelligence for credit portfolio management? A systematic literature 
review. http://dx.doi.org/10.1016/j.jjimei.2024.100234.
Arslan, M., Ghanem, H., Munawar, S., & Cruz, C. (2024). A survey on RAG with

LLMs. In Procedia computer science: vol. 246, (pp. 3781–3790). Elsevier B.V., http:
//dx.doi.org/10.1016/j.procs.2024.09.178.

Brown, T. B., Mann, B., Ryder, N., Subbiah, M., et al. (2020). Language models are

few-shot learners. Advances in Neural Information Processing Systems, URL https:
//arxiv.org/abs/2005.14165.

Chen, S., Li, H., Zhang, Z., Sun, Z., & Cheng, Y. (2024). OMAI: A specialized large

language model for operational maintenance in institute of high energy physics 
OMAI: A specialized large language model for operational maintenance. URL 
https://pos.sissa.it/458/034/pdf.

Cui, X., & Gao, Y. (2024). Analysis on the explainable of generative artificial intelligence

in military contexts. In Lecture notes in electrical engineering: vol. 1267 LNEE, (pp. 
84–94). Springer Science and Business Media Deutschland GmbH, http://dx.doi.
org/10.1007/978-981-97-7774-7_8.

Dang, Y., Lin, Q., & Huang, P. (2019). AIOps: Real-world challenges and research

innovations. In Proceedings - 2019 IEEE/ACM 41st international conference on software 
engineering: companion, ICSE-companion 2019 (pp. 4–5). Institute of Electrical 
and Electronics Engineers Inc., http://dx.doi.org/10.1109/ICSE-Companion.2019.
00023.

Intelligent Systems with Applications 28 (2025) 200608

---

M. De la Cruz Cabello et al.

Diaz-De-Arcaya, J., Torre-Bastida, A. I., Zárate, G., Miñón, R., & Almeida, A. (2023). A

joint study of the challenges, opportunities, and roadmap of MLOps and AIOps: A 
systematic survey. ACM Computing Surveys, 56, http://dx.doi.org/10.1145/3625289.
Duan, Y., Bao, H., Bai, G., Wei, Y., Xue, K., You, Z., Zhang, Y., Liu, B., Chen, J.,

Wang, S., & Ou, Z. (2024). Learning to diagnose: Meta-learning for efficient 
adaptation in few-shot AIOps scenarios. Electronics (Switzerland), 13, http://dx.doi.
org/10.3390/electronics13112102.
Fan, W., Ding, Y., Ning, L., Wang, S., Li, H., Yin, D., Chua, T.-S., & Li, Q. (2024). A

survey on RAG meeting LLMs: Towards retrieval-augmented large language models. 
URL http://arxiv.org/abs/2405.06211.
Farooq, M., Shahid, U., Rehmani, M. H., Irfan, M., Ali, I., & Xiang, Y. (2022). Fusion of

deep learning based cyberattack detection and classification model for intelligent 
systems. Cluster Computing, 25, 1603–1617. http://dx.doi.org/10.1007/s10586-02203686-0.
Firmansyah, E. B., Machado, M. R., & Moreira, J. L. R. (2024). How can artificial

intelligence (AI) be used to manage customer lifetime value (CLV)—A systematic 
literature review. http://dx.doi.org/10.1016/j.jjimei.2024.100279.
Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., & Wang, H.

(2023). Retrieval-augmented generation for large language models: A survey. URL 
http://arxiv.org/abs/2312.10997.
Guan, W., Cao, J., Qian, S., Gao, J., & Ouyang, C. (2024). LogLLM: Log-based anomaly

detection using large language models. URL http://arxiv.org/abs/2411.08561.
Guo, H., Yang, J., Liu, J., Bai, J., Wang, B., Li, Z., Zheng, T., Zhang, B., Peng, J.,

& Tian, Q. (2024). LogFormer: A pre-train and tuning pipeline for log anomaly 
detection. URL https://arxiv.org/abs/2401.04749.
Guo, H., Yang, J., Liu, J., Yang, L., Chai, L., Bai, J., Peng, J., Hu, X., Chen, C., Zhang, D.,

Shi, X., Zheng, T., Zheng, L., Zhang, B., Xu, K., & Li, Z. (2023). OWL: A large 
language model for IT operations. URL http://arxiv.org/abs/2309.09298.
Guo, H., Yuan, S., & Wu, X. (2021). LogBERT: Log anomaly detection via BERT. URL

http://arxiv.org/abs/2103.04475.
Hadadi, F., Xu, Q., Bianculli, D., & Briand, L. (2024). Anomaly detection on unstable

logs with GPT models. URL https://arxiv.org/html/2406.07467v1.
He, P., Zhu, J., Zheng, Z., & Lyu, M. R. (2017). Drain: An online log parsing approach

with fixed depth tree. In Proceedings - 2017 IEEE 24th international conference on web 
services, ICWS 2017 (pp. 33–40). Institute of Electrical and Electronics Engineers 
Inc., http://dx.doi.org/10.1109/ICWS.2017.13.
Jeon, J., Sim, Y., Lee, H., Han, C., Yun, D., Kim, E., Nagendra, S. L., Jun, M. B., Kim, Y.,

Lee, S. W., & Lee, J. (2025). ChatCNC: Conversational machine monitoring via 
large language model and real-time data retrieval augmented generation. Journal of 
Manufacturing Systems, 79, 504–514. http://dx.doi.org/10.1016/j.jmsy.2025.01.018.
Ji, Z., Lee, N., Frieske, R., et al. (2023). Survey of hallucination in natural language

generation. ACM Computing Surveys, http://dx.doi.org/10.1145/3571730.
Lewis, P., Perez, E., Piktus, A., et al. (2020). Retrieval-augmented generation for

knowledge-intensive NLP tasks. In Advances in neural information processing systems. 
URL https://arxiv.org/abs/2005.11401.
Liu, Y., Tao, S., Meng, W., Wang, J., Ma, W., Zhao, Y., Chen, Y., Yang, H., Jiang, Y.,

& Chen, X. (2023). Interpretable online log analysis using large language models 
with prompt strategies. URL http://arxiv.org/abs/2308.07610.
Loevenich, J. F., Adler, E., Becue, A., Velazquez, A., Wrona, K., Boshnakov, V.,

Falkcrona, J., Nordbotten, N., Worthington, O. L., Roning, J., Rigolin, R., & 
Lopes, F. (2024). Training autonomous cyber defense agents: Challenges & opportunities in military networks. In Proceedings - IEEE military communications 
conference MILCOM (pp. 158–163). Institute of Electrical and Electronics Engineers 
Inc., http://dx.doi.org/10.1109/MILCOM61039.2024.10773923.

Mansour, I. J., Rejab, M. B. M., & Mahdin, H. B. (2024). Review in adoption of

DevOps, AIOps, DataOps, GitOps, MLOps in IT MLEs in Germany. International 
Journal of Engineering Trends and Technology, 72, 64–76. http://dx.doi.org/10.
14445/22315381/IJETT-V72I12P106.
Mehrabi, M., Hamou-Lhadj, A., & Moosavi, H. (2024). The effectiveness of compact fine-

tuned LLMs in log parsing. URL https://users.encs.concordia.ca/~abdelw/papers/
ICSME24_LogLLM_preprint.pdf.
No, G., Lee, Y., Kang, H., & Kang, P. (2024). Training-free retrieval-based log anomaly

detection with pre-trained language model considering token-level information. 
Engineering Applications of Artificial Intelligence, 133, http://dx.doi.org/10.1016/j.
engappai.2024.108613.
Notaro, P., Cardoso, J., & Gerndt, M. (2021). A survey of AIOps methods for failure

management. ACM Transactions on Intelligent Systems and Technology, 12, http:
//dx.doi.org/10.1145/3483424.
Ovadia, O., Brief, M., Mishaeli, M., & Elisha, O. (2023). Fine-tuning or retrieval?

Comparing knowledge injection in LLMs. URL http://arxiv.org/abs/2312.05934.
Poenaru-Olaru, L., Karpova, N., Cruz, L., Rellermeyer, J. S., & Deursen, A. V. (2024).

Is your anomaly detector ready for change? adapting aiops solutions to the real 
world. In Proceedings - 2024 IEEE/ACM 3rd international conference on AI engineering 
- software engineering for AI, CAIN 2024 (pp. 222–233). Association for Computing 
Machinery, Inc, http://dx.doi.org/10.1145/3644815.3644961.
Prasad, B. A. P., & Rich, C. (2019). Licensed for distribution market guide for

AIOps platforms. URL https://tekwurx.com/wp-content/uploads/2019/05/GartnerMarket-Guide-for-AIOps-Platforms-Nov-18.pdf.
Su, J., Jiang, C., Jin, X., Qiao, Y., Xiao, T., Ma, H., Wei, R., Jing, Z., Xu, J., & Lin, J.

(2024). Large language models for forecasting and anomaly detection: A systematic 
literature review. URL http://arxiv.org/abs/2402.10350.
Vitui, A., & Chen, T.-H. (2025). Empowering AIOps: Leveraging large language models

for IT operations management. URL http://arxiv.org/abs/2501.12461.
Vizniuk, A., Diachenko, G., Laktionov, I., Siwocha, A., Xiao, M., & Smoląg, J. (2024).

A comprehensive survey of retrieval-augmented large language models for decision 
making in agriculture: Unsolved problems and research opportunities. Journal of 
Artificial Intelligence and Soft Computing Research, 15, 115–146. http://dx.doi.org/
10.2478/jaiscr-2025-0007.
Wang, J., Chu, G., Wang, J., Sun, H., Qi, Q., Wang, Y., Qi, J., & Liao, J. (2024).

LogExpert: Log-based recommended resolutions generation using large language 
model. In Proceedings - international conference on software engineering (pp. 42–46). 
IEEE Computer Society, http://dx.doi.org/10.1145/3639476.3639773.
Wohlin, C. (2014). Guidelines for snowballing in systematic literature studies and

a replication in software engineering. In ACM international conference proceeding 
series. Association for Computing Machinery, http://dx.doi.org/10.1145/2601248.
2601268.
Xu, R., & Ding, K. (2024). Large language models for anomaly and out-of-distribution

detection: A survey. URL http://arxiv.org/abs/2409.01980.
Zhang, L., Jia, T., Jia, M., Wu, Y., Liu, A., Yang, Y., Wu, Z., Hu, X., Yu, P. S., & Li, Y.

(2024). A survey of AIOps for failure management in the Era of large language 
models. URL http://arxiv.org/abs/2406.11213.
Zhang, T., Jiang, Z., Bai, S., Zhang, T., Lin, L., Liu, Y., & Ren, J. (2024). RAG4ITOps: A

supervised fine-tunable and comprehensive RAG framework for IT operations and 
maintenance. URL http://arxiv.org/abs/2410.15805.
Zhu, J., He, S., Liu, J., He, P., Xie, Q., Zheng, Z., & Lyu, M. R. (2018). Tools and

benchmarks for automated log parsing. URL http://arxiv.org/abs/1811.03509.

Intelligent Systems with Applications 28 (2025) 200608