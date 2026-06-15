# Baseline Accuracy Judge Prompt

You are evaluating translation Accuracy.

For each source and target pair, decide whether the target preserves the meaning of the source.

Evaluate only Accuracy. Do not mark fluency, style, tone, terminology, locale convention, or design issues unless they change the meaning.

Allowed Accuracy subtypes:

- `none`: no Accuracy error is present.
- `mistranslation`: the target renders the source meaning incorrectly.
- `omission`: meaningful information from the source is missing in the target.
- `addition`: the target adds meaningful information not present in the source.
- `untranslated`: text that should be translated is left in the source language.
- `unnecessarily_translated`: text that should remain unchanged, such as a protected brand name or fixed UI label, is translated.

Allowed severity labels:

- `none`: no Accuracy error is present.
- `minor`: the meaning difference is real but low impact.
- `major`: the issue could mislead or confuse the user about important content.
- `critical`: the issue creates health, safety, legal, financial, reputational, or complete comprehension risk.

Return exactly one primary Accuracy finding.

Return raw JSON only. Do not include Markdown, code fences, or extra commentary.

If an Accuracy error is present, return this structure:

{
  "has_accuracy_error": true,
  "accuracy_subtype": "omission",
  "severity": "major",
  "justification": "Short explanation."
}

If there is no Accuracy error, return this structure:

{
  "has_accuracy_error": false,
  "accuracy_subtype": "none",
  "severity": "none",
  "justification": "The target preserves the meaning of the source."
}

Input:

- Source language: `{source_language}`
- Source: `{source}`
- Target language: `{target_language}`
- Target: `{target}`
