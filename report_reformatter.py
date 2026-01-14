"""
Power BI Report Reformatter v3.0

Reads a Power BI PBIR .Report folder, applies professional themes,
calculates intelligent layouts based on visual types, and adds styling.

Layout: Slicers (left) | KPIs (top) | Charts (middle) | Tables (bottom)
"""

import os
import json
import shutil
from pathlib import Path
from dotenv import load_dotenv
from copy import deepcopy

load_dotenv()

# =============================================================================
# LAYOUT CONSTANTS
# =============================================================================

GRID_SIZE = 10       # Power BI default snap grid
PAGE_WIDTH = 1280    # Default page width
PAGE_HEIGHT = 720    # Default page height

PHI = 1.618          # Golden ratio

MARGIN = 40          # Page edge margin
GAP = 20             # Gap between visuals
KPI_HEIGHT = 120     # Fixed height for KPI row
SLICER_WIDTH = 200   # Fixed width for slicer sidebar
TABLE_HEIGHT = 200   # Fixed height for table area

# =============================================================================
# VISUAL TYPE CATEGORIES
# =============================================================================

KPI_TYPES = ['card', 'cardVisual', 'multiRowCard', 'kpi']
CHART_TYPES = [
    'clusteredBarChart', 'clusteredColumnChart', 'lineChart', 'barChart',
    'pieChart', 'donutChart', 'areaChart', 'waterfallChart', 'stackedBarChart',
    'stackedColumnChart', 'lineClusteredColumnComboChart', 'scatterChart',
    'treemap', 'funnel', 'gauge', 'ribbonChart', 'filledMap', 'map', 'shapeMap'
]
TABLE_TYPES = ['tableEx', 'pivotTable', 'matrix', 'table']
SLICER_TYPES = ['slicer', 'advancedSlicerVisual']

# =============================================================================
# CORPORATE BLUE THEME
# =============================================================================

CORPORATE_BLUE_THEME = {
    "name": "CorporateBlue",
    "dataColors": [
        "#0066CC",  # Primary blue
        "#00A3E0",  # Cyan blue
        "#004C99",  # Dark blue
        "#40E0D0",  # Turquoise accent
        "#003366",  # Navy
        "#5BC0DE",  # Light blue
        "#002244",  # Deep navy
        "#87CEEB",  # Sky blue
        "#0055AA",  # Medium blue
        "#00CED1",  # Dark turquoise
        "#1E90FF",  # Dodger blue
        "#4169E1",  # Royal blue
    ],
    "foreground": "#1E1E1E",
    "foregroundNeutralSecondary": "#505050",
    "foregroundNeutralTertiary": "#A0A0A0",
    "background": "#FFFFFF",
    "backgroundLight": "#F8FAFC",
    "backgroundNeutral": "#E2E8F0",
    "tableAccent": "#0066CC",
    "good": "#10B981",
    "neutral": "#F59E0B",
    "bad": "#EF4444",
    "maximum": "#0066CC",
    "center": "#F59E0B",
    "minimum": "#E0F2FE",
    "null": "#94A3B8",
    "hyperlink": "#0066CC",
    "visitedHyperlink": "#004C99",
    "textClasses": {
        "callout": {
            "fontSize": 32,
            "fontFace": "Segoe UI Light",
            "color": "#1E1E1E"
        },
        "title": {
            "fontSize": 14,
            "fontFace": "Segoe UI Semibold",
            "color": "#1E1E1E"
        },
        "header": {
            "fontSize": 12,
            "fontFace": "Segoe UI Semibold",
            "color": "#1E1E1E"
        },
        "label": {
            "fontSize": 10,
            "fontFace": "Segoe UI",
            "color": "#505050"
        }
    },
    "visualStyles": {
        "*": {
            "*": {
                "*": [{"wordWrap": True}],
                "background": [
                    {
                        "show": True,
                        "color": {"solid": {"color": "#FFFFFF"}},
                        "transparency": 0
                    }
                ],
                "border": [
                    {
                        "show": True,
                        "color": {"solid": {"color": "#E2E8F0"}},
                        "radius": 8
                    }
                ],
                "dropShadow": [
                    {
                        "show": True,
                        "preset": "BottomRight"
                    }
                ],
                "title": [
                    {
                        "show": True,
                        "fontColor": {"solid": {"color": "#1E1E1E"}},
                        "fontSize": 11,
                        "fontFamily": "Segoe UI Semibold"
                    }
                ],
                "categoryAxis": [
                    {
                        "labelColor": {"solid": {"color": "#505050"}},
                        "gridlineColor": {"solid": {"color": "#E2E8F0"}}
                    }
                ],
                "valueAxis": [
                    {
                        "labelColor": {"solid": {"color": "#505050"}},
                        "gridlineColor": {"solid": {"color": "#E2E8F0"}}
                    }
                ]
            }
        },
        "page": {
            "*": {
                "background": [
                    {
                        "color": {"solid": {"color": "#F1F5F9"}},
                        "transparency": 0
                    }
                ]
            }
        }
    }
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def snap_to_grid(value: float) -> int:
    """Round a value to the nearest grid point (10px)."""
    return round(value / GRID_SIZE) * GRID_SIZE


def get_visual_type(visual_data: dict) -> str:
    """Extract visual type from visual data."""
    return visual_data.get('visual', {}).get('visualType', 'unknown')


def categorize_visual(visual_type: str) -> str:
    """Categorize a visual type into: slicer, kpi, chart, table, or other."""
    if visual_type in SLICER_TYPES:
        return 'slicer'
    elif visual_type in KPI_TYPES:
        return 'kpi'
    elif visual_type in CHART_TYPES:
        return 'chart'
    elif visual_type in TABLE_TYPES:
        return 'table'
    else:
        return 'other'


def group_visuals_by_type(visuals: list) -> dict:
    """
    Group visuals by their category.

    Returns dict with keys: slicers, kpis, charts, tables, other
    """
    grouped = {
        'slicers': [],
        'kpis': [],
        'charts': [],
        'tables': [],
        'other': []
    }

    for v in visuals:
        visual_type = get_visual_type(v)
        category = categorize_visual(visual_type)

        if category == 'slicer':
            grouped['slicers'].append(v)
        elif category == 'kpi':
            grouped['kpis'].append(v)
        elif category == 'chart':
            grouped['charts'].append(v)
        elif category == 'table':
            grouped['tables'].append(v)
        else:
            grouped['other'].append(v)

    return grouped


# =============================================================================
# VISUAL STYLING
# =============================================================================

def get_visual_styling() -> dict:
    """
    Return the objects dict to add to each visual for professional styling.
    Includes: white background, rounded corners, drop shadow.
    """
    return {
        "background": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "color": {"solid": {"color": "#FFFFFF"}},
                    "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                }
            }
        ],
        "border": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "color": {"solid": {"color": "#E2E8F0"}},
                    "radius": {"expr": {"Literal": {"Value": "8D"}}}
                }
            }
        ],
        "dropShadow": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "color": {"solid": {"color": "#00000020"}},
                    "position": {"expr": {"Literal": {"Value": "'Outer'"}}},
                    "preset": {"expr": {"Literal": {"Value": "'BottomRight'"}}},
                    "transparency": {"expr": {"Literal": {"Value": "60D"}}}
                }
            }
        ]
    }


