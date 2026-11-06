import re
import html
import markdown

INPUT_MD_PATH = r"h:\My Drive\JD 2 - Crim Pro - Cases + Ext - 08 (Combined).md"
OUTPUT_HTML_PATH = r"c:\Users\IP Gaming 3\Desktop\HTML-izer\Crim-Pro-Cases-08-Combined.html"

def read_source():
    with open(INPUT_MD_PATH, "r", encoding="utf-8") as f:
        return f.read()

def highlight_legal_terms(text):
    # Highlight statutory provisions in teal
    statute_patterns = [
        (r'\b(Rule\s+\d+(?:,\s*Section\s+[\d\(\)a-zA-Z]+)?)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Section\s+[\d\(\)a-zA-Z]+(?:,\s*Rule\s+\d+)?)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Article\s+\d+(?:,\s*paragraph\s+[\d\(\)a-zA-Z]+)?(?:\s+of\s+the\s+Revised\s+Penal\s+Code)?)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Republic\s+Act\s+(?:No\.\s*)?\d+|R\.A\.\s+No\.\s*\d+|RA\s+\d+)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Presidential\s+Decree\s+(?:No\.\s*)?\d+|P\.D\.\s+No\.\s*\d+)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Batas\s+Pambansa\s+Blg\.\s*\d+|B\.P\.\s+Blg\.\s*\d+|BP\s+22)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(G\.R\.\s+Nos?\.\s*[\d\-,]+)\b', r'<span class="c-teal">\1</span>'),
    ]
    for pat, repl in statute_patterns:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)

    # Highlight fatal defects, voids in rust
    rust_patterns = [
        (r'\b(void\s+ab\s+initio)\b', r'<span class="c-rust"><strong><u>\1</u></strong></span>'),
        (r'\b(ousted\s+of\s+jurisdiction)\b', r'<span class="c-rust"><strong><u>\1</u></strong></span>'),
        (r'\b(denial\s+of\s+due\s+process|denied\s+the\s+State\s+due\s+process|deprived\s+the\s+prosecution\s+of\s+due\s+process)\b', r'<span class="c-rust"><strong><u>\1</u></strong></span>'),
        (r'\b(fatal\s+defect|fatally\s+defective)\b', r'<span class="c-rust"><strong><u>\1</u></strong></span>'),
        (r'\b(improvident\s+plea)\b', r'<span class="c-rust"><strong>\1</strong></span>'),
    ]
    for pat, repl in rust_patterns:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)

    # Highlight core operative rules in green
    green_patterns = [
        (r'\b(double\s+jeopardy)\b', r'<span class="c-green"><strong>\1</strong></span>'),
        (r'\b(hypothetical\s+admission\s+test|hypothetical\s+admission\s+rule)\b', r'<span class="c-green"><strong><u>\1</u></strong></span>'),
        (r'\b(finality-of-acquittal\s+rule|finality-of-acquittal\s+doctrine)\b', r'<span class="c-green"><strong><u>\1</u></strong></span>'),
        (r'\b(conditions\s+sine\s+qua\s+non)\b', r'<span class="c-green"><strong><u>\1</u></strong></span>'),
        (r'\b(searching\s+inquiry\s+requirement|searching\s+inquiry)\b', r'<span class="c-green"><strong><u>\1</u></strong></span>'),
        (r'\b(two-year\s+time-bar|time-bar)\b', r'<span class="c-green"><strong>\1</strong></span>'),
    ]
    for pat, repl in green_patterns:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)

    return text

def parse_markdown_snippet(md_text):
    md = markdown.Markdown(extensions=['extra', 'sane_lists'])
    return md.convert(md_text)

def enhance_out1_headings(t):
    headers = [
        'Case Identification',
        'Facts of the Case',
        'Parties & Contentions',
        'Procedural History',
        'Issues',
        'Supreme Court Ruling and Ratio Decidendi',
        'Legal Analysis & Ratio',
        'Brief Answers to the Issues',
        'Brief Answers',
    ]
    for h in headers:
        t = re.sub(rf'(?m)^(\*?\s*{re.escape(h)}:?\s*)$', rf'\n\n##### {h}\n\n', t)
        t = re.sub(rf'(?m)^(\*?\s*{re.escape(h)}:\s*)([^\n]+)', rf'\n\n##### {h}\n\n\2', t)
    
    # Sub-headings in legal analysis:
    sub_headers = [
        r'1\.\s+Statutory\s*/\s*Rule\s+Breakdown',
        r'2\.\s+Substantive\s*/\s*Procedural\s+Requirements',
        r'3\.\s+Judicial\s+Doctrines\s+Applied',
        r'4\.\s+Legal\s+Consequence\s*/\s*Relief(?:\s*/\s*Damages)?',
    ]
    for sh in sub_headers:
        t = re.sub(rf'(?m)^(\*?\s*{sh}:?\s*)$', rf'\n\n###### \1\n\n', t)
        t = re.sub(rf'(?m)^(\*?\s*{sh}:\s*)([^\n]+)', rf'\n\n###### \1\n\n\2', t)

    return t

def enhance_out2_sections(t):
    # Recitation Doctrine / Bar Takeaway
    doc_m = re.search(r'(\*\s*Recitation Doctrine / Bar Takeaway:\s*)(.*)', t, re.DOTALL | re.IGNORECASE)
    if doc_m:
        lead = doc_m.group(1)
        doc_body = doc_m.group(2).strip()
        doc_boxed = f'\n\n<div class="doctrine-card"><div class="doctrine-header">🎯 RECITATION DOCTRINE & BAR TAKEAWAY</div><div class="doctrine-body">{doc_body}</div></div>\n\n'
        t = t[:doc_m.start()] + doc_boxed

    # Core Recitation Issue
    issue_m = re.search(r'(\*\s*Core Recitation Issue:\s*)([^\n]+(?:\n(?!\*)[^\n]+)*)', t, re.IGNORECASE)
    if issue_m:
        issue_body = issue_m.group(2).strip().strip('"')
        issue_boxed = f'\n\n<div class="recit-issue-box"><span class="recit-issue-label">📌 CORE RECITATION ISSUE</span><div class="recit-issue-text">"{issue_body}"</div></div>\n\n'
        t = t[:issue_m.start()] + issue_boxed + t[issue_m.end():]

    return t

