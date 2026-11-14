---
name: case-digests-aesthetify
description: >-
  Transform legal texts, Philippine Supreme Court case digests, bar review topics, statutory provisions, and raw study notes into publication-grade, self-contained HTML study documents. Use this skill whenever the user wants to reformat, typeset, create, or synthesize legal study notes, bar review materials, case digests, or Philippine jurisprudence into aesthetic, highly scannable HTML documents featuring an executive legal color palette, an interactive sticky dropdown table of contents with active scroll-spy, and a dual-column layout with a contextual sticky right-hand snapshot panel for case digests.
---

# Case Digests Aesthetify — Executive Legal Typesetting & Digest Architect

An elite skill for transforming Philippine legal texts, bar review materials, statutory provisions, and case digests into publication-grade, self-contained, responsive HTML study documents.

---

## 1. Operational Modes

### Mode A: Verbatim Reformatting (Default Mode)
Active whenever the user pastes existing notes, lecture transcripts, syllabus materials, or case digests.

- **Strict Zero Word Alteration Rule for Body Text:**
  - **Do NOT** add, remove, summarize, paraphrase, or rewrite any words, sentences, doctrinal discussions, case citations, statutory references, or parentheticals in the main digest text.
  - **Retain every single doctrinal word** in its exact original sequence.
  - **Only modify typographical layout:** structural hierarchy (`h1`, `h3`, `h4`), line breaks, bullet lists (`ul`, `ol`, `li`), blockquotes (`blockquote`), and visual color tagging (`.c-navy`, `.c-teal`, `.c-green`, `.c-burgundy`, `.c-rust`).
- **Parsing "For Quick Notes":**
  - When notes include a block labeled **"For Quick Notes"** (or sections providing Quick Facts, Main Issue, and SC Ruling), extract this data exclusively into the sticky right-hand snapshot panel (`.case-sidebar` > `.case-quick-card`).
  - **Remove the raw "For Quick Notes" block from the main body text** to avoid visual clutter and duplicate text.
- **Structural Wrapper Permissibility:**
  - Structural wrappers (sticky navbars, CSS grids, snapshot cards, scripts, responsive containers, and synthesized diagrams) do **not** violate the zero-alteration rule; they enhance readability and scan speed.

### Mode B: Synthesis & Note Creation
Active when the user explicitly instructs to "create notes," "summarize," "synthesize a topic," or "draft bar review digests."

- Generate comprehensive, bar-exam caliber legal notes based on Philippine law and jurisprudence.
- For every cited case or digest, automatically synthesize and populate the sticky right-hand snapshot panel with crisp, high-yield **Facts**, **Main Issue**, and **SC Ruling** summaries.

---

## 2. Case Digest Dual-Column Architecture

Every individual case digest or jurisprudence block is structured as an isolated, scoped two-column grid.

### HTML Structure
```html
<section class="case-section">
  <div class="case-grid">
    <!-- LEFT COLUMN: Full Case Content -->
    <div class="case-main">
      <h4 id="case-slug">Case Title v. Adverse Party</h4>
      <p class="case-meta">
        <span class="c-burgundy"><em>Case Title v. Adverse Party</em></span>, 
        <span class="c-teal">G.R. No. 123456</span> (Month DD, YYYY)
      </p>
      
      <!-- Verbatim narrative / full digest body text -->
      <p>Full facts, procedural history, and legal arguments...</p>
      
      <blockquote>
        Verbatim key doctrinal holding or dispositive ratio...
      </blockquote>
      
      <p>Further analysis, ratio decidendi, and concurring opinions...</p>
    </div>

    <!-- RIGHT COLUMN: Contextual Sticky Snapshot Card -->
    <aside class="case-sidebar">
      <div class="case-quick-card">
        <div class="quick-title">Quick Snapshot • G.R. No. 123456</div>
        
        <div class="quick-group">
          <span class="quick-label label-facts">Facts</span>
          <p class="quick-text">1-3 punchy bullet points or a concise paragraph summarizing material operative facts.</p>
        </div>
        
        <div class="quick-group">
          <span class="quick-label label-issue">Main Issue</span>
          <p class="quick-text">The core legal dispute or constitutional question resolved by the Court.</p>
        </div>
        
        <div class="quick-group">
          <span class="quick-label label-ruling">SC Ruling</span>
          <p class="quick-text">The dispositive ratio, doctrinal rule, and operative legal test.</p>
        </div>
      </div>
    </aside>
  </div>
</section>
```

