# AI Evals Workshop – Allegro x GenAI in Localisation

A hands-on workshop for localisation specialists on building evaluation pipelines for AI-generated translations. Led by Allegro's Localisation and Data team, this workshop guides participants through annotating their own translation datasets, experimenting with prompts and running structured evaluations to identify and categorise translation errors.

---

## Overview

As AI-assisted translation and localisation workflows become the norm, the role of the localisation specialist is evolving. This workshop equips you with practical skills to move beyond reviewing individual AI outputs and into designing systematic, scalable quality pipelines.

By the end of the workshop you will be able to:

- Create and annotate a localisation dataset suitable for AI evaluation
- Design and iterate on prompts for localisation tasks
- Define evaluation criteria and run quantitative assessments of model outputs
- Interpret evaluation results and use them to improve prompts and workflows

---

## Who is this for?

This workshop is designed for localisation specialists, translators, LQA reviewers and localisation engineers, as well as anyone looking to enhance their professional portfolio with hands-on AI-quality verification and evaluation skills.

---

## Workshop Structure

The workshop is divided into three stages:

### 1. Dataset Annotation
Curate and annotate a localisation dataset by hand-labelling outputs.

### 2. Prompt Experimentation
Design and iteratively refine prompts for specific localisation tasks using your annotated dataset as ground truth.

### 3. Evaluation
Run a structured evaluation to score model outputs against your annotations, identify failure modes, and plan workflow improvements.

---

## Workshop Prerequisites

To get the most out of this hands-on session, please review the following technical setup and background knowledge criteria.

### Operational Setup (Before the Workshop)
* **LangSmith Access:** Check your email for an invitation to our  [LangSmith workspace](https://eu.smith.langchain.com/). Please accept the invitation and log in before the session to ensure your access works.
* **No API Keys Needed:** Pre-configured LLM endpoints will be provided directly in the LangSmith environment.
* **Workshop Agenda:** Familiarise yourself with the Workshop Agenda. During the workshop, you will be completing a live calibration task where you will annotate e-commerce translations based on specific Accuracy subtypes and Severity levels. Reviewing these definitions beforehand will ensure a smooth, fast-paced live session.

### Knowledge Prerequisites

#### Required
* **Localisation Context:** A basic understanding of the traditional translation workflow (segments, Translation Memories, QA processes).
* **Conceptual AI Literacy:** Familiarity with what LLMs are and a conceptual understanding of how prompts work.
* **Data Comfort:** Comfort viewing and basic editing of plain-text data files (CSV, .txt, .md).

#### Recommended
* **Basic Code Literacy (Python):** You do not need to write code from scratch. However, being comfortable reading a short Python script and changing a variable string or number inside the LangSmith UI will be highly beneficial.
* **QA Frameworks:** Some familiarity with automated testing or translation quality frameworks (e.g., MQM, BLEU, DQF).

#### Pre-Reading
* To make sure you are familiar with most of the concepts we will be discussing during the workshop, please take a look at the following:
- [Offline Evaluation](https://docs.langchain.com/langsmith/evaluation)
- [Prompt Engineering](https://docs.langchain.com/langsmith/prompt-engineering)

---

## Resources


- [GEMBA – GPT-based MT evaluation](https://arxiv.org/abs/2302.13823)
- [MQM Error Typology](https://themqm.org/)
- [OpenAI Evals framework](https://github.com/openai/evals)