def build_case_sections(raw_text):
    cases_raw = re.split(r'\n(?=# 08\.\d+\.)', raw_text)[1:]
    case_sections_html = []
    case_toc_items = []
    case_matrix_data = []

    case_slugs = [
        ("case-08-1-people-v-magat", "08.1. People v. Magat", "Void Pleas & Double Jeopardy", "May 31, 2000", "G.R. No. 130026", "Per Curiam (En Banc)"),
        ("case-08-2-people-v-sandiganbayan", "08.2. People v. Sandiganbayan (Alba)", "Probable Cause & Pre-Trial Acquittal", "Sept. 29, 2004", "G.R. No. 144159", "Callejo, Sr., J."),
        ("case-08-3-lazarte-v-sandiganbayan", "08.3. Lazarte v. Sandiganbayan", "Conspiracy Indictment & Sufficiency", "March 13, 2009", "G.R. No. 180122", "Tinga, J. (En Banc)"),
        ("case-08-4-serana-v-sandiganbayan", "08.4. Serana v. Sandiganbayan", "Sandiganbayan Jurisdiction (Student Regent)", "Jan. 22, 2008", "G.R. No. 162059", "Reyes, R.T., J."),
        ("case-08-5-go-v-sandiganbayan", "08.5. Go v. Sandiganbayan", "Private Co-Conspirators in Graft", "April 13, 2007", "G.R. No. 172602", "Callejo, Sr., J."),
        ("case-08-6-castro-v-people", "08.6. Castro v. People", "Finality of Acquittal & Prescription", "July 23, 2008", "G.R. No. 180832", "Corona, J."),
        ("case-08-7-people-v-asis", "08.7. People v. Asis", "Certiorari vs. Double Jeopardy", "August 25, 2010", "G.R. No. 173089", "Mendoza, J."),
        ("case-08-8-ivler-v-modesto-san-pedro", "08.8. Ivler v. Modesto-San Pedro", "Quasi-Crimes & Splitting Charges", "Nov. 17, 2010", "G.R. No. 172716", "Carpio, J."),
        ("case-08-9-nierras-v-dacucuy", "08.9. Nierras v. Dacuycuy", "Same Act vs Same Offense (BP 22 & Estafa)", "Jan. 11, 1990", "G.R. Nos. 59568-76", "Paras, J. (En Banc)"),
        ("case-08-10-people-v-lacson", "08.10. People v. Lacson", "Provisional Dismissal & Two-Year Bar", "April 1, 2003", "G.R. No. 149453", "Callejo, Sr., J. (En Banc)"),
    ]

    for idx, c_raw in enumerate(cases_raw):
        slug, short_title, topic_tag, date_str, gr_str, ponente_str = case_slugs[idx]
        clean_name = re.sub(r'^08\.\d+\.\s*', '', short_title).strip()
        case_toc_items.append((slug, f"{short_title} ({topic_tag})"))

        # Split into Outputs
        parts = re.split(r'\[OUTPUT \d+:[^\]]+\]', c_raw)
        header_part = parts[0].strip()
        out1_text = parts[1].strip()
        out2_text = parts[2].strip()
        out3_text = parts[3].strip()
        # Clean trailing separator from out3
        out3_text = re.sub(r'\n---.*', '', out3_text, flags=re.DOTALL).strip()

        # Parse Output 3 for sticky sidebar
        parties_m = re.search(r'\*\s*Parties\s*(?:\(and their contentions\))?:?\s*(.*?)(?=\*\s*Core Recitation Issue:|\Z)', out3_text, re.DOTALL | re.IGNORECASE)
        issue_m = re.search(r'\*\s*Core Recitation Issue:?\s*(.*?)(?=\*\s*Short Ruling & Ratio:|\Z)', out3_text, re.DOTALL | re.IGNORECASE)
        ruling_m = re.search(r'\*\s*Short Ruling & Ratio:?\s*(.*?)\Z', out3_text, re.DOTALL | re.IGNORECASE)

        parties_raw = parties_m.group(1).strip() if parties_m else ""
        issue_raw = issue_m.group(1).strip() if issue_m else ""
        ruling_raw = ruling_m.group(1).strip() if ruling_m else ""

        # Format parties in sidebar
        parties_html = parse_markdown_snippet(parties_raw)
        parties_html = highlight_legal_terms(parties_html)

        # Format issue in sidebar
        issue_html = parse_markdown_snippet(issue_raw)
        issue_html = highlight_legal_terms(issue_html)

        # Format ruling in sidebar
        ruling_html = parse_markdown_snippet(ruling_raw)
        ruling_html = highlight_legal_terms(ruling_html)

        # Extract Quick Bar Doctrine for matrix
        bar_doctrine_m = re.search(r'\*\s*Recitation Doctrine / Bar Takeaway:\s*([^\n]+(?:\n[^\*\n]+)*)', out2_text, re.IGNORECASE)
        bar_doctrine = bar_doctrine_m.group(1).strip().strip('"') if bar_doctrine_m else ""

        core_issue_m = re.search(r'\*\s*Core Recitation Issue:\s*([^\n]+(?:\n[^\*\n]+)*)', out2_text, re.IGNORECASE)
        core_issue = core_issue_m.group(1).strip().strip('"') if core_issue_m else issue_raw.strip('"')

        case_matrix_data.append({
            "num": f"08.{idx+1}",
            "title": short_title,
            "slug": slug,
            "citation": f"{gr_str} ({date_str})",
            "topic": topic_tag,
            "issue": core_issue[:160] + ("..." if len(core_issue) > 160 else ""),
            "doctrine": bar_doctrine[:220] + ("..." if len(bar_doctrine) > 220 else "")
        })

        # Process Output 1 Body Text (VERBATIM zero-word alteration)
        out1_proc = out1_text

        # Detect Trigger Words block
        tw_match = re.search(r'Trigger Words:\s*(.*?)(?=\n[A-Z][a-zA-Z\s]+:|\n\nFacts of the Case|\Z)', out1_proc, re.DOTALL)
        tw_html = ""
        if tw_match:
            tw_content = tw_match.group(1).strip()
            pills = []
            for line in tw_content.split('\n'):
                line = line.strip()
                if line.startswith('*'):
                    line = line.lstrip('*').strip()
                elif line.startswith('-'):
                    line = line.lstrip('-').strip()
                if line:
                    for sub in line.split(';'):
                        sub = sub.strip()
                        if sub:
                            pills.append(f'<span class="trigger-pill">{html.escape(sub)}</span>')
            if pills:
                tw_html = f'<div class="trigger-container"><span class="trigger-title">KEY TOPICS & TRIGGERS:</span> {" ".join(pills)}</div>'
            out1_proc = out1_proc[:tw_match.start()] + out1_proc[tw_match.end():]

        # Convert Dispositive portion into blockquote accurately
        disp_match = re.search(r'(\*?\s*Dispositive Portion:?\s*)(.*?)(?=\n\*?\s*Legal Analysis|\n\*?\s*Brief Answers|\n\n###|\Z)', out1_proc, re.DOTALL | re.IGNORECASE)
        if disp_match:
            disp_body = disp_match.group(2).strip()
            # Wrap lines in blockquote
            disp_quoted = f"\n\n##### Dispositive Portion\n\n<blockquote class=\"dispositive-quote\">\n\n{disp_body}\n\n</blockquote>\n\n"
            out1_proc = out1_proc[:disp_match.start()] + disp_quoted + out1_proc[disp_match.end():]

        # Enhance headings in out1
        out1_proc = enhance_out1_headings(out1_proc)

        # Convert markdown to html for out1
        out1_html = parse_markdown_snippet(out1_proc)
        out1_html = highlight_legal_terms(out1_html)

        # Enhance Output 2 (High-Yield Recitation Digest)
        out2_proc = enhance_out2_sections(out2_text)
        out2_html = parse_markdown_snippet(out2_proc)
        out2_html = highlight_legal_terms(out2_html)

        # Build full case section HTML
        section_html = f"""
    <!-- CASE {idx+1}: {short_title} -->
    <section class="case-section" id="{slug}">
      <div class="case-grid">
        <!-- LEFT COLUMN: Full Verbatim Case Content -->
        <div class="case-main">
          <div class="case-header-card">
            <div class="case-num-badge">CASE 08.{idx+1}</div>
            <h4 id="{slug}-title">{short_title}</h4>
            <div class="case-meta">
              <span class="c-burgundy"><strong>{clean_name}</strong></span> • 
              <span class="c-teal">{gr_str}</span> • 
              <span>{date_str}</span> • 
              <span class="c-navy">Ponente: {ponente_str}</span>
            </div>
          </div>

          {tw_html}

          <!-- OUTPUT 1: COMPREHENSIVE ACADEMIC DIGEST -->
          <div class="academic-digest">
            <div class="digest-section-label">OUTPUT 1: COMPREHENSIVE ACADEMIC DIGEST</div>
            {out1_html}
          </div>

          <!-- OUTPUT 2: HIGH-YIELD RECITATION DIGEST -->
          <div class="recitation-box">
            <div class="recitation-label">OUTPUT 2: HIGH-YIELD RECITATION DIGEST</div>
            {out2_html}
          </div>
        </div>

        <!-- RIGHT COLUMN: Contextual Sticky Snapshot Panel -->
        <aside class="case-sidebar">
          <div class="case-quick-card">
            <div class="quick-title">Quick Snapshot • {gr_str}</div>

            <div class="quick-group">
              <span class="quick-label label-parties">Parties & Contentions</span>
              <div class="quick-text">{parties_html}</div>
            </div>

            <div class="quick-group">
              <span class="quick-label label-issue">Core Recitation Issue</span>
              <div class="quick-text">{issue_html}</div>
            </div>

            <div class="quick-group">
              <span class="quick-label label-ruling">Short Ruling & Ratio</span>
              <div class="quick-text">{ruling_html}</div>
            </div>
          </div>
        </aside>
      </div>
    </section>
    """
        case_sections_html.append(section_html)

    return "\n".join(case_sections_html), case_toc_items, case_matrix_data