### Sticky Mechanics & Viewport Scrolling
- Each case is encapsulated inside its own `<section class="case-section">`.
- Because `.case-sidebar` has `position: sticky; top: calc(var(--nav-height) + 1.25rem);`, the card stays pinned beside the narrative text as the student scrolls down the long case.
- When the reader scrolls past that case into the next `<section class="case-section">`, the previous card naturally scrolls out of view and the next case's card seamlessly engages.
- **Important:** Never place `overflow: hidden`, `overflow: clip`, or `transform` on `.case-section` or `.document-container`, as this breaks standard CSS `position: sticky`.

### Responsive Layout (Mobile & Tablet)
- On screens **> 900px**: Full dual-column grid (`minmax(0, 1fr) 320px`).
- On screens **≤ 900px**: The grid collapses to a single column (`grid-template-columns: 1fr`). `.case-sidebar` switches to `position: static`, appearing cleanly right after or before the digest text as an executive briefing box.

---

## 3. Interactive Sticky Header Navigation

Every document must feature a sticky navigation header fixed to the top of the viewport:

- **Location:** Placed immediately after the opening `<body>` tag, above `.document-container`.
- **Auto-Populating TOC:** An embedded JavaScript routine dynamically scans `.document-container` for all `<h1>`, `<h3>` (Major Modules / Topics), and `<h4>` (Cases / Subsections).
  - Automatically generates slugified `id` attributes if not already present.
  - Formats dropdown options with visual hierarchy:
    - `<h1>`: Root title
    - `<h3>`: Major Module (`▪ Title`)
    - `<h4>`: Case / Subtopic (`    ↳ Title`)
- **Active Scroll-Spy:** An `IntersectionObserver` watches headings and synchronizes `<select id="toc-select">` in real time as the student scrolls through the document.
- **Print Optimization:** The header is completely suppressed during printing or PDF export (`@media print { .sticky-nav { display: none !important; } }`).

---

## 4. Systematic Legal Color Palette & Scaffolding

Apply color classes deliberately to maximize visual scannability:

| Element | Color | Hex | CSS Class | Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Titles & Headings** | Deep Navy | `#1E3A8A` | `.c-navy` | `h1`, `h3`, `h4`, main structural headers |
| **Statutory Provisions & Codes** | Slate Teal | `#0F766E` | `.c-teal` | Articles, Rules, Sections, Republic Acts, G.R. Nos. |
| **Core Definitions & Operative Rules** | Forest Green | `#166534` | `.c-green` | Operative legal tests, mandatory requisites, holdings |
| **Jurisprudence & Scholar Citations** | Burgundy | `#991B1B` | `.c-burgundy` | Case titles, citations, Latin maxims, doctrinal names |
| **Fatal Voids, Prohibitions & Exceptions** | Burnt Rust | `#C2410C` | `.c-rust` | Fatal omissions, nullities, strict exceptions, penalties |
| **Body Narrative Text** | Slate Charcoal | `#1F2937` | Default | Standard narrative paragraphs, procedural facts |

### Typographical Emphases
- **Operative Legal Tests & Requisites:** Wrap in bold underlines:
  `<span class="c-green"><strong><u>mandatory operative test</u></strong></span>`
- **Case Law References:** Italicize with Burgundy class:
  `<span class="c-burgundy"><em>Chi Ming Tsoi v. Court of Appeals</em></span>, <span class="c-teal">G.R. No. 119190 (1997)</span>`
