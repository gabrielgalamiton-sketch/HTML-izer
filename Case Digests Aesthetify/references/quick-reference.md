# Case Digests Aesthetify — Quick Reference Guide

A fast lookup sheet for classes, structural tokens, and best practices.

---

## 1. Color Palette & Typography Tokens

| Token | Class | Hex Code | Semantic Role |
| :--- | :--- | :--- | :--- |
| **Deep Navy** | `.c-navy` | `#1E3A8A` | Document titles (`h1`), Major topics (`h3`), Case titles (`h4`), Quick card titles |
| **Slate Teal** | `.c-teal` | `#0F766E` | Statutory articles, Republic Acts, G.R. Numbers, Rule provisions |
| **Forest Green** | `.c-green` | `#166534` | Mandatory elements, operative legal tests, dispositive holdings, affirmative criteria |
| **Burgundy** | `.c-burgundy` | `#991B1B` | Case names (`<em>`), Latin legal maxims, scholar citations, doctrinal names |
| **Burnt Rust** | `.c-rust` | `#C2410C` | Fatal defects, voids (*ab initio*), strict prohibitions, disqualifications |
| **Charcoal** | *(Default)* | `#1F2937` | Narrative factual statements, procedural background |

---

## 2. Quick Card Badges & Styling

```html
<!-- Facts Badge -->
<span class="quick-label label-facts">Facts</span>

<!-- Main Issue Badge -->
<span class="quick-label label-issue">Main Issue</span>

<!-- SC Ruling Badge -->
<span class="quick-label label-ruling">SC Ruling</span>
```

Corresponding CSS definitions:
- `.label-facts`: `background: #E0E7FF; color: #1E3A8A;`
- `.label-issue`: `background: #FEF3C7; color: #92400E;`
- `.label-ruling`: `background: #DCFCE7; color: #166534;`

---

## 3. Dual-Column Case Wrapper Blueprint

```html
<section class="case-section">
  <div class="case-grid">
    <!-- LEFT: Main Narrative Digest -->
    <div class="case-main">
      <h4 id="case-anchor-slug">Case Title v. Adverse Party</h4>
      <p class="case-meta">
        <span class="c-burgundy"><em>Case Title v. Adverse Party</em></span>, 
        <span class="c-teal">G.R. No. 123456</span>, Month DD, YYYY
      </p>
      <p>Body narrative text...</p>
      <blockquote>
        "Verbatim quote of seminal doctrine..."
      </blockquote>
    </div>

    <!-- RIGHT: Sticky Snapshot Card -->
    <aside class="case-sidebar">
      <div class="case-quick-card">
        <div class="quick-title">Quick Snapshot • G.R. 123456</div>
        <div class="quick-group">
          <span class="quick-label label-facts">Facts</span>
          <p class="quick-text">Essential operative facts.</p>
        </div>
        <div class="quick-group">
          <span class="quick-label label-issue">Main Issue</span>
          <p class="quick-text">Pivotal legal question.</p>
        </div>
        <div class="quick-group">
          <span class="quick-label label-ruling">SC Ruling</span>
          <p class="quick-text">Supreme Court ruling and doctrine.</p>
        </div>
      </div>
    </aside>
  </div>
</section>
```

---

## 4. Sticky Scrolling Trap Checklist

To ensure `position: sticky` on `.case-sidebar` functions smoothly:
1. **Never** set `overflow: hidden`, `overflow: clip`, or `overflow: auto` on ancestor elements like `.case-section` or `.document-container`.
2. Ensure `.case-section` is the direct parent of `.case-grid`. This constrains the sticky track to that specific case, causing the card to release naturally when scrolling to the next case.
3. Keep `top: calc(var(--nav-height) + 1.25rem);` so the card pins right below the sticky navigation bar without clipping.

---

## 5. Mode A vs. Mode B Checklist

### Mode A (Verbatim Digest Reformatting)
- [ ] Strict Zero Word Alteration on body narrative.
- [ ] Extract raw "For Quick Notes" block into `.case-sidebar`.
- [ ] Delete original raw "For Quick Notes" block from the main body text.
- [ ] Apply semantic tags (`h1`, `h3`, `h4`, `blockquote`, `ul`, `ol`).
- [ ] Colorize citations, provisions, tests, and fatal defects.

### Mode B (Synthesis & Note Creation)
- [ ] Comprehensive bar-review caliber discussion under Philippine law.
- [ ] Automatically synthesize concise Facts, Issue, and Ruling for every case into the right sidebar card.
- [ ] Add Mermaid flowcharts for multi-step tests and timelines.
