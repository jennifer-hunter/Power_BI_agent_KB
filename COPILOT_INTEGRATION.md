# Copilot Integration for Power BI Report Reformatter

This document outlines how Microsoft Copilot can be integrated into the Power BI report reformatting workflow while maintaining strict control over AI usage.

---

## Current Workflow (Script-Only)

```
┌─────────────────────┐
│  Power BI .Report   │
│      Folder         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ directory_flattener │  ← Flattens to Word doc
│       .py           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Word Document     │  ← Human-readable format
│  (flattened.docx)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ report_reformatter  │  ← Applies preset themes
│       .py           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Reformatted Report │
│      (.Report)      │
└─────────────────────┘
```

---

## Proposed Copilot Integration

### Where Copilot Fits In

```
┌─────────────────────┐
│   Word Document     │
│  (flattened.docx)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   COPILOT REVIEW    │  ← NEW: AI analysis & suggestions
│   (Manual Step)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Edited Word Doc    │  ← Human approves/modifies
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ report_reformatter  │
└─────────────────────┘
```

### Integration Approaches

#### Option 1: Copy-Paste to Copilot (Most Controlled)

**Pros:** Full human control, no automation, audit trail
**Cons:** Manual, time-consuming for large reports

**Process:**
1. Open the flattened Word document
2. Copy specific sections (e.g., one visual's JSON) to Copilot
3. Ask for suggestions
4. Manually apply approved changes to the Word doc
5. Run reformatter

#### Option 2: Copilot in Word (Microsoft 365)

**Pros:** Integrated experience, works within Word
**Cons:** Requires M365 Copilot license, less control over prompts

**Process:**
1. Open flattened.docx in Word with Copilot enabled
2. Use Copilot to analyze and suggest changes
3. Review and accept/reject each suggestion
4. Save and run reformatter

#### Option 3: Copilot API Integration (Future - Requires Development)

**Pros:** Automated, consistent
**Cons:** Requires API access, more complex, less human oversight

---

## Safe Prompts for Copilot

These prompts are designed to get useful suggestions while maintaining control.

### Theme Analysis Prompts

```
PROMPT 1: Color Palette Review
---
I have a Power BI report theme with these data colors:
[paste dataColors array]

Suggest improvements for:
1. Better contrast for accessibility
2. Color-blind friendly alternatives
3. Professional corporate appearance

Do NOT generate code. Only provide color hex values and explanations.
```

```
PROMPT 2: Visual Layout Review
---
Here are the positions of visuals on a 1280x720 page:
[paste position data from multiple visuals]

Suggest better x, y, width, height values to:
1. Align visuals to a clean grid
2. Balance whitespace
3. Create visual hierarchy

Provide only numeric values, no code.
```

### Content Improvement Prompts

```
PROMPT 3: Chart Type Recommendations
---
I have these visuals in my Power BI report:
- Visual 1: donutChart showing "Segment" by "Sale Price"
- Visual 2: clusteredBarChart showing "Product" by "Revenue"
[etc.]

Based on data visualization best practices, suggest:
1. Whether current chart types are appropriate
2. Alternative chart types that might work better
3. Reasoning for each suggestion

Do NOT modify any JSON. Only provide recommendations.
```

```
PROMPT 4: Title and Label Review
---
Review these Power BI visual configurations and suggest
clearer, more professional display names:
[paste relevant JSON sections]

Provide suggestions as a simple list:
- Current: "Sum of Sale Price" → Suggested: "Total Sales ($)"
```

---

## Strict Rules Compliance

### What Copilot Should NOT Do

1. **No direct file access** - Copilot should never read/write files directly
2. **No code execution** - All code runs locally via your scripts
3. **No sensitive data exposure** - Remove actual data values before sharing
4. **No automatic application** - Human must manually apply all suggestions

### What Copilot CAN Do

1. **Review JSON structure** - Suggest improvements to configuration
2. **Recommend colors** - Provide hex values for better palettes
3. **Suggest layouts** - Provide numeric coordinates for alignment
4. **Explain options** - Help understand Power BI JSON schema

### Audit Trail

For compliance, maintain a log of Copilot interactions:

```
Date: YYYY-MM-DD
Report: [report name]
Prompt Used: [which prompt template]
Suggestions Received: [summary]
Changes Applied: [what was actually changed]
Approved By: [name]
```

---

## Implementation Checklist

### Phase 1: Manual Integration (Now)
- [ ] Use copy-paste workflow with approved prompts
- [ ] Document all Copilot suggestions before applying
- [ ] Human reviews and approves every change

### Phase 2: Streamlined Workflow (Future)
- [ ] Create prompt templates file
- [ ] Build "export for Copilot" script (sanitizes sensitive data)
- [ ] Build "import from Copilot" script (validates suggestions)

### Phase 3: Semi-Automated (Requires Approval)
- [ ] Evaluate Copilot API access requirements
- [ ] Define approval workflow for AI suggestions
- [ ] Implement logging and audit capabilities

---

## Example Workflow

### Step-by-Step with Copilot

1. **Flatten the report**
   ```bash
   python directory_flattener.py
   ```

2. **Open Word document**
   - Location: `C:\Users\jenni\Documents\powerbitest_flattened.docx`

3. **Extract theme section**
   - Find: `═══ FILE: StaticResources/SharedResources/BaseThemes/CY25SU11.json ═══`
   - Copy the `dataColors` array

4. **Ask Copilot for color suggestions**
   ```
   I have this Power BI color palette:
   ["#0066CC", "#004C99", "#3399FF", ...]

   Suggest a more modern, accessible corporate palette.
   Provide 12 hex colors with explanations.
   ```

5. **Review Copilot's response**
   - Check contrast ratios
   - Verify brand alignment
   - Test for color-blind accessibility

6. **Update Word document**
   - Replace old colors with approved suggestions
   - Save document

7. **Run reformatter**
   ```bash
   python report_reformatter.py
   ```

8. **Verify in Power BI**
   - Open the reformatted .Report folder
   - Check visual appearance
   - Confirm all changes are correct

---

## Security Considerations

### Data Sanitization Before Copilot

Before sharing JSON with Copilot, remove:
- Actual data values
- Connection strings
- User/account information
- Sensitive field names

**Example sanitization:**
```json
// BEFORE (don't share):
"Entity": "sales_confidential_2024"

// AFTER (safe to share):
"Entity": "[TABLE_NAME]"
```

### What's Safe to Share

- Color hex values
- Position coordinates (x, y, width, height)
- Visual types (donutChart, barChart, etc.)
- Generic schema structure

### What's NOT Safe to Share

- Table/column names (may reveal business data)
- Measure definitions (may contain business logic)
- Filter values (may contain sensitive data)
- Connection information

---

## Future Script Enhancement Ideas

### 1. Copilot Export Script
```python
# copilot_export.py - Sanitizes report for safe Copilot sharing
# Removes: entity names, measures, filters, data values
# Keeps: structure, positions, colors, visual types
```

### 2. Copilot Import Script
```python
# copilot_import.py - Validates and applies Copilot suggestions
# Validates: JSON structure, value ranges, color formats
# Rejects: invalid hex colors, out-of-bounds positions
```

### 3. Suggestion Validator
```python
# validate_suggestions.py - Checks Copilot output before applying
# Checks: color contrast (WCAG), layout bounds, schema compliance
```

---

## Contact & Approval

Before implementing any Copilot integration beyond manual copy-paste:

1. Review this document with your compliance team
2. Get written approval for the integration level you want
3. Document the approval in your project records

---

*Document created: Based on conversation about Power BI report reformatting workflow*
*Last updated: See git history*