- **Fatal Conditions, Voids & Strict Prohibitions:**
  `<span class="c-rust"><strong><u>void ab initio</u></strong></span>`
- **Key Verbatim Supreme Court Quotations:**
  Wrap in `<blockquote>` (featuring a distinctive burgundy accent left border and soft slate background).

---

## 5. Visual Aids: Nano Banana Pro 2 Infographics & Procedural Workflow Cards (Zero Mermaid)

Mermaid.js diagrams are **discontinued**. Whenever complex procedural workflows, timelines, multi-step tests, or jurisdictional hierarchies appear, enhance the text with:

### A. Pure HTML Workflow Cards (For Simple ≤ 4-Step Linear Flows)
Use `.ui-box`, `.ui-grid`, and `.ui-workflow` cards for compact sequential flows and statutory comparisons.

### B. Nano Banana Pro 2 Educational Infographics (For Complex Trees & Multi-Case Architectures)
1. **Visual Style & Palette:** Invoke `image-generator` on a crisp white (`#FFFFFF`) or light-slate (`#F8FAFC`) canvas matching Deep Navy (`#1E3A8A`), Slate Teal (`#0F766E`), Forest Green (`#166534`), and Burnt Rust (`#C2410C`), in `16:9` widescreen layout. Choose a Clean Executive Vector Infographic or conceptual illustration based on whichever depicts the procedural rule most clearly.
2. **Mandatory Visual QA Gate:** Always inspect every generated image via `read_file` before embedding. If any legal term, case name, or rule number is misspelled, regenerate/edit (up to 1 retry). If `image-generator` hits quota exhaustion, substitute clean HTML `.ui-box` cards instead of Mermaid.
3. **Asset Storage & Static Card Markup:** Save verified images into `c:\Users\IP Gaming 3\Desktop\HTML-izer\images\<doc-slug>\01-concept.jpg` and embed via a clean static responsive card (no modal or Mermaid script):
```html
<figure class="img-figure">
  <img src="images/topic-slug/01-concept.jpg" alt="Descriptive alt text of procedural flowchart" />
  <figcaption><strong>Figure 1 — Procedural Flow:</strong> Core doctrinal takeaway illustrated above.</figcaption>
</figure>
```

---

## 6. Output Delivery & GitHub Pages Workflow

Follow these mandatory rules for file generation:

1. **Direct HTML File Generation (Zero Code Dumps in Chat):**
   - **Never** dump hundreds of lines of raw HTML code or markdown fences into the chat conversation.
   - Always write the complete, standalone HTML document directly to the project directory using file tools (e.g., `c:\Users\IP Gaming 3\Desktop\HTML-izer\<filename>.html`).
2. **Automatic GitHub Pages Deployment:**
   - Immediately after writing or updating the `.html` file, stage both the `.html` file and any generated `images/<doc-slug>/` folder, commit, and push in `c:\Users\IP Gaming 3\Desktop\HTML-izer`:
     ```powershell
     git add "<filename>.html" "images/<doc-slug>"
     git commit -m "Publish <filename>.html"
     git push
     ```
3. **Concise Chat Confirmation:**
   - In your chat reply, provide only:
     - A clickable local file link (e.g., `[<filename>.html](file:///c:/Users/IP%20Gaming%203/Desktop/HTML-izer/<filename>.html)`)
     - The live shareable GitHub Pages URL: `https://gabrielgalamiton-sketch.github.io/HTML-izer/<filename>.html`
     - A high-level executive summary of the cases or topics packaged.

---

## 7. Supporting Resources & References

- **Starter HTML Template:** See [resources/template.html](./resources/template.html) for the full standalone document framework.
- **Reference Implementation:** See [examples/sample-case-digest.html](./examples/sample-case-digest.html) for a complete, multi-case study document.
- **Token Quick Reference:** See [references/quick-reference.md](./references/quick-reference.md) for CSS tokens and color classes.