# =============================================================================
# LAYOUT CALCULATION
# =============================================================================

def calculate_dashboard_layout(
    grouped_visuals: dict,
    page_width: int = PAGE_WIDTH,
    page_height: int = PAGE_HEIGHT
) -> dict:
    """
    Calculate optimal positions for all visuals using dashboard layout.

    Layout:
    ┌────────┬────────────────────────────────────────────────┐
    │        │  KPI 1   │   KPI 2   │   KPI 3   │   KPI 4   │
    │        ├──────────┴───────────┴───────────┴───────────┤
    │ SLICER │                                               │
    │   S    │     Main Chart Area                           │
    │        │                                               │
    │        ├───────────────────────────────────────────────┤
    │        │     Tables Area                               │
    └────────┴───────────────────────────────────────────────┘

    Returns: dict mapping visual name to new position dict
    """
    positions = {}

    slicers = grouped_visuals.get('slicers', [])
    kpis = grouped_visuals.get('kpis', [])
    charts = grouped_visuals.get('charts', [])
    tables = grouped_visuals.get('tables', [])
    other = grouped_visuals.get('other', [])

    # Determine if we have a slicer sidebar
    has_slicers = len(slicers) > 0
    slicer_width = SLICER_WIDTH if has_slicers else 0

    # Calculate main content area
    content_left = MARGIN + slicer_width + (GAP if has_slicers else 0)
    content_width = page_width - content_left - MARGIN

    # Determine if we have KPIs (top row)
    has_kpis = len(kpis) > 0
    kpi_area_height = KPI_HEIGHT + GAP if has_kpis else 0

    # Determine if we have tables (bottom row)
    has_tables = len(tables) > 0
    table_area_height = TABLE_HEIGHT + GAP if has_tables else 0

    # Calculate chart area
    chart_top = MARGIN + kpi_area_height
    chart_height = page_height - MARGIN - kpi_area_height - table_area_height - MARGIN

    z_index = 0

    # === LAYOUT SLICERS (Left sidebar) ===
    if slicers:
        slicer_height = (page_height - 2 * MARGIN - (len(slicers) - 1) * GAP) // len(slicers)
        for i, slicer in enumerate(slicers):
            positions[slicer['name']] = {
                'x': snap_to_grid(MARGIN),
                'y': snap_to_grid(MARGIN + i * (slicer_height + GAP)),
                'z': z_index,
                'width': snap_to_grid(SLICER_WIDTH),
                'height': snap_to_grid(slicer_height),
                'tabOrder': z_index
            }
            z_index += 1

    # === LAYOUT KPIs (Top row) ===
    if kpis:
        kpi_width = (content_width - (len(kpis) - 1) * GAP) // len(kpis)
        for i, kpi in enumerate(kpis):
            positions[kpi['name']] = {
                'x': snap_to_grid(content_left + i * (kpi_width + GAP)),
                'y': snap_to_grid(MARGIN),
                'z': z_index,
                'width': snap_to_grid(kpi_width),
                'height': snap_to_grid(KPI_HEIGHT),
                'tabOrder': z_index
            }
            z_index += 1

    # === LAYOUT CHARTS (Main area - grid) ===
    if charts:
        num_charts = len(charts)

        # Determine grid dimensions
        if num_charts == 1:
            cols, rows = 1, 1
        elif num_charts == 2:
            cols, rows = 2, 1
        elif num_charts <= 4:
            cols, rows = 2, 2
        elif num_charts <= 6:
            cols, rows = 3, 2
        else:
            cols, rows = 3, 3

        chart_cell_width = (content_width - (cols - 1) * GAP) // cols
        chart_cell_height = (chart_height - (rows - 1) * GAP) // rows

        for i, chart in enumerate(charts):
            row = i // cols
            col = i % cols

            positions[chart['name']] = {
                'x': snap_to_grid(content_left + col * (chart_cell_width + GAP)),
                'y': snap_to_grid(chart_top + row * (chart_cell_height + GAP)),
                'z': z_index,
                'width': snap_to_grid(chart_cell_width),
                'height': snap_to_grid(chart_cell_height),
                'tabOrder': z_index
            }
            z_index += 1

    # === LAYOUT TABLES (Bottom area) ===
    if tables:
        table_top = page_height - MARGIN - TABLE_HEIGHT
        table_width = (content_width - (len(tables) - 1) * GAP) // len(tables)

        for i, table in enumerate(tables):
            positions[table['name']] = {
                'x': snap_to_grid(content_left + i * (table_width + GAP)),
                'y': snap_to_grid(table_top),
                'z': z_index,
                'width': snap_to_grid(table_width),
                'height': snap_to_grid(TABLE_HEIGHT),
                'tabOrder': z_index
            }
            z_index += 1

    # === LAYOUT OTHER (fill remaining space in chart area) ===
    if other:
        # Place other visuals in chart area if no charts, else below tables
        if not charts:
            other_top = chart_top
            other_height = chart_height
        else:
            other_top = MARGIN
            other_height = 200

        other_width = (content_width - (len(other) - 1) * GAP) // max(len(other), 1)

        for i, vis in enumerate(other):
            positions[vis['name']] = {
                'x': snap_to_grid(content_left + i * (other_width + GAP)),
                'y': snap_to_grid(other_top),
                'z': z_index,
                'width': snap_to_grid(other_width),
                'height': snap_to_grid(min(other_height, 300)),
                'tabOrder': z_index
            }
            z_index += 1

    return positions


