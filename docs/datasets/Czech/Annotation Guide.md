\#\#\# Dataset Annotation

Each row in your e-commerce translation dataset will contain:

\- source text    
\- target translation    
\- English support note or back-translation for humans    
\- suggested Accuracy subtype    
\- suggested reason

\*\*Your task:\*\* For each live annotation row:

1\. Confirm whether the suggested label is correct.    
2\. Correct the Accuracy subtype if needed.    
3\. Add severity.

\#\# Accuracy Subtypes

| Label | Use when |  
| :---- | :---- |  
| \`none\` | No Accuracy error is present. |  
| \`mistranslation\` | The target changes the source meaning. |  
| \`omission\` | Meaningful source information is missing in the target. |  
| \`addition\` | The target adds meaningful information not present in the source. |  
| \`untranslated\` | Text that should be translated is left in the source language. |  
| \`unnecessarily\_translated\` | Text that should stay unchanged, such as a brand name, is translated. |

\#\# Severity

| Label | Use when |  
| :---- | :---- |  
| \`none\` | No Accuracy error is present. |  
| \`minor\` | The meaning difference is real but low impact. |  
| \`major\` | The issue could mislead or confuse the user about important content. |  
| \`critical\` | The issue creates health, safety, legal, financial, reputational, or complete comprehension risk. |  
