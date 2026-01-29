# Copilot Prompt Guide

Safe, low-risk prompts for reformatting Power BI reports. These prompts focus on layout and styling only - they won't touch your data, queries, or measures.

---

## Agent Configuration

Before using these prompts, set up your Copilot agent using the instructions in [AGENT_CONFIG.md](AGENT_CONFIG.md).

---

## Important Warning

While these prompts include guardrails and safety instructions, **it is still possible to break your report if you prompt incorrectly**. AI agents can make mistakes or misinterpret instructions.

Always:
- Keep a backup of your original .Report folder before making any changes
- Test the reformatted report in Power BI Desktop before deleting your backup
- Start with small changes before attempting large-scale reformatting

**You are responsible for reviewing all changes before applying them.**

---

## Before You Start

**Golden Rules:**
1. Always keep a backup of your original .Report folder
2. Only modify position values (x, y, width, height) and theme colours
3. Never change anything inside `query`, `prototypeQuery`, or `dataTransforms` sections
4. Test in Power BI Desktop before deleting your original

---

## Example Prompts

These prompts combine theme styling with intelligent layout rules. Copy and adapt them to your needs.

### Light Blue Professional

```
I want the theme to be a light blue palette. Could you use your
knowledge of colour theory and accessibility to create something
professional?

For pages with one visual, make it full screen.
For pages with two visuals, make them side by side filling the screen.
For pages with three visuals, make the first visual fill half the
page on the left, and the other two stacked vertically in quarters
filling the other half.

Do not modify any query, prototypeQuery, or dataTransforms sections.
```

### Warm Earth Tones

```
I want the theme to use warm earth tones - terracotta, sand, and
olive. Could you use your knowledge of colour theory and accessibility
to create something professional?

For pages with one visual, make it full screen.
For pages with two visuals, make them side by side filling the screen.
For pages with three visuals, make the first visual fill half the
page on the left, and the other two stacked vertically in quarters
filling the other half.

Do not modify any query, prototypeQuery, or dataTransforms sections.
```

### Dark Mode Professional

```
I want a dark mode theme with a deep navy background and bright
accent colours. Could you use your knowledge of colour theory and
accessibility to ensure good contrast and readability?

For pages with one visual, make it full screen.
For pages with two visuals, make them side by side filling the screen.
For pages with three visuals, make the first visual fill half the
page on the left, and the other two stacked vertically in quarters
filling the other half.

Do not modify any query, prototypeQuery, or dataTransforms sections.
```

### Corporate Green

```
I want the theme to be a professional green palette - think
sustainability or finance. Could you use your knowledge of colour
theory and accessibility to create something that looks corporate
but modern?

For pages with one visual, make it full screen.
For pages with two visuals, make them side by side filling the screen.
For pages with three visuals, make the first visual fill half the
page on the left, and the other two stacked vertically in quarters
filling the other half.

Do not modify any query, prototypeQuery, or dataTransforms sections.
```

### Soft Purple Minimal

```
I want a soft purple and grey palette with a clean, minimal feel.
Could you use your knowledge of colour theory and accessibility to
create something professional and calming?

For pages with one visual, make it full screen.
For pages with two visuals, make them side by side filling the screen.
For pages with three visuals, make the first visual fill half the
page on the left, and the other two stacked vertically in quarters
filling the other half.

Do not modify any query, prototypeQuery, or dataTransforms sections.
```

---

## Customising the Prompts

Feel free to adjust:

- **Colour palette**: Describe the mood or specific colours you want
- **Layout rules**: Change how visuals are arranged based on count
- **Additional styling**: Ask for borders, shadows, rounded corners, etc.

Example additions:
```
Also add subtle rounded corners and a light drop shadow to each visual.
```

```
Make the background a very light grey (#F8F9FA) instead of white.
```

```
For pages with four or more visuals, arrange them in a 2x2 grid.
```

---

## Safe Review Prompts

### Check for Issues

```
Please review this Power BI report structure and tell me:
1. Are there any visuals that overlap?
2. Are there any visuals outside the page bounds (1280 x 720)?
3. Are the visuals aligned to a consistent grid?

Do not make any changes - just report what you find.
```

### List All Visuals

```
Please list all the visuals in this report with:
- Visual type
- Current position (x, y, width, height)
- Which page they are on

Do not make any changes - just provide the summary.
```

### Suggest Improvements

```
Please review the layout of this report and suggest improvements.
Do not make changes yet - just describe what you would recommend
for better alignment and visual hierarchy.
```

---

## What NOT to Ask

**Avoid these prompts - they risk breaking your report:**

- "Update the data bindings" ❌
- "Change the queries" ❌
- "Modify the measures" ❌
- "Update the entity references" ❌
- "Change the prototypeQuery" ❌
- "Add new visuals" ❌
- "Delete visuals" ❌

---

## Prompt Template

Use this template structure for safe prompts:

```
Please [ACTION] in this Power BI report.

Rules:
- Only modify [WHAT TO CHANGE]
- Do not modify query, prototypeQuery, dataTransforms, or entity sections
- Page size is 1280 x 720 pixels
- Use 40px margins and 20px gaps

[SPECIFIC INSTRUCTIONS]
```

---

## After Copilot Makes Changes

1. Download the edited Word document
2. Run `restore_from_word.py` to rebuild the .Report folder
3. Open in Power BI Desktop
4. Check all visuals display correctly
5. Check all data is still showing
6. If everything works, you can delete your backup

If something is broken, restore from your backup and try a more specific prompt.