# =============================================================================
# FILE PROCESSING
# =============================================================================

def process_visual_file(visual_data: dict, new_position: dict = None) -> dict:
    """
    Process a visual file - update position only.

    Note: The PBIR schema does NOT allow 'objects' at the top level of visual.json.
    All visual styling must be applied through the theme file (visualStyles section).
    """
    result = deepcopy(visual_data)

    # Only update position - styling comes from theme
    if new_position:
        result['position'] = new_position

    return result


def process_theme_file(theme_data: dict) -> dict:
    """
    Process theme file - apply Corporate Blue theme.
    """
    result = deepcopy(CORPORATE_BLUE_THEME)
    # Preserve original name for compatibility
    result['name'] = theme_data.get('name', 'CorporateBlue')
    return result


def process_page(page_dir: Path) -> None:
    """Process a single page - update layout and styling for all visuals."""
    page_name = page_dir.name
    print(f"\n  Processing page: {page_name}")

    # Read page info
    page_file = page_dir / "page.json"
    with open(page_file, 'r', encoding='utf-8') as f:
        page_data = json.load(f)

    page_width = page_data.get('width', PAGE_WIDTH)
    page_height = page_data.get('height', PAGE_HEIGHT)
    display_name = page_data.get('displayName', page_name)

    print(f"    Page: {display_name} ({page_width}x{page_height})")

    # Collect all visuals on this page
    visuals_dir = page_dir / "visuals"
    if not visuals_dir.exists():
        print(f"    No visuals folder found")
        return

    visuals = []
    visual_files = {}  # Map name to file path

    for visual_dir in visuals_dir.iterdir():
        if visual_dir.is_dir():
            visual_file = visual_dir / "visual.json"
            if visual_file.exists():
                with open(visual_file, 'r', encoding='utf-8') as f:
                    visual_data = json.load(f)
                visuals.append(visual_data)
                visual_files[visual_data['name']] = visual_file

    if not visuals:
        print(f"    No visuals found")
        return

    # Group visuals by type
    grouped = group_visuals_by_type(visuals)

    print(f"    Found: {len(grouped['slicers'])} slicers, {len(grouped['kpis'])} KPIs, "
          f"{len(grouped['charts'])} charts, {len(grouped['tables'])} tables, "
          f"{len(grouped['other'])} other")

    # Calculate optimal layout
    layout_positions = calculate_dashboard_layout(grouped, page_width, page_height)

    # Update each visual
    for visual_data in visuals:
        visual_name = visual_data.get('name', '')
        visual_type = get_visual_type(visual_data)
        visual_file = visual_files.get(visual_name)

        if not visual_file:
            continue

        new_position = layout_positions.get(visual_name)

        # Process visual with new position and styling
        new_visual_data = process_visual_file(visual_data, new_position)

        with open(visual_file, 'w', encoding='utf-8') as f:
            json.dump(new_visual_data, f, indent=2)

        if new_position:
            print(f"    [OK] {visual_type}: ({new_position['x']}, {new_position['y']}) "
                  f"{new_position['width']}x{new_position['height']}")


