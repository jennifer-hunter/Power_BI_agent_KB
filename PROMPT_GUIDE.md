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

## Layout Prompts

### Align All Visuals to Grid

```
Please review this Power BI report and adjust all visual positions
to snap to a 10px grid. Round x, y, width, and height values to
the nearest 10.

Do not modify any query, prototypeQuery, or dataTransforms sections.
Only change position values.
```

### Organise Visuals by Type

```
Please reorganise the visuals in this report following these rules:
- KPI cards (card, cardVisual, multiRowCard) go in the top row, height 120px
- Slicers go in a left sidebar, width 200px
- Charts go in the main area
- Tables go on the right half of the page

Page size is 1280 x 720 pixels. Use 40px margins and 20px gaps.

Do not modify any query or data binding sections - only change position values.
```

### Even Spacing

```
Please adjust the visual positions so there is consistent 20px
spacing between all visuals. Keep 40px margins from the page edges.

Only modify x, y, width, and height values. Do not change any
other properties.
```

---

## Theme Prompts

### Apply Corporate Blue Theme

```
Please update the theme file (the JSON in StaticResources/SharedResources/BaseThemes/)
with these colours:

Primary: #0066CC
Data colours: #0066CC, #004C99, #3399FF, #66B2FF, #99CCFF, #003366
Background: #FFFFFF
Text: #1A1A1A

Only modify the theme JSON file, not the visual files.
```

### Add Borders and Shadows

```
In the theme file, please add these visualStyles to give all visuals
a consistent appearance:

- Border: show true, colour #E2E8F0, radius 8px
- Drop shadow: show true, preset BottomRight
- Background: show true, colour #FFFFFF

Only modify the theme file's visualStyles section.
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
