# Power BI Report Design Style Guide

## Layout Principles

### Grid System
- **Grid size**: 10px increments
- **Page margins**: 40px on all sides
- **Gap between visuals**: 20px
- **Standard page size**: 1280 x 720 pixels

### Visual Hierarchy

1. **Top Row** - KPIs and key metrics (120px height)
2. **Main Area** - Charts and visualizations (2x2 or 3x2 grid)
3. **Bottom Row** - Tables and detailed data (200px height)
4. **Left Sidebar** - Slicers/filters (200px width, if present)

### Layout by Composition Type

#### KPI Dashboard
```
┌─────────────────────────────────────────────────┐
│  KPI    │  KPI    │  KPI    │  KPI              │  ← 120px
├─────────┴─────────┴─────────┴───────────────────┤
│                    │                            │
│    Main Chart      │      Main Chart            │  ← Fill
│                    │                            │
├────────────────────┴────────────────────────────┤
│                    │                            │
│    Chart           │      Chart                 │
│                    │                            │
└─────────────────────────────────────────────────┘
```

#### Analytical (with slicers)
```
┌────────┬────────────────────────────────────────┐
│        │  KPI    │  KPI    │  KPI               │
│ Slicer ├─────────┴─────────┴────────────────────┤
│        │                                        │
│ 200px  │           Main Chart Area              │
│        │                                        │
│        ├────────────────────────────────────────┤
│        │              Table                     │
└────────┴────────────────────────────────────────┘
```

## Theme Guidelines

### Color Palettes

#### Corporate Blue (Professional/Finance)
```json
{
  "dataColors": [
    "#0066CC", "#004C99", "#3399FF", "#66B2FF",
    "#99CCFF", "#003366", "#0080FF", "#4DA6FF",
    "#80BFFF", "#B3D9FF", "#002244", "#0059B3"
  ],
  "background": "#FFFFFF",
  "foreground": "#1A1A1A",
  "accent": "#0066CC"
}
```

#### Modern Dark (Tech/Startup)
```json
{
  "dataColors": [
    "#00D4FF", "#00A3CC", "#0077B6", "#023E8A",
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
    "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F"
  ],
  "background": "#1E1E2E",
  "foreground": "#FFFFFF",
  "accent": "#00D4FF"
}
```

#### Clean Minimal (Executive)
```json
{
  "dataColors": [
    "#2C3E50", "#34495E", "#7F8C8D", "#95A5A6",
    "#BDC3C7", "#1ABC9C", "#16A085", "#3498DB",
    "#2980B9", "#9B59B6", "#8E44AD", "#E74C3C"
  ],
  "background": "#FFFFFF",
  "foreground": "#2C3E50",
  "accent": "#3498DB"
}
```

### Visual Styling

All visuals should have:
- **Border radius**: 8px
- **Border color**: Theme-appropriate (e.g., #E2E8F0 for light themes)
- **Drop shadow**: BottomRight preset
- **Background**: Solid fill matching theme

### Typography

- **Titles**: Bold, 14pt
- **Subtitles**: Regular, 11pt
- **Data labels**: Regular, 9pt
- **Font family**: Segoe UI (default)

## Accessibility

### Color Contrast
- Minimum contrast ratio: 4.5:1 for normal text
- Minimum contrast ratio: 3:1 for large text
- Test with color blindness simulators

### Data Colors
- Avoid red/green combinations alone
- Use patterns or labels as secondary differentiators
- Ensure sequential colors have distinct luminance

## File Naming Conventions

### Template Folders
```
example-name.Report/
├── definition/
├── StaticResources/
├── _screenshot.png      # Visual reference
├── _description.md      # When to use
└── _layout-rules.json   # Machine-readable rules
```

### Theme Files
```
theme-name.json
```
- Use lowercase with hyphens
- Include style category in name (e.g., `corporate-blue-theme.json`)
