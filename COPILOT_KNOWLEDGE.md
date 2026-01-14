# Power BI Report Design Knowledge Base

This document contains the complete knowledge base for AI-assisted Power BI report reformatting.

---

## Layout Rules by Visual Composition

### Constants
```
GRID_SIZE = 10        # All positions snap to 10px grid
MARGIN = 40           # Page margins (all sides)
GAP = 20              # Space between visuals
PAGE_WIDTH = 1280     # Standard page width
PAGE_HEIGHT = 720     # Standard page height
```

### KPI Dashboard Layout (No Tables)

**When to use**: Reports with KPI/card visuals and charts only

**Rules**:
- KPIs in top row, height = 120px
- Distribute KPIs evenly across width
- Charts fill remaining space in 2x2 grid

**Position calculations**:
```
Content width = PAGE_WIDTH - (2 * MARGIN) = 1200px
Content height = PAGE_HEIGHT - (2 * MARGIN) = 640px

KPI row:
  y = MARGIN (40)
  height = 120
  width = (content_width - (n-1)*GAP) / n  # n = number of KPIs

Chart area:
  y = MARGIN + 120 + GAP = 180
  height = remaining space / 2
  width = (content_width - GAP) / 2
```

### Mixed Layout (Charts + Table)

**When to use**: Reports with both charts and tables on the same page

**Rules**:
- KPIs in top row (if present), height = 120px
- Charts on left half (50% width)
- Table on right half (50% width, full height below KPIs)

**Position calculations**:
```
Content width = PAGE_WIDTH - (2 * MARGIN) = 1200px
Half width = (content_width - GAP) / 2 = 590px

Left side (Charts):
  x = MARGIN (40)
  width = 590

Right side (Table):
  x = MARGIN + 590 + GAP = 650
  width = 590
  y = MARGIN + KPI_HEIGHT + GAP (if KPIs) or MARGIN (if no KPIs)
  height = remaining content height
```

### Table-Focused Layout

**When to use**: Reports where the table is the primary visual

**Rules**:
- KPIs in top row (if present), height = 120px
- Table takes full page width below KPIs
- No charts, or charts on separate page

**Position calculations**:
```
Table area:
  x = MARGIN (40)
  y = MARGIN + KPI_HEIGHT + GAP (if KPIs) or MARGIN (if no KPIs)
  width = content_width (1200)
  height = remaining content height
```

### Analytical Layout (with Slicers)

**When to use**: Reports with slicers/filters

**Rules**:
- Slicers in left sidebar, width = 200px
- KPIs in top row (right of slicers)
- Charts in center-left area
- Table on right half (if present)

**Position calculations**:
```
Slicer area:
  x = MARGIN (40)
  y = MARGIN (40)
  width = 200
  height = content_height (640)

Main content area:
  x = MARGIN + 200 + GAP = 260
  available_width = PAGE_WIDTH - 260 - MARGIN = 980

If table present, split main content:
  Left (Charts): width = (980 - GAP) / 2 = 480
  Right (Table): width = 480, x = 260 + 480 + GAP = 760
```

### Executive Summary Layout

**When to use**: High-level overviews with few, large visuals

**Rules**:
- Maximum 4-6 visuals per page
- Larger visual sizes for impact
- More whitespace
- Single KPI row or no KPIs

---

## Theme Application Rules

### Corporate Blue Theme

**Complete theme JSON**:
```json
{
  "name": "Corporate Blue Professional",
  "dataColors": [
    "#0066CC", "#004C99", "#3399FF", "#66B2FF",
    "#99CCFF", "#003366", "#0080FF", "#4DA6FF",
    "#80BFFF", "#B3D9FF", "#002244", "#0059B3"
  ],
  "background": "#FFFFFF",
  "foreground": "#1A1A1A",
  "tableAccent": "#0066CC",
  "visualStyles": {
    "*": {
      "*": {
        "border": [{
          "show": true,
          "color": {"solid": {"color": "#E2E8F0"}},
          "radius": 8
        }],
        "dropShadow": [{
          "show": true,
          "preset": "BottomRight"
        }],
        "background": [{
          "show": true,
          "color": {"solid": {"color": "#FFFFFF"}},
          "transparency": 0
        }],
        "title": [{
          "show": true,
          "fontColor": {"solid": {"color": "#1A1A1A"}},
          "fontSize": 14,
          "bold": true
        }]
      }
    }
  }
}
```

### Modern Dark Theme

**Complete theme JSON**:
```json
{
  "name": "Modern Dark",
  "dataColors": [
    "#00D4FF", "#00A3CC", "#0077B6", "#023E8A",
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
    "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"
  ],
  "background": "#1E1E2E",
  "foreground": "#FFFFFF",
  "tableAccent": "#00D4FF",
  "visualStyles": {
    "*": {
      "*": {
        "border": [{
          "show": true,
          "color": {"solid": {"color": "#3D3D5C"}},
          "radius": 8
        }],
        "dropShadow": [{
          "show": true,
          "preset": "BottomRight"
        }],
        "background": [{
          "show": true,
          "color": {"solid": {"color": "#2D2D44"}},
          "transparency": 0
        }],
        "title": [{
          "show": true,
          "fontColor": {"solid": {"color": "#FFFFFF"}},
          "fontSize": 14,
          "bold": true
        }]
      }
    }
  }
}
```

### Clean Minimal Theme

