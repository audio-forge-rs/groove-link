# Semantic Discovery System Plan

## Goal

Enable natural language queries like:
- "set me up for a bluegrass song"
- "70s prog rock keyboard sound"
- "something Steely Dan would use"
- "ethereal ambient pad"
- "punchy funk bass"

## Core Problem

We have thousands of instruments/presets/patches. How do we:
1. **Tag them** with genres, eras, vibes, use cases
2. **Search semantically** using natural language
3. **Stay fast** (< 1.5 seconds)
4. **Keep it simple** (no complex infrastructure)

---

## Approach: Tag Database + Fuzzy Matching

### Data Model

```
instrument_tags.csv (or SQLite)

id,source,source_id,name,tags
1,preset,/path/to/Warm Pad.bwpreset,Warm Pad,"ambient,pad,warm,mellow,cinematic"
2,kontakt,/path/to/Electric Sunburst.nki,Electric Sunburst,"guitar,acoustic,folk,country,bluegrass,americana"
3,mtron,MkII Violins,MkII Violins,"strings,orchestral,vintage,70s,prog,genesis"
```

### Tag Sources (Automated)

1. **From existing metadata**
   - M-Tron: timbres (Warm, Breathy, Dark) + types (Artist Patch, Dynamic)
   - Kontakt: categories from DB
   - Presets: device type (inst/note/fx), device name

2. **From name parsing**
   - "Warm Pad" → warm, pad
   - "Electric Sunburst" → electric, guitar
   - "MkII Violins" → violins, strings, vintage

3. **From known mappings** (static CSV)
   ```
   device,default_tags
   Polymer,synth,wavetable,modern
   FM-4,fm,digital,80s
   Phase-4,phase,analog,vintage
   ```

4. **From collection/library names**
   - "Streetly Tapes" → mellotron, vintage, 70s
   - "OrchesTron" → orchestral, cinematic
   - "ChamberTron" → chamber, intimate, classical

### Tag Sources (Manual/Curated)

5. **Genre presets** (user-editable CSV)
   ```
   genre,instruments,tags
   bluegrass,"banjo,mandolin,fiddle,acoustic guitar,upright bass","americana,folk,country,acoustic"
   prog rock,"mellotron,hammond,moog,strings","70s,genesis,yes,king crimson,vintage"
   steely dan,"rhodes,wurlitzer,clean guitar,jazz bass","jazz,fusion,70s,sophisticated"
   ```

---

## Search Algorithm

```python
def semantic_search(query: str, limit: int = 20) -> list[InstrumentMatch]:
    """
    1. Extract keywords from query
    2. Expand with synonyms/related terms
    3. Match against tag database
    4. Score by tag match coverage
    5. Return ranked results
    """

    # Step 1: Parse query into keywords
    keywords = extract_keywords(query)
    # "set me up for a bluegrass song" → ["bluegrass", "song"]

    # Step 2: Expand with genre mappings
    expanded = expand_with_genres(keywords)
    # ["bluegrass"] → ["bluegrass", "banjo", "mandolin", "fiddle", "acoustic", "folk"]

    # Step 3: Search all sources
    results = []
    for source in [presets, kontakt, mtron, plugins]:
        matches = source.search_by_tags(expanded)
        results.extend(matches)

    # Step 4: Score and rank
    for r in results:
        r.score = calculate_tag_overlap(r.tags, expanded)

    return sorted(results, key=lambda x: -x.score)[:limit]
```

---

## Genre/Vibe Mappings (Curated)