def build_full_html():
    raw_text = read_source()
    cases_html, toc_items, matrix_data = build_case_sections(raw_text)

    # Build TOC options
    toc_options_html = ['<option value="" disabled selected>Select topic or case...</option>']
    toc_options_html.append('<option value="#executive-overview">▪ I. Executive Overview & Procedural Flowchart</option>')
    toc_options_html.append('<option value="#core-doctrinal-pillars">▪ II. Four Doctrinal Pillars (Rule 116 & 117)</option>')
    toc_options_html.append('<option value="#statutory-comparison-matrix">▪ III. Master Landmark Jurisprudence Matrix</option>')
    toc_options_html.append('<option value="#cases-section-heading">▪ IV. Landmark Case Digests (Cases 08.1 – 08.10)</option>')

    for slug, label in toc_items:
        toc_options_html.append(f'<option value="#{slug}">&nbsp;&nbsp;↳ {html.escape(label)}</option>')

    # Build Matrix Table Rows
    matrix_rows = []
    for item in matrix_data:
        matrix_rows.append(f"""
        <tr>
          <td><a href="#{item['slug']}" class="matrix-link"><strong>{item['num']}</strong><br>{item['title']}</a></td>
          <td><span class="c-teal">{item['citation']}</span></td>
          <td><span class="topic-tag">{item['topic']}</span></td>
          <td class="matrix-issue">{item['issue']}</td>
          <td class="matrix-doctrine">{item['doctrine']}</td>
        </tr>
        """)
    matrix_table_html = "\n".join(matrix_rows)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Criminal Procedure: Rule 116 & Rule 117 Landmark Jurisprudence (Cases 08.1 – 08.10)</title>
  <style>
    :root {{
      --color-navy: #1E3A8A;
      --color-teal: #0F766E;
      --color-green: #166534;
      --color-burgundy: #991B1B;
      --color-rust: #C2410C;
      --color-text: #1F2937;
      --color-bg: #FFFFFF;
      --color-page-bg: #F8FAFC;
      --color-quote-bg: #FFF7ED;
      --color-sidebar-bg: #FFFFFF;
      --color-border: #E2E8F0;
      --nav-height: 54px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      line-height: 1.65;
      color: var(--color-text);
      background-color: var(--color-page-bg);
      margin: 0;
      padding: 0;
    }}

    /* STICKY TOP NAVIGATION BAR */
    .sticky-nav {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #1E3A8A;
      color: #FFFFFF;
      padding: 0.65rem 1.5rem;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
      height: var(--nav-height);
      display: flex;
      align-items: center;
    }}
    .nav-content {{
      max-width: 1240px;
      width: 100%;
      margin: 0 auto;
      display: flex;
      align-items: center;
      gap: 1rem;
    }}
    .nav-label {{
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      white-space: nowrap;
      text-transform: uppercase;
      color: #E2E8F0;
    }}
    .nav-dropdown {{
      flex-grow: 1;
      padding: 0.42rem 0.75rem;
      font-size: 0.85rem;
      font-weight: 500;
      border-radius: 6px;
      border: 1px solid #CBD5E1;
      background-color: #FFFFFF;
      color: #1F2937;
      outline: none;
      cursor: pointer;
    }}
    .nav-dropdown:focus {{
      border-color: #93C5FD;
      box-shadow: 0 0 0 2px rgba(147, 197, 253, 0.5);
    }}

    /* DOCUMENT CONTAINER */
    .document-container {{
      max-width: 1240px;
      margin: 2rem auto 4rem auto;
      background: #FFFFFF;
      padding: 2.5rem 3rem;
      border-radius: 10px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
    }}

    /* HEADINGS & SCROLL MARGINS */
    h1, h2, h3, h4, h5, h6 {{
      scroll-margin-top: calc(var(--nav-height) + 1.25rem);
    }}
    h1 {{
      color: var(--color-navy);
      font-size: 1.85rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: -0.01em;
      margin-top: 0;
      margin-bottom: 0.5rem;
      padding-bottom: 0.75rem;
      border-bottom: 3px solid var(--color-navy);
    }}
    .doc-subtitle {{
      font-size: 1.05rem;
      color: #64748B;
      font-weight: 500;
      margin-bottom: 2rem;
    }}
    h2 {{
      color: var(--color-navy);
      font-size: 1.45rem;
      font-weight: 700;
      margin-top: 2.5rem;
      margin-bottom: 1rem;
      border-bottom: 2px solid #E2E8F0;
      padding-bottom: 0.4rem;
    }}
    h3 {{
      color: var(--color-navy);
      font-size: 1.25rem;
      font-weight: 700;
      margin-top: 2rem;
      margin-bottom: 0.75rem;
    }}
    h4 {{
      color: var(--color-navy);
      font-size: 1.15rem;
      font-weight: 700;
      margin-top: 1.25rem;
      margin-bottom: 0.5rem;
    }}
    h5 {{
      color: var(--color-navy);
      font-size: 1.02rem;
      font-weight: 700;
      margin-top: 1.4rem;
      margin-bottom: 0.4rem;
      padding-bottom: 0.2rem;
      border-bottom: 1px solid #E2E8F0;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    h6 {{
      color: #334155;
      font-size: 0.95rem;
      font-weight: 700;
      margin-top: 1.1rem;
      margin-bottom: 0.35rem;
    }}
    hr {{
      border: 0;
      height: 1px;
      background-color: var(--color-border);
      margin: 2.25rem 0;
    }}
    p {{
      margin: 0.75rem 0;
    }}
    ul, ol {{
      margin: 0.5rem 0 0.75rem 1.35rem;
      padding: 0;
    }}
    li {{
      margin-bottom: 0.4rem;
    }}
    blockquote, .dispositive-quote {{
      border-left: 4px solid var(--color-burgundy);
      margin: 1.25rem 0;
      padding: 0.85rem 1.25rem;
      background: var(--color-quote-bg);
      font-style: italic;
      color: #451A03;
      border-radius: 0 8px 8px 0;
    }}

    /* COLOR PALETTE CLASSES */
    .c-navy {{ color: var(--color-navy); }}
    .c-teal {{ color: var(--color-teal); }}
    .c-green {{ color: var(--color-green); }}
    .c-burgundy {{ color: var(--color-burgundy); }}
    .c-rust {{ color: var(--color-rust); }}

    /* TRIGGER WORDS TAGS */
    .trigger-container {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.45rem;
      margin: 0.85rem 0 1.25rem 0;
      padding: 0.75rem 1rem;
      background: #F1F5F9;
      border-radius: 6px;
      border: 1px solid #E2E8F0;
    }}
    .trigger-title {{
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--color-navy);
      letter-spacing: 0.05em;
      margin-right: 0.25rem;
    }}
    .trigger-pill {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 600;
      color: #1E3A8A;
      background: #E0E7FF;
      padding: 0.2rem 0.55rem;
      border-radius: 9999px;
      border: 1px solid #C7D2FE;
    }}

    /* EXECUTIVE UI SUMMARY CARDS */
    .ui-box {{
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 1.5rem;
      margin: 1.75rem 0;
      background: #FFFFFF;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    }}
    .ui-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.25rem;
    }}
    .ui-col {{
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      padding: 1rem;
      background: #F8FAFC;
      border-radius: 8px;
      border: 1px solid #E2E8F0;
    }}
    .ui-icon {{
      font-size: 1.75rem;
      margin-bottom: 0.4rem;
    }}
    .ui-kicker {{
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--color-navy);
      margin-bottom: 0.25rem;
    }}
    .ui-title {{
      font-size: 1rem;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 0.25rem;
    }}
    .ui-sub {{
      font-size: 0.84rem;
      color: #64748B;
      line-height: 1.4;
    }}

    /* STATUTORY COMPARISON TABLE */
    .ui-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      font-size: 0.88rem;
      line-height: 1.5;
    }}
    .ui-table th {{
      text-align: left;
      font-weight: 700;
      color: var(--color-navy);
      background-color: #F1F5F9;
      padding: 0.75rem 0.85rem;
      border-bottom: 2px solid #CBD5E1;
      border-top: 1px solid #E2E8F0;
    }}
    .ui-table td {{
      padding: 0.75rem 0.85rem;
      border-bottom: 1px solid #E2E8F0;
      vertical-align: top;
      color: #334155;
    }}
    .ui-table tr:hover td {{
      background-color: #F8FAFC;
    }}
    .matrix-link {{
      color: var(--color-navy);
      text-decoration: none;
    }}
    .matrix-link:hover {{
      text-decoration: underline;
    }}
    .topic-tag {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      background: #E0F2FE;
      color: #0369A1;
    }}
    .matrix-issue {{
      font-size: 0.82rem;
      color: #475569;
    }}
    .matrix-doctrine {{
      font-size: 0.82rem;
      color: #1E293B;
      font-weight: 500;
    }}

    /* DUAL-COLUMN CASE GRID & STICKY PANEL */
    .case-section {{
      margin: 2.75rem 0;
      padding-top: 1.5rem;
      padding-bottom: 2.5rem;
      border-bottom: 2px dashed #E2E8F0;
    }}
    .case-section:last-of-type {{
      border-bottom: none;
    }}
    .case-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 350px;
      gap: 2.25rem;
      align-items: start;
    }}
    .case-main {{
      min-width: 0;
    }}
    .case-header-card {{
      background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
      border: 1px solid #CBD5E1;
      border-left: 5px solid var(--color-navy);
      border-radius: 8px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.25rem;
    }}
    .case-num-badge {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background: var(--color-navy);
      color: #FFFFFF;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
      margin-bottom: 0.5rem;
    }}
    .case-header-card h4 {{
      margin: 0.25rem 0 0.5rem 0;
      font-size: 1.3rem;
      color: var(--color-navy);
    }}
    .case-meta {{
      font-size: 0.85rem;
      color: #64748B;
    }}
    .digest-section-label {{
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #475569;
      background: #F1F5F9;
      padding: 0.3rem 0.75rem;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 1rem;
      margin-top: 1.5rem;
    }}
    .academic-digest {{
      margin-bottom: 2rem;
    }}
    .recitation-box {{
      background: #FAFAF9;
      border: 1px solid #E7E5E4;
      border-top: 4px solid var(--color-teal);
      border-radius: 8px;
      padding: 1.5rem;
      margin-top: 2rem;
    }}
    .recitation-label {{
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--color-teal);
      margin-bottom: 1rem;
      display: inline-block;
    }}
    .recit-issue-box {{
      background: #FEF3C7;
      border: 1px solid #FDE68A;
      border-left: 4px solid #D97706;
      border-radius: 6px;
      padding: 0.85rem 1.15rem;
      margin: 1rem 0;
    }}
    .recit-issue-label {{
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #92400E;
      display: block;
      margin-bottom: 0.25rem;
    }}
    .recit-issue-text {{
      font-size: 0.95rem;
      font-weight: 600;
      color: #78350F;
      font-style: italic;
    }}
    .doctrine-card {{
      background: #ECFDF5;
      border: 1.5px solid #A7F3D0;
      border-left: 5px solid var(--color-green);
      border-radius: 8px;
      padding: 1.15rem 1.35rem;
      margin: 1.25rem 0;
    }}
    .doctrine-header {{
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      color: var(--color-green);
      margin-bottom: 0.4rem;
    }}
    .doctrine-body {{
      font-size: 0.95rem;
      font-weight: 600;
      color: #064E3B;
      line-height: 1.5;
    }}

    /* STICKY RIGHT SIDEBAR SNAPSHOT PANEL */
    .case-sidebar {{
      position: sticky;
      top: calc(var(--nav-height) + 1.25rem);
    }}
    .case-quick-card {{
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      border-top: 4px solid var(--color-navy);
      border-radius: 8px;
      padding: 1.15rem 1.25rem;
      font-size: 0.83rem;
      line-height: 1.48;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.06);
    }}
    .quick-title {{
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--color-navy);
      margin-bottom: 0.85rem;
      padding-bottom: 0.4rem;
      border-bottom: 1.5px solid #E2E8F0;
    }}
    .quick-group {{
      margin-bottom: 0.85rem;
    }}
    .quick-group:last-child {{
      margin-bottom: 0;
    }}
    .quick-label {{
      display: inline-block;
      font-size: 0.68rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 2px 6px;
      border-radius: 4px;
      margin-bottom: 0.35rem;
    }}
    .label-parties {{ background: #E0E7FF; color: var(--color-navy); }}
    .label-issue {{ background: #FEF3C7; color: #92400E; }}
    .label-ruling {{ background: #DCFCE7; color: var(--color-green); }}
    .quick-text {{
      color: #334155;
    }}
    .quick-text p {{
      margin: 0.35rem 0;
    }}
    .quick-text ul {{
      margin: 0.25rem 0 0.5rem 1.1rem;
      padding: 0;
    }}
    .quick-text li {{
      margin-bottom: 0.3rem;
    }}

    /* INTERACTIVE DIAGRAM WRAPPER, PAN-ZOOM & FULLSCREEN */
    .diagram-wrapper {{
      margin: 2rem 0;
      border: 1px solid #CBD5E1;
      border-radius: 8px;
      background: #FFFFFF;
      overflow: hidden;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    .diagram-wrapper.is-fullscreen {{
      position: fixed;
      inset: 0;
      z-index: 9999;
      margin: 0;
      border: none;
      border-radius: 0;
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
      background: #FFFFFF;
    }}
    .diagram-toolbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #F8FAFC;
      padding: 0.5rem 1rem;
      border-bottom: 1px solid #E2E8F0;
      z-index: 2;
    }}
    .diagram-label {{
      font-size: 0.75rem;
      font-weight: 700;
      color: #1E3A8A;
      letter-spacing: 0.05em;
    }}
    .diagram-hint {{
      font-weight: 400;
      color: #64748B;
      font-size: 0.7rem;
      margin-left: 0.4rem;
    }}
    .diagram-controls {{
      display: flex;
      gap: 0.35rem;
    }}
    .zoom-btn {{
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      border-radius: 4px;
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.9rem;
      font-weight: 700;
      color: #334155;
      cursor: pointer;
      user-select: none;
      transition: background 0.15s, border-color 0.15s;
    }}
    .zoom-btn:hover {{
      background: #F1F5F9;
      border-color: #94A3B8;
      color: #0F172A;
    }}
    .diagram-viewport {{
      position: relative;
      overflow: hidden;
      background: #F8FAFC;
      min-height: 480px;
      cursor: grab;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .diagram-wrapper.is-fullscreen .diagram-viewport {{
      flex-grow: 1;
      height: calc(100vh - 45px);
    }}
    .diagram-viewport.is-dragging {{
      cursor: grabbing;
    }}
    .diagram-container {{
      transform-origin: center center;
      transition: transform 0.05s ease-out;
      padding: 1.5rem;
      display: inline-block;
    }}

    /* RESPONSIVE LAYOUT */
    @media (max-width: 960px) {{
      .document-container {{ padding: 1.5rem 1.25rem; margin: 1rem auto; }}
      .case-grid {{ grid-template-columns: 1fr; gap: 1.5rem; }}
      .case-sidebar {{ position: static; }}
      .nav-label {{ display: none; }}
      .ui-grid {{ grid-template-columns: 1fr; }}
      .ui-table {{ font-size: 0.8rem; }}
    }}
    @media print {{
      .sticky-nav {{ display: none !important; }}
      body {{ background: #FFF; padding: 0; }}
      .document-container {{ box-shadow: none; padding: 0; max-width: 100%; margin: 0; }}
      .case-grid {{ display: block; }}
      .case-sidebar {{ position: static; margin-top: 1.5rem; page-break-inside: avoid; }}
      .diagram-wrapper {{ page-break-inside: avoid; }}
    }}
  </style>
</head>
<body>

  <!-- STICKY TOP NAVIGATION BAR -->
  <nav class="sticky-nav">
    <div class="nav-content">
      <span class="nav-label">TOPIC NAVIGATION:</span>
      <select id="toc-select" class="nav-dropdown" onchange="if(this.value) {{ document.querySelector(this.value).scrollIntoView({{behavior: 'smooth'}}); }}">
        {' '.join(toc_options_html)}
      </select>
    </div>
  </nav>

  <div class="document-container">
    <h1>Criminal Procedure: Rule 116 & Rule 117 Landmark Jurisprudence</h1>
    <div class="doc-subtitle">Comprehensive Academic Digests, High-Yield Recitation Briefs & Strategic Snapshot Panels (Cases 08.1 – 08.10)</div>

    <!-- SECTION I: EXECUTIVE OVERVIEW & PROCEDURAL FLOWCHART -->
    <h3 id="executive-overview">I. Executive Overview & Procedural Architecture</h3>
    <p>
      This master reviewer packages the ten landmark Supreme Court decisions governing <span class="c-teal"><strong>Rule 116 (Arraignment and Plea)</strong></span> and <span class="c-teal"><strong>Rule 117 (Motion to Quash, Double Jeopardy & Provisional Dismissal)</strong></span> of the Revised Rules of Criminal Procedure. The decisions establish the constitutional boundaries of plea bargaining, trial court jurisdiction, summary pre-trial acquittals, due process rights of the State, and the statutory requirements of double jeopardy and provisional dismissal.
    </p>

    <!-- INTERACTIVE PAN-AND-ZOOM MERMAID DIAGRAM -->
    <div class="diagram-wrapper">
      <div class="diagram-toolbar">
        <span class="diagram-label">PROCEDURAL DECISION ARCHITECTURE: RULES 116 & 117 <span class="diagram-hint">(Drag to pan • Scroll to zoom • ⛶ for Fullscreen)</span></span>
        <div class="diagram-controls">
          <button type="button" class="zoom-btn" onclick="zoomDiagram(this, 0.25)" title="Zoom In">+</button>
          <button type="button" class="zoom-btn" onclick="zoomDiagram(this, -0.25)" title="Zoom Out">−</button>
          <button type="button" class="zoom-btn" onclick="resetDiagramZoom(this)" title="Reset & Center">↺</button>
          <button type="button" class="zoom-btn fullscreen-btn" onclick="toggleDiagramFullscreen(this)" title="View Fullscreen">⛶</button>
        </div>
      </div>
      <div class="diagram-viewport">
        <div class="diagram-container">
          <pre class="mermaid">
flowchart TD
  START(["CRIMINAL INFORMATION FILED"]) --> ARRN["Arraignment & Plea (Rule 116)"]

  %% Rule 116 branch
  ARRN --> PLEA{{"Type of Plea Entered?"}}
  PLEA -- "Conditional Plea for Reduced Penalty" --> MAGAT["People v. Magat<br/>• Unauthorized under Sec. 2, Rule 116<br/>• Treated as Plea of Not Guilty<br/>• Conviction void ab initio; no double jeopardy"]
  PLEA -- "Plea of Not Guilty" --> MTQ_STAGE{{"Motion to Quash (Rule 117) Filed?"}}

  %% Motion to Quash Branch
  MTQ_STAGE -- "Grounded on Absence of Probable Cause" --> ALBA["People v. Sandiganbayan (Alba)<br/>• Lack of PC is NOT a ground under Sec. 3<br/>• Summary acquittal denies State due process<br/>• Order is void; jeopardy does not attach"]
  MTQ_STAGE -- "Failure to Charge an Offense (Sec. 3[a])" --> TEST{{"Hypothetical Admission Test"}}

  TEST -- "Conspiracy as Mode of Commission" --> LAZARTE["Lazarte v. Sandiganbayan<br/>• Ultimate facts & community of design suffice<br/>• Specific overt acts are evidentiary for trial"]
  TEST -- "Private Co-Conspirator in Sec. 3(g) Graft" --> GO["Go v. Sandiganbayan<br/>• Private persons liable under conspiracy<br/>• Sec. 3(a) defense never waived (Sec. 9)"]

  MTQ_STAGE -- "Lack of Jurisdiction (Sec. 3[b])" --> SERANA["Serana v. Sandiganbayan<br/>• Sandiganbayan covers Estafa in relation to office<br/>• UP Student Regent is a public officer<br/>• Source of funds is an evidentiary defense"]

  %% Trial & Verdict Branch
  MTQ_STAGE -- "Motion Denied / Proceed to Trial" --> TRIAL["Trial on the Merits"]
  TRIAL --> VERDICT{{"Trial Court Verdict"}}

  VERDICT -- "Acquittal / Conviction for Lesser Offense" --> FINALITY["Finality-of-Acquittal Rule"]
  FINALITY -- "Factual Misappreciation / Error of Judgment" --> CASTRO["Castro v. People & People v. Asis<br/>• Certiorari cannot review evidentiary findings<br/>• Double jeopardy strictly protects acquittal"]
  FINALITY -- "Sham Trial / Deprivation of Due Process" --> GALMAN["Galman Exception<br/>• Ouster of jurisdiction; void decree<br/>• Double jeopardy inapplicable"]

  %% Quasi-Crimes & BP 22 vs Estafa
  ARRN --> SPLIT{{"Special Double Jeopardy Indictments"}}
  SPLIT -- "Quasi-Crimes (Art. 365, RPC)" --> IVLER["Ivler v. Modesto-San Pedro<br/>• Reckless imprudence is a single offense<br/>• Splitting charges prohibited<br/>• Prior conviction bars subsequent prosecution"]
  SPLIT -- "Bouncing Checks (BP 22 vs Estafa)" --> NIERRAS["Nierras v. Dacuycuy<br/>• Same ACT, distinct OFFENSES<br/>• BP 22 (public interest) vs Estafa (property)<br/>• Simultaneous prosecution valid"]

  %% Provisional Dismissal
  TRIAL --> PROV_DISM{{"Provisional Dismissal (Sec. 8, Rule 117)"}}
  PROV_DISM --> REQ{{"Conditions Sine Qua Non"}}
  REQ -- "Express Consent + Notice to Offended Parties" --> TIME_BAR["People v. Lacson<br/>• 2-year time-bar renders dismissal permanent<br/>• Reckoned PROSPECTIVELY from Dec 1, 2000"]
  REQ -- "Defective (No consent / No notice to all heirs)" --> NO_BAR["Dismissal not under Sec. 8<br/>• Time-bar does not attach<br/>• Refiling of Information valid"]

  classDef navyNode fill:#EFF6FF,stroke:#1E3A8A,stroke-width:2px,color:#1E3A8A;
  classDef tealNode fill:#F0FDFA,stroke:#0F766E,stroke-width:2px,color:#0F766E;
  classDef greenNode fill:#ECFDF5,stroke:#166534,stroke-width:2px,color:#166534;
  classDef rustNode fill:#FFF7ED,stroke:#C2410C,stroke-width:2px,color:#C2410C;

  class START,ARRN,TRIAL navyNode;
  class MAGAT,ALBA,CASTRO,GALMAN,IVLER,NO_BAR rustNode;
  class LAZARTE,GO,SERANA,NIERRAS tealNode;
  class FINALITY,TIME_BAR greenNode;
          </pre>
        </div>
      </div>
    </div>

    <!-- SECTION II: CORE DOCTRINAL PILLARS -->
    <h3 id="core-doctrinal-pillars">II. Four Doctrinal Pillars of Rules 116 & 117</h3>
    <div class="ui-box">
      <div class="ui-grid">
        <div class="ui-col">
          <div class="ui-icon">⚖️</div>
          <div class="ui-kicker">RULE 116: PLEAS</div>
          <div class="ui-title">Unconditional Pleas</div>
          <div class="ui-sub"><span class="c-burgundy"><em>People v. Magat</em></span>: Plea bargaining solely for penalty is void ab initio; treated as plea of not guilty; no double jeopardy attaches.</div>
        </div>
        <div class="ui-col">
          <div class="ui-icon">🛡️</div>
          <div class="ui-kicker">RULE 117: QUASHAL</div>
          <div class="ui-title">Exclusive Grounds</div>
          <div class="ui-sub"><span class="c-burgundy"><em>People v. Sandiganbayan, Lazarte, Go, Serana</em></span>: Lack of PC not a ground; hypothetical admission tests face of Information; GOCC managers & private co-conspirators covered.</div>
        </div>
        <div class="ui-col">
          <div class="ui-icon">🔁</div>
          <div class="ui-kicker">RULE 117: JEOPARDY</div>
          <div class="ui-title">Finality of Acquittal</div>
          <div class="ui-sub"><span class="c-burgundy"><em>Castro, Asis, Ivler, Nierras</em></span>: Errors of judgment unassailable by certiorari; quasi-crimes cannot be split; distinct crimes from same act allowed.</div>
        </div>
        <div class="ui-col">
          <div class="ui-icon">⏱️</div>
          <div class="ui-kicker">RULE 117: SEC. 8</div>
          <div class="ui-title">Provisional Dismissal</div>
          <div class="ui-sub"><span class="c-burgundy"><em>People v. Lacson</em></span>: Strict conditions sine qua non (express consent + notice); prospective application of 2-year bar from Dec 1, 2000.</div>
        </div>
      </div>
    </div>

    <!-- SECTION III: MASTER COMPARISON MATRIX -->
    <h3 id="statutory-comparison-matrix">III. Master Landmark Jurisprudence Matrix</h3>
    <p>Quick lookup matrix cross-referencing all 10 cases, citations, core issues, and governing bar doctrines:</p>

    <div style="overflow-x: auto;">
      <table class="ui-table">
        <thead>
          <tr>
            <th style="width: 14%;">Case Title</th>
            <th style="width: 15%;">Citation & Date</th>
            <th style="width: 14%;">Subject & Rule</th>
            <th style="width: 25%;">Core Issue</th>
            <th style="width: 32%;">Recitation / Bar Doctrine</th>
          </tr>
        </thead>
        <tbody>
          {matrix_table_html}
        </tbody>
      </table>
    </div>

    <hr>

    <!-- SECTION IV: LANDMARK CASE DIGESTS -->
    <h2 id="cases-section-heading">IV. Landmark Case Digests: Rules 116 & 117</h2>

    {cases_html}

  </div>

  <!-- MERMAID SCRIPT & PAN/ZOOM/FULLSCREEN ENGINE -->
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'base',
      themeVariables: {{
        primaryColor: '#F8FAFC',
        primaryBorderColor: '#1E3A8A',
        primaryTextColor: '#1F2937',
        lineColor: '#1E3A8A',
        fontFamily: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif'
      }}
    }});
  </script>

  <script>
    // Grab-to-Pan & Zoom Handlers
    function updateDiagramTransform(container) {{
      const scale = parseFloat(container.dataset.scale || '1');
      const x = parseFloat(container.dataset.panX || '0');
      const y = parseFloat(container.dataset.panY || '0');
      container.style.transform = `translate(${{x}}px, ${{y}}px) scale(${{scale}})`;
    }}

    function zoomDiagram(btn, delta) {{
      const container = btn.closest('.diagram-wrapper').querySelector('.diagram-container');
      let scale = parseFloat(container.dataset.scale || '1');
      scale = Math.min(Math.max(0.3, +(scale + delta).toFixed(2)), 5.0);
      container.dataset.scale = scale;
      updateDiagramTransform(container);
    }}

    function resetDiagramZoom(btn) {{
      const container = btn.closest('.diagram-wrapper').querySelector('.diagram-container');
      container.dataset.scale = '1';
      container.dataset.panX = '0';
      container.dataset.panY = '0';
      updateDiagramTransform(container);
    }}

    function toggleDiagramFullscreen(btn) {{
      const wrapper = btn.closest('.diagram-wrapper');
      const container = wrapper.querySelector('.diagram-container');
      const enteringFullscreen = !wrapper.classList.contains('is-fullscreen');

      wrapper.classList.toggle('is-fullscreen', enteringFullscreen);
      btn.textContent = enteringFullscreen ? '✕' : '⛶';
      btn.title = enteringFullscreen ? 'Exit Fullscreen (Esc)' : 'View Fullscreen';
      document.body.style.overflow = enteringFullscreen ? 'hidden' : '';

      if (container) {{
        container.dataset.panX = '0';
        container.dataset.panY = '0';
        updateDiagramTransform(container);
      }}

      if (enteringFullscreen && wrapper.requestFullscreen) {{
        wrapper.requestFullscreen().catch(() => {{}});
      }} else if (!enteringFullscreen && document.fullscreenElement) {{
        document.exitFullscreen().catch(() => {{}});
      }}
    }}

    function exitAllDiagramFullscreens() {{
      document.querySelectorAll('.diagram-wrapper.is-fullscreen').forEach(wrapper => {{
        wrapper.classList.remove('is-fullscreen');
        const container = wrapper.querySelector('.diagram-container');
        if (container) {{
          container.dataset.panX = '0';
          container.dataset.panY = '0';
          updateDiagramTransform(container);
        }}
        const btn = wrapper.querySelector('.fullscreen-btn');
        if (btn) {{
          btn.textContent = '⛶';
          btn.title = 'View Fullscreen';
        }}
      }});
      document.body.style.overflow = '';
    }}

    document.addEventListener('fullscreenchange', () => {{
      if (!document.fullscreenElement) {{
        exitAllDiagramFullscreens();
      }}
    }});

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') {{
        exitAllDiagramFullscreens();
      }}
    }});

    // Drag to Pan
    let activeDiagramDrag = null;

    document.addEventListener('mousedown', (e) => {{
      const viewport = e.target.closest('.diagram-viewport');
      if (!viewport || e.button !== 0) return;
      const container = viewport.querySelector('.diagram-container');
      if (!container) return;
      e.preventDefault();
      viewport.classList.add('is-dragging');
      activeDiagramDrag = {{
        viewport,
        container,
        startX: e.clientX - parseFloat(container.dataset.panX || '0'),
        startY: e.clientY - parseFloat(container.dataset.panY || '0')
      }};
    }});

    document.addEventListener('mousemove', (e) => {{
      if (!activeDiagramDrag) return;
      activeDiagramDrag.container.dataset.panX = e.clientX - activeDiagramDrag.startX;
      activeDiagramDrag.container.dataset.panY = e.clientY - activeDiagramDrag.startY;
      updateDiagramTransform(activeDiagramDrag.container);
    }});

    document.addEventListener('mouseup', () => {{
      if (!activeDiagramDrag) return;
      activeDiagramDrag.viewport.classList.remove('is-dragging');
      activeDiagramDrag = null;
    }});

    // Wheel Zoom inside Viewport
    document.addEventListener('wheel', (e) => {{
      const viewport = e.target.closest('.diagram-viewport');
      if (!viewport) return;
      const wrapper = viewport.closest('.diagram-wrapper');
      if (wrapper.classList.contains('is-fullscreen') || e.ctrlKey || e.metaKey) {{
        e.preventDefault();
        const container = viewport.querySelector('.diagram-container');
        let scale = parseFloat(container.dataset.scale || '1');
        const delta = e.deltaY < 0 ? 0.15 : -0.15;
        scale = Math.min(Math.max(0.3, +(scale + delta).toFixed(2)), 5.0);
        container.dataset.scale = scale;
        updateDiagramTransform(container);
      }}
    }}, {{ passive: false }});

    // Active Scroll-Spy for Sticky Navigation Dropdown
    document.addEventListener('DOMContentLoaded', () => {{
      const select = document.getElementById('toc-select');
      const watchedTargets = document.querySelectorAll(
        '#executive-overview, #core-doctrinal-pillars, #statutory-comparison-matrix, #cases-section-heading, .case-section'
      );

      const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            const id = entry.target.id;
            const matchingOption = select.querySelector(`option[value="#${{id}}"]`);
            if (matchingOption) {{
              select.value = '#' + id;
            }}
          }}
        }});
      }}, {{ rootMargin: '0px 0px -70% 0px' }});

      watchedTargets.forEach(target => observer.observe(target));
    }});
  </script>
</body>
</html>"""

    with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Successfully generated: {OUTPUT_HTML_PATH}")

if __name__ == "__main__":
    build_full_html()
