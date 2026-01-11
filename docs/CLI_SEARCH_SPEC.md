# CLI Search Commands Specification

## Overview

Three new search commands following the same patterns as `bitwig preset`:
- `bitwig plugin` - Search VST3/AU/CLAP plugins
- `bitwig kontakt` - Search Kontakt libraries and instruments
- `bitwig m-tron` - Search M-Tron Pro IV tapes

All commands share the same design principles:
- Fuzzy, case-insensitive search
- Fast (< 2 seconds)
- No truncation (full content displayed)
- Randomized ties for similar scores

---

## Shared Code Architecture

### Base Module: `src/bitwig_cli/search.py`

```python
@dataclass
class SearchMatch:
    """Base class for search results."""
    name: str
    file_path: str
    score: float

    def to_dict(self) -> dict:
        """Override in subclasses for specific fields."""
        return {"name": self.name, "path": self.file_path}


def fuzzy_match(query: str, name: str, boost_field: str | None = None) -> float:
    """Shared fuzzy matching with optional boost field."""
    # Exact same algorithm as presets.py:_fuzzy_match
    # - Query exact match: +1.00
    # - Query substring at word boundary: +0.60 + position bonus
    # - Query substring anywhere: +0.40 + position bonus
    # - Boost field match: +0.50 exact, +0.30 partial
    # - Random jitter: ±0.03
    pass


def adaptive_table(rows, columns, title=None) -> Table:
    """Already exists in table.py - reuse as-is."""
    pass
```

### Refactor presets.py to use shared code

Move `_fuzzy_match` to `search.py` and import it.

---

## Command: `bitwig plugin`

### Data Sources

**Filesystem scan using Spotlight:**
```bash
mdfind "kMDItemContentType == 'com.apple.audio-unit-preset'"
mdfind -onlyin /Library/Audio/Plug-Ins -name ".vst3"
mdfind -onlyin /Library/Audio/Plug-Ins -name ".component"
mdfind -onlyin /Library/Audio/Plug-Ins -name ".clap"
```

**Fallback filesystem paths:**
```
~/Library/Audio/Plug-Ins/{VST3,VST,CLAP,Components}/
/Library/Audio/Plug-Ins/{VST3,VST,CLAP,Components}/
```

### PluginMatch Dataclass

```python
@dataclass
class PluginMatch(SearchMatch):
    name: str           # "Kontakt 8" (from bundle name)
    file_path: str      # Full path to .vst3/.component/.clap
    format: str         # "vst3", "au", "clap", "vst"
    vendor: str         # Extracted from Info.plist or path
    version: str | None # From Info.plist if available
    location: str       # "user" or "system"
    score: float
```

### Columns

| Column   | Key       | Description                    |
|----------|-----------|--------------------------------|
| Name     | name      | Plugin name                    |
| Format   | format    | vst3, au, clap                 |
| Vendor   | vendor    | Manufacturer                   |
| Version  | version   | Plugin version                 |
| Location | location  | user or system                 |

### CLI Options

```
bitwig plugin <query>
  -n, --limit     Max results (default: 20)
  -f, --format    Filter: vst3, au, clap
  --paths         Output paths only
  -v, --verbose   Debug logging
```

### Examples

```bash
bitwig plugin kontakt
bitwig plugin surge --format clap
bitwig plugin "native instruments" -n 10
```

---

## Command: `bitwig kontakt`

### Data Source

**Primary: Kontakt SQLite database**
```
~/Library/Application Support/Native Instruments/Kontakt 8/komplete.db3
```

**Tables:**
- `k_content_path` - Library locations and names
- `k_sound_info` - Individual instruments/presets

**Query:**
```sql
SELECT
    s.name,
    s.vendor,
    p.name as library,
    s.file_name,
    p.path || '/' || COALESCE(s.sub_path, '') || '/' || s.file_name as full_path
FROM k_sound_info s
JOIN k_content_path p ON s.content_path_id = p.id
WHERE s.name LIKE '%query%' OR p.name LIKE '%query%'
```

**Fallback: NKI file search**
```bash
mdfind -name ".nki"
```

