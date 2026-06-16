# Workshop Guide

## Allegro x GenAI in Localisation

## Goal of the Workshop

Participants will experience a simplified accuracy-only Automatic LQA workflow:

1. Calibrate a human gold dataset.  
2. Inspect how the dataset becomes an LLM-as-a-judge evaluation set.  
3. Run a baseline judge prompt in LangSmith.  
4. Evaluate the judge with code evaluators.  
5. Compare a second prompt version or prepared second run.  
6. Understand why meta-evaluation is necessary.

---

## MQM Category for Today: Accuracy

> **Does the target preserve the meaning of the source?**

---

## Workshop Structure

### 1. Dataset Annotation

Curate and annotate a localisation dataset by hand-labelling outputs.

Each participant will work on their own e-commerce translation dataset. Each row will contain:

- source text  
- target translation  
- English support note or back-translation for humans  
- suggested Accuracy subtype  
- suggested reason

**Your task:** For each live annotation row:

1. Confirm whether the suggested label is correct.  
2. Correct the Accuracy subtype if needed.  
3. Add severity.

## Accuracy Subtypes

| Label | Use when |
| :---- | :---- |
| `none` | No Accuracy error is present. |
| `mistranslation` | The target changes the source meaning. |
| `omission` | Meaningful source information is missing in the target. |
| `addition` | The target adds meaningful information not present in the source. |
| `untranslated` | Text that should be translated is left in the source language. |
| `unnecessarily_translated` | Text that should stay unchanged, such as a brand name, is translated. |

## Severity

| Label | Use when |
| :---- | :---- |
| `none` | No Accuracy error is present. |
| `minor` | The meaning difference is real but low impact. |
| `major` | The issue could mislead or confuse the user about important content. |
| `critical` | The issue creates health, safety, legal, financial, reputational, or complete comprehension risk. |

---

### 2. Prompt Experimentation

Design and iteratively refine prompts for specific localisation tasks using the human-annotated dataset as the ground truth.

Each participant will start from a [baseline experiment prompt](https://github.com/mjunczyk/ai-evals-workshop-allegro-genai-in-loc/blob/main/docs/prompts/baseline-judge-prompt.md) and create their own prompt version.

**Valid prompt changes include:**

- Add a clearer definition of Accuracy.  
- Add stricter subtype definitions.  
- Add severity boundary examples.  
- Add a warning not to classify fluency-only issues as Accuracy.  
- Add one or two few-shot examples.  
- Add role prompting — e.g. *"You are a senior localisation quality analyst."*  
- Add stronger JSON-format instructions.

---

### 3. Evaluation

Run a structured evaluation to score model outputs against the annotations.

Each participant will set up three evaluators:

| Evaluator | Question |  
|---|---|  
| [**Error Presence**](https://github.com/mjunczyk/ai-evals-workshop-allegro-genai-in-loc/blob/main/docs/evaluators/has_accuracy_error_match.py) | Did the judge correctly detect whether any Accuracy error is present? |   
| [**Accuracy Subtype**](https://github.com/mjunczyk/ai-evals-workshop-allegro-genai-in-loc/blob/main/docs/evaluators/accuracy_subtype_match.py) | Did the judge identify the same Accuracy subtype as the human gold annotation? |  
| [**Critical Detection**](https://github.com/mjunczyk/ai-evals-workshop-allegro-genai-in-loc/blob/main/docs/evaluators/critical_detection_match.py) | Did the judge correctly detect whether the Accuracy error is critical? |

---

## Reservations

This workshop does **not** cover:

- full MQM typology  
- multiple errors in one segment  
- span-level error matching  
- production scoring formulas  
- glossary or RAG-based evaluation