# =============================================================================
# MAIN REFORMATTER
# =============================================================================

def reformat_report(input_dir: str, output_dir: str) -> None:
    """
    Main function to reformat a Power BI report.

    Args:
        input_dir: Path to the source .Report folder
        output_dir: Path to output the reformatted report
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    print("=" * 65)
    print("  Power BI Report Reformatter v3.0")
    print("=" * 65)
    print(f"  Input:  {input_path}")
    print(f"  Output: {output_path}")
    print(f"  Theme:  Corporate Blue")
    print(f"  Layout: Slicers(left) | KPIs(top) | Charts(middle) | Tables(bottom)")
    print("=" * 65)

    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    # Clean and create output directory
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)

    # === Step 1: Copy all files ===
    print("\n[1/4] Copying source files...")
    file_count = 0
    for item in input_path.rglob('*'):
        if item.is_file():
            relative = item.relative_to(input_path)
            dest = output_path / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            file_count += 1
    print(f"    Copied {file_count} files")

    # === Step 2: Process pages and visuals ===
    print("\n[2/4] Processing pages and layouts...")
    pages_dir = output_path / "definition" / "pages"

    if pages_dir.exists():
        # Get page order
        pages_json = pages_dir / "pages.json"
        if pages_json.exists():
            with open(pages_json, 'r', encoding='utf-8') as f:
                pages_meta = json.load(f)
            page_order = pages_meta.get('pageOrder', [])
            print(f"    Found {len(page_order)} pages")

        # Process each page
        for page_dir in pages_dir.iterdir():
            if page_dir.is_dir() and (page_dir / "page.json").exists():
                process_page(page_dir)

    # === Step 3: Apply theme ===
    print("\n[3/4] Applying Corporate Blue theme...")
    theme_path = output_path / "StaticResources" / "SharedResources" / "BaseThemes"
    if theme_path.exists():
        for theme_file in theme_path.glob("*.json"):
            with open(theme_file, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)

            new_theme = process_theme_file(theme_data)

            with open(theme_file, 'w', encoding='utf-8') as f:
                json.dump(new_theme, f, indent=2)

            print(f"    [OK] Updated: {theme_file.name}")

    # === Step 4: Summary ===
    print("\n[4/4] Finalizing...")
    print("\n" + "=" * 65)
    print("  REFORMATTING COMPLETE!")
    print("=" * 65)
    print(f"\n  Output: {output_path.absolute()}")
    print("\n  Changes applied:")
    print("    - Corporate Blue color palette")
    print("    - Dashboard layout (slicers left, KPIs top, etc.)")
    print("    - Visual styling (rounded corners, shadows)")
    print("    - Grid-snapped positions (10px)")
    print("\n  Next: Open the output folder in Power BI Desktop")
    print("=" * 65)


def main():
    """Main entry point."""
    input_dir = os.getenv('INPUT_DIR')
    output_dir = os.getenv('OUTPUT_REPORT_DIR')

    if not input_dir:
        raise ValueError("INPUT_DIR not set in .env file")
    if not output_dir:
        output_dir = str(Path(input_dir).parent / (Path(input_dir).stem + "_reformatted.Report"))

    reformat_report(input_dir, output_dir)


if __name__ == '__main__':
    main()