Common library paths:
```
/Library/Application Support/Native Instruments/Kontakt 8/Content/
/Users/Shared/*Library/
/Volumes/External/kontakt_libraries/
```

### KontaktMatch Dataclass

```python
@dataclass
class KontaktMatch(SearchMatch):
    name: str           # "Electric Sunburst Deluxe"
    file_path: str      # Full path to .nki
    library: str        # "Session Guitarist - Electric Sunburst Deluxe"
    vendor: str | None  # "Native Instruments"
    category: str | None # From k_category join
    score: float
```

### Columns

| Column   | Key      | Description                     |
|----------|----------|---------------------------------|
| Name     | name     | Instrument/preset name          |
| Library  | library  | Kontakt library name            |
| Vendor   | vendor   | Publisher                       |
| Category | category | Instrument category             |

### CLI Options

```
bitwig kontakt <query>
  -n, --limit     Max results (default: 20)
  -l, --library   Filter by library name
  --paths         Output paths only
  -v, --verbose   Debug logging
```

### Examples

```bash
bitwig kontakt "electric sunburst"
bitwig kontakt piano --library "Kontakt 8 Factory"
bitwig kontakt bass -n 10
```

---

## Command: `bitwig m-tron`

### Data Source

M-Tron Pro IV stores tape metadata in:
```
~/Library/Application Support/GForce/M-Tron Pro IV/UPB_md_lib.gforce
```

This is likely a proprietary format. **Alternative approach:**

1. Parse the `props.gforce` file for any tape listings
2. Check if M-Tron has a presets folder with readable files
3. If no metadata available, provide a curated list of known tapes

**Known M-Tron Tape Banks:**
- Original Mellotron tapes (Violins, Flutes, Strings, Choir, etc.)
- M-Tron expansion packs
- Custom user recordings

### MTronMatch Dataclass

```python
@dataclass
class MTronMatch(SearchMatch):
    name: str           # "MkII Violins"
    tape_bank: str      # "Mellotron MkII" or "M400"
    layer: str          # "A" or "B"
    category: str       # "Strings", "Woodwind", "Choir", etc.
    score: float
```

### Columns

| Column   | Key       | Description                    |
|----------|-----------|--------------------------------|
| Name     | name      | Tape name                      |
| Bank     | tape_bank | Mellotron model                |
| Layer    | layer     | A or B                         |
| Category | category  | Sound category                 |

### CLI Options

```
bitwig m-tron <query>
  -n, --limit     Max results (default: 20)
  -b, --bank      Filter by tape bank
  -c, --category  Filter by category
  -v, --verbose   Debug logging
```

### Examples

```bash
bitwig m-tron violins
bitwig m-tron strings --bank "M400"
bitwig m-tron choir -n 5
```

---

## Implementation Order

1. **Create `search.py`** - Extract shared fuzzy matching
2. **Refactor `presets.py`** - Use shared code
3. **Implement `plugin.py`** - Highest value, simple filesystem scan
4. **Implement `kontakt.py`** - SQLite integration
5. **Implement `mtron.py`** - May need reverse engineering

---

## File Structure After Implementation

```
src/bitwig_cli/
├── __init__.py
├── main.py           # CLI commands
├── client.py         # Bitwig RPC client
├── protocol.py       # Wire protocol
├── search.py         # Shared fuzzy matching (NEW)
├── table.py          # Adaptive table display
├── presets.py        # Bitwig preset search (refactored)
├── plugins.py        # VST/AU/CLAP search (NEW)
├── kontakt.py        # Kontakt library search (NEW)
└── mtron.py          # M-Tron tape search (NEW)
```

---

## Design Principles (from CLAUDE.md)

1. **No truncation** - All content displayed fully
2. **Fast** - Use Spotlight/indexes, < 2 seconds
3. **Fuzzy matching** - Case insensitive, word boundaries, position bonuses
4. **Randomized ties** - Similar scores shuffle each run
5. **DRY** - Share fuzzy matching, table display code
6. **SOLID** - Single responsibility per module
7. **No regressions** - Don't remove functionality while refactoring