```yaml
# genres.yaml
bluegrass:
  instruments: [banjo, mandolin, fiddle, acoustic guitar, upright bass, dobro]
  tags: [americana, folk, country, acoustic, twangy]
  related: [country, folk, americana]

prog_rock:
  instruments: [mellotron, hammond, moog, synth, strings]
  tags: [70s, genesis, yes, king crimson, vintage, epic, complex]
  artists: [genesis, yes, king crimson, pink floyd, emerson lake palmer]

jazz:
  instruments: [rhodes, wurlitzer, upright bass, brushes, vibes]
  tags: [sophisticated, smooth, complex, improvisation]
  related: [fusion, bebop, cool jazz]

ambient:
  instruments: [pad, drone, texture, reverb, delay]
  tags: [atmospheric, ethereal, spacious, cinematic, calm]
  related: [electronic, new age, soundscape]

synthwave:
  instruments: [analog synth, arpeggio, bass, pad]
  tags: [80s, retro, neon, cyberpunk, nostalgic]
  related: [retrowave, outrun, electronic]
```

---

## Implementation Plan

### Phase 1: Tag Extraction (Automated)
1. Build tag extractor for each source
2. Parse names, timbres, categories
3. Store in `~/.bitwig-cli/tags.sqlite`

### Phase 2: Genre Mappings (Curated)
1. Create `genres.yaml` with common genres
2. Map instruments → genres
3. Map artists → genres

### Phase 3: Search Integration
1. New command: `bitwig find "bluegrass"`
2. Searches all sources with tag expansion
3. Returns combined, ranked results

### Phase 4: Learning (Optional)
1. Track what user actually loads
2. Adjust rankings based on usage
3. "You often use X for Y genre"

---

## Quality & Trust (Web Searches)

For discovering NEW instruments (not installed):

**Trusted Sources:**
- Native Instruments (official)
- Plugin Boutique (reviews)
- KVR Audio (user database)
- Sound on Sound (reviews)
- Tape Op (reviews)

**Quality Signals:**
- Number of reviews
- Average rating
- Professional recommendations
- "Used by" artist mentions

**Implementation:**
```python
def search_web_instruments(query: str) -> list[WebResult]:
    # Only search trusted domains
    results = web_search(
        query + " plugin instrument",
        allowed_domains=["native-instruments.com", "kvraudio.com", "soundonsound.com"]
    )
    return rank_by_trust_score(results)
```

---

## Future: Instrument Stacking

```bash
# Find 3 banjos and create comparison track
bitwig find-and-stack "banjo" --count 3

# Creates:
# Track 1: "Banjo Compare"
#   └─ XY Instrument
#       ├─ Banjo 1 (Kontakt)
#       ├─ Banjo 2 (Preset)
#       └─ Banjo 3 (Plugin)
```

Requires:
1. RPC method to create tracks
2. RPC method to add devices
3. XY Instrument for A/B/C comparison

---

## File Structure

```
~/.bitwig-cli/
├── tags.sqlite          # Auto-generated tag database
├── genres.yaml          # Curated genre mappings (editable)
├── usage.sqlite         # Track usage for learning
└── custom_tags.yaml     # User's custom instrument tags
```

---

## Example Queries

| Query | Keywords | Expanded Tags | Top Results |
|-------|----------|---------------|-------------|
| "bluegrass song" | bluegrass | banjo, mandolin, fiddle, acoustic, folk | Kontakt Banjo, Picked Acoustic, Fiddle |
| "70s prog rock" | prog, rock, 70s | mellotron, moog, genesis, vintage | M-Tron MkII Violins, Polymer Strings |
| "warm ambient pad" | warm, ambient, pad | pad, ethereal, spacious, mellow | Polymer Warm Pad, Phase-4 Ambient |
| "something funky" | funky | bass, clavinet, wah, rhythmic | FM-4 Funky Bass, Clavinet preset |

---

## Performance Target

- Tag database query: < 50ms
- Genre expansion: < 10ms
- Total search: < 200ms (well under 1.5s)

CSV/SQLite is more than fast enough for ~10,000 instruments.

---

## Next Steps (When Ready to Implement)

1. Create `tags.py` with tag extraction logic
2. Create `genres.yaml` with initial mappings
3. Create `find.py` with semantic search
4. Add `bitwig find` command
5. Test with real queries
