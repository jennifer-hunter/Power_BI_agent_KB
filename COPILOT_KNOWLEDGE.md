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

### KPI Dashboard Layout

**When to use**: Reports with 3+ KPI/card visuals and summary charts

**Rules**:
- KPIs in top row, height = 120px
- Distribute KPIs evenly across width
- Charts fill remaining space in 2x2 grid
- Tables (if any) at bottom, height = 200px

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

### Analytical Layout (with Slicers)

**When to use**: Reports with slicers/filters and data tables

**Rules**:
- Slicers in left sidebar, width = 200px
- KPIs in top row (right of slicers)
- Main charts in center
- Table at bottom, full width minus slicer

**Position calculations**:
```
Slicer area:
  x = MARGIN (40)
  y = MARGIN (40)
  width = 200
  height = content_height (640)

Main content:
  x = MARGIN + 200 + GAP = 260
  available_width = PAGE_WIDTH - 260 - MARGIN = 980
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

**When to use**:
- Finance and banking
- Consulting firms
- Conservative corporate environments
- Government/public sector

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

**When to use**:
- Technology companies
- Startups
- Developer/analyst audiences
- Digital/innovation contexts

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

**When to use**:
- Executive presentations
- Board reports
- Print-friendly dashboards
- Minimalist preferences

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

## Editing Instructions for Copilot

When editing a flattened Power BI Word document:

### DO:
1. Modify position values (x, y, width, height) to align visuals
2. Update theme colors in the theme JSON file
3. Adjust visualStyles for borders, shadows, backgrounds
4. Reorder visuals logically by type

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
| Table height | 200px |
| Border radius | 8px |

### Visual Grouping Priority
1. Slicers → Left sidebar
2. KPIs → Top row
3. Charts → Main area (grid)
4. Tables → Bottom row
5. Text/Shapes → As positioned

---

*This document is the single source of truth for AI-assisted Power BI report formatting.*