**Complete theme JSON**:
```json
{
  "name": "Clean Minimal",
  "dataColors": [
    "#2C3E50", "#34495E", "#7F8C8D", "#95A5A6",
    "#BDC3C7", "#1ABC9C", "#16A085", "#3498DB",
    "#2980B9", "#9B59B6", "#8E44AD", "#E74C3C"
  ],
  "background": "#FFFFFF",
  "foreground": "#2C3E50",
  "tableAccent": "#3498DB",
  "visualStyles": {
    "*": {
      "*": {
        "border": [{
          "show": false
        }],
        "dropShadow": [{
          "show": false
        }],
        "background": [{
          "show": true,
          "color": {"solid": {"color": "#FFFFFF"}},
          "transparency": 0
        }],
        "title": [{
          "show": true,
          "fontColor": {"solid": {"color": "#2C3E50"}},
          "fontSize": 14,
          "bold": true
        }]
      }
    }
  }
}
```

---

## Typography

- **Titles**: Bold, 14pt
- **Subtitles**: Regular, 11pt
- **Data labels**: Regular, 9pt
- **Font family**: Segoe UI (Power BI default)

---

## Accessibility

### Colour Contrast
- Minimum contrast ratio: 4.5:1 for normal text
- Minimum contrast ratio: 3:1 for large text
- Always test with colour blindness simulators before finalising

### Colour Blind Friendly Design
- **Never use red/green combinations alone**
- Use patterns, shapes, or labels as secondary differentiators
- Ensure sequential colours have distinct luminance (light to dark)
- Add data labels to charts where colour is the only differentiator

### Recommended Colour Blind Safe Palettes
Instead of red/green, use:
- Blue and orange
- Blue and yellow
- Purple and yellow
- Different shades of the same colour with clear luminance difference

### Testing Tips
- Check charts in greyscale to verify luminance differences

---

## Visual Type Classification

### KPI Visuals
- `card`
- `cardVisual`
- `multiRowCard`
- `kpi`

### Chart Visuals
- `clusteredBarChart`
- `clusteredColumnChart`
- `lineChart`
- `areaChart`
- `pieChart`
- `donutChart`
- `treemap`
- `waterfallChart`
- `funnel`
- `scatterChart`
- `ribbonChart`

### Table Visuals
- `tableEx`
- `pivotTable`
- `matrix`

### Slicer Visuals
- `slicer`
- `advancedSlicerVisual`

### Other Visuals
- `shape`
- `textbox`
- `image`
- `actionButton`

---

## Visual Aspect Ratio Rules

When resizing visuals to fill the page, respect these shape constraints:

### MUST BE SQUARE (1:1 ratio)
These visuals contain circles or need equal axis treatment:
- `pieChart` - min 200x200px
- `donutChart` - min 200x200px
- `treemap` - min 200x200px
- `scatterChart` - min 250x250px
- `gauge` - min 150x150px

### MUST BE LANDSCAPE (wider than tall)
These visuals show trends or horizontal data flow:
- `lineChart` - ratio ~1.6:1, min 300x180px
- `areaChart` - ratio ~1.6:1, min 300x180px
- `clusteredBarChart` - ratio ~1.5:1, min 300x200px
- `waterfallChart` - ratio ~1.6:1, min 350x220px
- `ribbonChart` - ratio ~1.6:1, min 350x220px
- `card` / `kpi` - ratio ~3:1, min 200x80px

### MUST BE PORTRAIT (taller than wide)
These visuals flow vertically:
- `funnel` - ratio ~1:1.5, min 200x300px
- `slicer` - ratio ~1:2, min 150x300px
- `clusteredColumnChart` - ratio ~1:1.2, min 200x240px

### FLEXIBLE (either orientation)
- `tableEx` / `matrix` - adjust based on columns vs rows
- `multiRowCard` - landscape preferred but flexible

### The "Don't Stretch" Rule
NEVER make a square visual into a thin rectangle to fill space.
Instead: adjust surrounding visuals or accept whitespace.

---

## Editing Instructions for Copilot

When editing a flattened Power BI Word document:

### DO:
1. Modify position values (x, y, width, height) to align visuals
2. Update theme colors in the theme JSON file
3. Adjust visualStyles for borders, shadows, backgrounds
4. Reorder visuals logically by type
5. **Rename the theme file** when applying a new theme (e.g., change `CY25SU11.json` to `CustomTheme.json`) and update references in `report.json` - this prevents Power BI caching issues
6. **Fill the page** - resize and position visuals to use the full available space (1200x640 content area) with no large empty gaps

### DO NOT:
1. Modify `query` sections (data bindings)
2. Change `prototypeQuery` content
3. Alter entity or column references
4. Remove required schema properties
5. Add `objects` property to visual.json top level (use theme instead)

### Position Format
```json
"position": {
  "x": 40,      // Left edge (pixels from left)
  "y": 40,      // Top edge (pixels from top)
  "width": 300, // Visual width
  "height": 200 // Visual height
}
```

### File Markers
Preserve these markers exactly:
- `═══ FILE: path/to/file.json ═══` (start)
- `═══ END FILE ═══` (end)

---

## Quick Reference

### Standard Dimensions
| Element | Value |
|---------|-------|
| Page width | 1280px |
| Page height | 720px |
| Margin | 40px |
| Gap | 20px |
| KPI height | 120px |
| Slicer width | 200px |
| Half page width | 590px |
| Border radius | 8px |

### Visual Grouping Priority
1. Slicers → Left sidebar
2. KPIs → Top row
3. Charts → Left half (or full width if no table)
4. Tables → Right half (or full width if table-focused)
5. Text/Shapes → As positioned

---

*This document is the single source of truth for AI-assisted Power BI report formatting.*
