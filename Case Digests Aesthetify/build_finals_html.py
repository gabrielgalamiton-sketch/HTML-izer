import re
import html
import markdown
import os

INPUT_MD_PATH = r"H:\My Drive\JD 2 - Crim Pro - Cases + Ext - Finals (Combined).md"
SUPP_MD_PATH = r"c:\Users\IP Gaming 3\Desktop\HTML-izer\Case Digests Aesthetify\supplemental_quiz_cases.md"
OUTPUT_HTML_PATH = r"c:\Users\IP Gaming 3\Desktop\HTML-izer\Crim-Pro-Finals-Cases-06-07-08-Consolidated.html"

def read_source():
    with open(INPUT_MD_PATH, "r", encoding="utf-8") as f:
        base = f.read()
    with open(SUPP_MD_PATH, "r", encoding="utf-8") as f:
        supp = f.read()
    return base.rstrip() + "\n\n" + supp.lstrip()

def highlight_legal_terms(text):
    statute_patterns = [
        (r'\b(Rule\s+\d+(?:,\s*Section\s+[\d\(\)a-zA-Z]+)?)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Section\s+[\d\(\)a-zA-Z]+(?:,\s*Rule\s+\d+)?)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Article\s+\d+(?:,\s*paragraph\s+[\d\(\)a-zA-Z]+)?(?:\s+of\s+the\s+Revised\s+Penal\s+Code)?)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Republic\s+Act\s+(?:No\.\s*)?\d+|R\.A\.\s+No\.\s*\d+|RA\s+\d+)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Presidential\s+Decree\s+(?:No\.\s*)?\d+|P\.D\.\s+No\.\s*\d+)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(Batas\s+Pambansa\s+Blg\.\s*\d+|B\.P\.\s+Blg\.\s*\d+|BP\s+22)\b', r'<span class="c-teal"><strong>\1</strong></span>'),
        (r'\b(G\.R\.\s+Nos?\.\s*[\d\-,]+)\b', r'<span class="c-teal">\1</span>'),
        (r'\b(A\.M\.\s+No\.\s*[A-Z0-9\-\_]+)\b', r'<span class="c-teal">\1</span>'),
    ]
    for pat, repl in statute_patterns:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)

    rust_patterns = [
        (r'\b(void\s+ab\s+initio)\b', r'<span class="c-rust"><strong><u>\1</u></strong></span>'),
        (r'\b(ousted\s+of\s+jurisdiction)\b', r'<span class="c-rust"><strong><u>\1</u></strong></span>'),
        (r'\b(denial\s+of\s+due\s+process|denied\s+the\s+State\s+due\s+process|deprived\s+the\s+prosecution\s+of\s+due\s+process)\b', r'<span class="c-rust"><strong><u>\1</u></strong></span>'),
        (r'\b(fatal\s+defect|fatally\s+defective)\b', r'<span class="c-rust"><strong><u>\1</u></strong></span>'),
        (r'\b(improvident\s+plea)\b', r'<span class="c-rust"><strong>\1</strong></span>'),
    ]
    for pat, repl in rust_patterns:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)

    green_patterns = [
        (r'\b(double\s+jeopardy)\b', r'<span class="c-green"><strong>\1</strong></span>'),
        (r'\b(hypothetical\s+admission\s+test|hypothetical\s+admission\s+rule)\b', r'<span class="c-green"><strong><u>\1</u></strong></span>'),
        (r'\b(finality-of-acquittal\s+rule|finality-of-acquittal\s+doctrine)\b', r'<span class="c-green"><strong><u>\1</u></strong></span>'),
        (r'\b(conditions\s+sine\s+qua\s+non)\b', r'<span class="c-green"><strong><u>\1</u></strong></span>'),
        (r'\b(searching\s+inquiry\s+requirement|searching\s+inquiry)\b', r'<span class="c-green"><strong><u>\1</u></strong></span>'),
        (r'\b(two-year\s+time-bar|time-bar)\b', r'<span class="c-green"><strong>\1</strong></span>'),
        (r'\b(corpus\s+delicti)\b', r'<span class="c-green"><strong><em>\1</em></strong></span>'),
        (r'\b(chain\s+of\s+custody)\b', r'<span class="c-green"><strong>\1</strong></span>'),
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
        t = re.sub(rf'(?m)^(\*?\s*(?:\*\*)?{re.escape(h)}:?(?:\*\*)?\s*)$', rf'\n\n##### {h}\n\n', t)
        t = re.sub(rf'(?m)^(\*?\s*(?:\*\*)?{re.escape(h)}:(?:\*\*)?\s*)([^\n]+)', rf'\n\n##### {h}\n\n\2', t)

    sub_headers = [
        r'1\.\s+(?:\*\*)?Statutory\s*/\s*Rule\s+Breakdown',
        r'2\.\s+(?:\*\*)?Substantive\s*/\s*Procedural\s+Requirements',
        r'3\.\s+(?:\*\*)?Judicial\s+Doctrines\s+Applied',
        r'4\.\s+(?:\*\*)?Legal\s+Consequence\s*/\s*Relief(?:\s*/\s*Damages)?',
        r'On\s+Custody\s+of\s+the\s+Law\s+and\s+Jurisdiction\s+over\s+the\s+Person',
        r"On\s+Judge\s+Anghad's\s+Grave\s+Abuse\s+of\s+Discretion",
        r'On\s+Double\s+Jeopardy\s+and\s+Venue\s+Transfer',
        r'Unconditional\s+Nature\s+of\s+the\s+Plea',
        r'Reception\s+of\s+Evidence\s+upon\s+a\s+Plea\s+of\s+Guilty\s+to\s+a\s+Capital\s+Offense',
        r'Admissibility\s+of\s+the\s+Extrajudicial\s+Confession',
        r'Disallowance\s+of\s+Disproven\s+Aggravating\s+Circumstances',
        r'On\s+the\s+Effect\s+of\s+Self-Defense\s+Testimony\s+on\s+a\s+Plea\s+of\s+Guilty',
        r'On\s+the\s+Issue\s+of\s+Double\s+Jeopardy',
        r'Primary\s+Issue:\s*Double\s+Jeopardy\s+and\s+Identity\s+of\s+Offenses',
        r'Secondary\s+Issue:\s*Propriety\s+of\s+Certiorari\s+to\s+Challenge\s+Denial\s+of\s+Motion\s+to\s+Quash',
        r'Absence\s+of\s+Conditions\s+Sine\s+Qua\s+Non\s+Under\s+Section\s+8,\s+Rule\s+117',
        r'Prospective\s+Application\s+of\s+the\s+Two-Year\s+Time-Bar',
        r'On\s+Issue\s+1:\s*Lack\s+of\s+Probable\s+Cause\s+is\s+Not\s+a\s+Ground\s+to\s+Quash',
        r'On\s+Issue\s+2:\s*Nullity\s+of\s+Summary\s+Pre-Trial\s+Acquittal',
    ]
    for sh in sub_headers:
        t = re.sub(rf'(?m)^\s*(\*?\s*{sh}(?:\*\*)?:?(?:\*\*)?\s*)$', lambda m: f"\n\n###### {m.group(1).lstrip('* ').replace('**', '').strip().rstrip(':').strip()}\n\n", t)
        t = re.sub(rf'(?m)^\s*(\*?\s*{sh}(?:\*\*)?:(?:\*\*)?\s*)([^\n]+)', lambda m: f"\n\n###### {m.group(1).lstrip('* ').replace('**', '').strip().rstrip(':').strip()}\n\n{m.group(2)}", t)

    return t

def enhance_out2_sections(t):
    # Recitation Doctrine / Bar Takeaway
    doc_m = re.search(r'(\*\s*(?:\*\*)?Recitation Doctrine / Bar Takeaway:(?:\*\*)?\s*)(.*)', t, re.DOTALL | re.IGNORECASE)
    if doc_m:
        doc_body = doc_m.group(2).strip()
        if doc_body.startswith('*') and doc_body.endswith('*') and not doc_body.startswith('**'):
            doc_body = f"<em>{doc_body[1:-1]}</em>"
        doc_boxed = f'\n\n<div class="doctrine-card"><div class="doctrine-header">🎯 RECITATION DOCTRINE & BAR TAKEAWAY</div><div class="doctrine-body">{doc_body}</div></div>\n\n'
        t = t[:doc_m.start()] + doc_boxed

    # Core Recitation Issue
    issue_m = re.search(r'(\*\s*(?:\*\*)?Core Recitation Issue:(?:\*\*)?\s*)([^\n]+(?:\n(?!\*)[^\n]+)*)', t, re.IGNORECASE)
    if issue_m:
        issue_body = issue_m.group(2).strip().strip('"')
        if issue_body.startswith('*') and issue_body.endswith('*') and not issue_body.startswith('**'):
            issue_body = issue_body[1:-1].strip()
        issue_boxed = f'\n\n<div class="recit-issue-box"><span class="recit-issue-label">📌 CORE RECITATION ISSUE</span><div class="recit-issue-text">"{issue_body}"</div></div>\n\n'
        t = t[:issue_m.start()] + issue_boxed + t[issue_m.end():]

    return t

cases_meta = [
    # 06.1 - 06.5
    ('case-06-1-people-v-tanez', '06.1. People v. Tanes', 'People of the Philippines v. Novo Tanes y Belmonte', 'April 3, 2019', 'G.R. No. 240596', 'Caguioa, J.', 'Bail in Capital Offenses & Chain of Custody (Sec. 21 RA 9165)', 'Rule 114, Sec. 7', '06'),
    ('case-06-2-borlongan-v-pena', '06.2. Borlongan v. Peña', 'Teodoro C. Borlongan, Jr., et al. v. Magdaleno M. Peña', 'May 5, 2010', 'G.R. No. 143591', 'Perez, J.', 'Posting Bail Not a Waiver of Illegal Arrest / Absence of Probable Cause', 'Rule 114, Sec. 26', '06'),
    ('case-06-3-san-miguel-v-maceda', '06.3. San Miguel v. Maceda', 'Eduardo San Miguel v. Judge Bonifacio Sanz Maceda', 'April 4, 2007', 'A.M. No. RTJ-03-1749', 'Austria-Martinez, J.', 'Due Process in Bail Cancellation & Hearing Requirement', 'Rule 114, Sec. 17-20', '06'),
    ('case-06-4-mendoza-v-alarma', '06.4. Mendoza v. Alarma', 'Winston Mendoza and Fe Miclat v. Fernando & Fausta Alarma', 'May 7, 2008', 'G.R. No. 151970', 'Carpio, J.', 'Forfeiture vs. Judgment on the Bail Bond & Due Process', 'Rule 114, Sec. 21', '06'),
    ('case-06-5-leviste-v-ca', '06.5. Leviste v. Court of Appeals', 'Jose Antonio Leviste v. Court of Appeals & People', 'March 17, 2010', 'G.R. No. 189122', 'Corona, J.', 'Discretionary Bail Pending Appeal Post-RTC Conviction', 'Rule 114, Sec. 5', '06'),

    # 07.1 - 07.11
    ('case-07-1-miranda-vs-tuliao', '07.1. Miranda v. Tuliao', 'Jose C. Miranda, et al. v. Virgilio M. Tuliao', 'March 31, 2006', 'G.R. No. 158763', 'Chico-Nazario, J.', 'Custody of Law vs. Jurisdiction & Special Appearance to Quash Warrant', 'Rule 116 / Rule 114', '07'),
    ('case-07-2-gandarosa-vs-flores', '07.2. Gandarosa v. Flores', 'Mustapha M. Gandarosa v. Evaristo Flores & People', 'July 17, 2007', 'G.R. No. 167910', 'Chico-Nazario, J.', 'Unconditional Arraignment as Waiver & Abandonment of DOJ Appeal', 'Rule 116, Sec. 11', '07'),
    ('case-07-3-zapatos-vs-people', '07.3. Zapatos v. People', 'Raul Zapatos y Legaspi v. People of the Philippines', 'September 16, 2003', 'G.R. Nos. 147814-15', 'Sandoval-Gutierrez, J.', 'Arraignment Before Incompetent Court & Valid Self-Defense', 'Rule 116 / Rule 117', '07'),
    ('case-07-4-cabacangan-vs-concepcio', '07.4. Cabacangan v. Concepcion', 'Daniel Cabangangan v. CA Justices Concepcion, et al.', 'May 26, 1954', 'G.R. No. L-6353', 'Paras, C.J.', 'Mandatory Arraignment on Amended Information & Non-Waiver', 'Rule 116', '07'),
    ('case-07-5-people-vs-comendador', '07.5. People v. Comendador', 'People of the Philippines v. Diosdado Comendador', 'September 19, 1980', 'G.R. No. L-38000', 'Guerrero, J. (En Banc)', 'Capital Guilty Plea & Disproven Aggravating Circumstances', 'Rule 116, Sec. 3', '07'),
    ('case-07-6-people-vs-magat', '07.6. People v. Magat (Searching Inquiry)', 'People of the Philippines v. Antonio Magat y Londonio', 'May 31, 2000', 'G.R. No. 130026', 'Per Curiam (En Banc)', 'Searching Inquiry & Independent Evidence Curing Improvident Plea', 'Rule 116, Sec. 3', '07'),
    ('case-07-7-people-vs-balicasana', '07.7. People v. Balisacan', 'People of the Philippines v. Aurelio Balisacan', 'August 31, 1966', 'G.R. No. L-26376', 'Bengzon, J.P., J. (En Banc)', 'Self-Defense Testimony Vacates Guilty Plea / Void Summary Acquittal', 'Rule 116 / Rule 119', '07'),
    ('case-07-8-dawn-vs-sandiganbayan', '07.8. Daan v. Sandiganbayan', 'Joselito Raniero J. Daan v. Hon. Sandiganbayan', 'March 28, 2008', 'G.R. Nos. 163972-77', 'Austria-Martinez, J.', 'Pre-Trial Plea Bargaining & Lesser Included Offenses', 'Rule 116, Sec. 2', '07'),
    ('case-07-9-people-vs-magat', '07.9. People v. Magat (Void Plea Bargain)', 'People of the Philippines v. Antonio Magat y Londonio', 'May 31, 2000', 'G.R. No. 130026', 'Per Curiam (En Banc)', 'Plea Bargaining for Lesser Penalty is Void Ab Initio', 'Rule 116, Sec. 2', '07'),
    ('case-07-10-people-vs-dawaton', '07.10. People v. Dawaton', 'People of the Philippines v. Edgar Dawaton', 'September 17, 2002', 'G.R. No. 146247', 'Bellosillo, J. (En Banc)', 'Unaccepted Plea to Lesser Offense & Treachery on Drunk Victim', 'Rule 116, Sec. 2 / Art. 13 RPC', '07'),
    ('case-07-11-people-vs-documento', '07.11. People v. Documento', 'People of the Philippines v. Oscar M. Documento', 'March 17, 2010', 'G.R. No. 188706', 'Nachura, J.', 'Defective Searching Inquiry Cured by Overwhelming Evidence', 'Rule 116, Sec. 3', '07'),

    # 08.1 - 08.10
    ('case-08-1-people-v-magat', '08.1. People v. Magat (Double Jeopardy)', 'People of the Philippines v. Antonio Magat y Londonio', 'May 31, 2000', 'G.R. No. 130026', 'Per Curiam (En Banc)', 'Void Judgment Based on Conditional Plea Does Not Trigger Jeopardy', 'Rule 117, Sec. 3(i) & 7', '08'),
    ('case-08-2-people-v-sandiganbayan', '08.2. People v. Sandiganbayan (Alba)', 'People of the Philippines v. Sandiganbayan & Manuel S. Alba', 'September 29, 2004', 'G.R. No. 144159', 'Callejo, Sr., J.', 'Lack of Probable Cause Not Ground to Quash / State Due Process', 'Rule 117, Sec. 3', '08'),
    ('case-08-3-lazarte-v-sandiganbayan', '08.3. Lazarte v. Sandiganbayan', 'Felicisimo F. Lazarte, Jr. v. Sandiganbayan & People', 'March 13, 2009', 'G.R. No. 180122', 'Tinga, J. (En Banc)', 'Conspiracy as Mode of Commission & GOCC Manager Jurisdiction', 'Rule 117, Sec. 3(a) & (b)', '08'),
    ('case-08-4-serana-v-sandiganbayan', '08.4. Serana v. Sandiganbayan', 'Hannah Eunice D. Serana v. Sandiganbayan & People', 'January 22, 2008', 'G.R. No. 162059', 'Reyes, R.T., J.', 'Sandiganbayan Jurisdiction over Estafa & UP Student Regent', 'Rule 117, Sec. 3(b)', '08'),
    ('case-08-5-go-v-sandiganbayan', '08.5. Go v. Sandiganbayan', 'Henry T. Go v. Fifth Division Sandiganbayan & OSP', 'April 13, 2007', 'G.R. No. 172602', 'Callejo, Sr., J.', 'Private Co-Conspirators in RA 3019 Sec. 3(g) Graft', 'Rule 117, Sec. 3(a) & 9', '08'),
    ('case-08-6-castro-v-people', '08.6. Castro v. People', 'Jerome Castro v. People of the Philippines', 'July 23, 2008', 'G.R. No. 180832', 'Corona, J.', 'Finality of Acquittal & Prescription as Unreviewable Error of Judgment', 'Rule 117, Sec. 7', '08'),
    ('case-08-7-people-v-asis', '08.7. People v. Asis', 'People of the Philippines v. Judge Enrique C. Asis & Abordo', 'August 25, 2010', 'G.R. No. 173089', 'Mendoza, J.', 'Rule 65 Certiorari vs. Double Jeopardy / Error of Judgment', 'Rule 117, Sec. 7', '08'),
    ('case-08-8-ivler-v-modesto-san-pedro', '08.8. Ivler v. Modesto-San Pedro', 'Jason Ivler y Aguilar v. Judge Maria Rowena Modesto-San Pedro', 'November 17, 2010', 'G.R. No. 172716', 'Carpio, J.', 'Quasi-Offenses (Art. 365) & Prohibition Against Splitting Charges', 'Rule 117, Sec. 3(i) & 7', '08'),
    ('case-08-9-nierras-v-dacucuy', '08.9. Nierras v. Dacuycuy', 'Peter Nierras v. Judge Auxencio C. Dacuycuy & City Fiscal Lopez', 'January 11, 1990', 'G.R. Nos. 59568-76', 'Paras, J. (En Banc)', 'Same Act vs. Same Offense (Batas Pambansa Blg. 22 vs. Estafa)', 'Rule 117, Sec. 3(i)', '08'),
    ('case-08-10-people-v-lacson', '08.10. People v. Lacson', 'People of the Philippines, SOJ, PNP, et al. v. Panfilo M. Lacson', 'April 1, 2003', 'G.R. No. 149453', 'Callejo, Sr., J. (En Banc)', 'Provisional Dismissal Requisites & Prospective Two-Year Bar', 'Rule 117, Sec. 8', '08'),
    # Quiz Watchlist Express Cases (QW.1 - QW.2)
    ('case-qw-1-yasa-v-chavez', 'QW.1. Yasa v. Chavez', 'Francisco O. Yasa v. Mary Jean Chavez and Beberly Hoyumpa Cuasito, and People of the Philippines', 'June 23, 2026', 'G.R. No. 273948', 'Singh, J. (Third Division)', 'OSG Exclusive Authority & Demurrer Acquittal Double Jeopardy', 'Rule 119, Sec. 23 & Rule 117', 'QW'),
    ('case-qw-2-people-v-xxx271087', 'QW.2. People v. XXX271087', 'People of the Philippines v. XXX271087', 'July 14, 2026', 'G.R. No. 271087', 'Leonen, S.A.J. (Second Division)', 'Battered Woman Syndrome (BWS) Affirmative Defense & Expert Proof', 'R.A. No. 9262, Sec. 26 & Rule 116', 'QW'),
]

def build_case_sections(raw_text):
    cases_raw = re.split(r'(?m)^#\s+(?=0[678]\.\d+\.|CASE\s+\d+:)', raw_text)[1:]
    
    sections_by_module = {'06': [], '07': [], '08': [], 'QW': []}
    case_toc_items = []
    case_matrix_data = []

    for idx, c_raw in enumerate(cases_raw):
        slug, short_title, clean_name, date_str, gr_str, ponente_str, topic_tag, rule_str, mod_num = cases_meta[idx]
        case_toc_items.append((slug, f"{short_title} ({topic_tag})", mod_num))

        # Split into Outputs (handle optional markdown headings like ### [OUTPUT ...])
        parts = re.split(r'(?:^|\n)(?:#{1,6}\s*)?\[OUTPUT \d+:[^\]]+\]', c_raw)
        header_part = re.sub(r'\n---\s*$', '', parts[0].strip()).strip()
        out1_text = re.sub(r'\n---\s*$', '', parts[1].strip()).strip()
        out2_text = re.sub(r'\n---\s*$', '', parts[2].strip()).strip()
        out3_text = parts[3].strip() if len(parts) > 3 else ""

        # Clean trailing separator or next headers from out3
        out3_text = re.sub(r'\n---.*', '', out3_text, flags=re.DOTALL).strip()

        # Parse Output 3 for sticky sidebar
        parties_m = re.search(r'\*\s*(?:\*\*)?Parties\s*(?:\(and their contentions\))?:?(?:\*\*)?\s*(.*?)(?=\*\s*(?:\*\*)?Core Recitation Issue:|\Z)', out3_text, re.DOTALL | re.IGNORECASE)
        issue_m = re.search(r'\*\s*(?:\*\*)?Core Recitation Issue:?(?:\*\*)?\s*(.*?)(?=\*\s*(?:\*\*)?Short Ruling & Ratio:|\Z)', out3_text, re.DOTALL | re.IGNORECASE)
        ruling_m = re.search(r'\*\s*(?:\*\*)?Short Ruling & Ratio:?(?:\*\*)?\s*(.*?)\Z', out3_text, re.DOTALL | re.IGNORECASE)

        parties_raw = parties_m.group(1).strip() if parties_m else ""
        issue_raw = issue_m.group(1).strip() if issue_m else ""
        ruling_raw = ruling_m.group(1).strip() if ruling_m else ""

        parties_html = highlight_legal_terms(parse_markdown_snippet(parties_raw))
        issue_html = highlight_legal_terms(parse_markdown_snippet(issue_raw))
        ruling_html = highlight_legal_terms(parse_markdown_snippet(ruling_raw))

        # Extract Quick Bar Doctrine for matrix
        bar_doctrine_m = re.search(r'\*\s*(?:\*\*)?Recitation Doctrine / Bar Takeaway:(?:\*\*)?\s*([^\n]+(?:\n[^\*\n]+)*)', out2_text, re.IGNORECASE)
        bar_doctrine = bar_doctrine_m.group(1).strip().strip('"').strip('*').strip() if bar_doctrine_m else ""

        core_issue_m = re.search(r'\*\s*(?:\*\*)?Core Recitation Issue:(?:\*\*)?\s*([^\n]+(?:\n[^\*\n]+)*)', out2_text, re.IGNORECASE)
        core_issue = core_issue_m.group(1).strip().strip('"').strip('*').strip() if core_issue_m else issue_raw.strip('"').strip('*').strip()

        case_matrix_data.append({
            "num": short_title.split('.')[0] + '.' + short_title.split('.')[1],
            "title": short_title,
            "slug": slug,
            "citation": f"{gr_str} ({date_str})",
            "topic": topic_tag,
            "rule": rule_str,
            "module": mod_num,
            "issue": core_issue[:170] + ("..." if len(core_issue) > 170 else ""),
            "doctrine": bar_doctrine[:220] + ("..." if len(bar_doctrine) > 220 else "")
        })

        # Process Output 1 Body Text (VERBATIM)
        out1_proc = out1_text

        # Detect Trigger Words block
        tw_match = re.search(r'(?:\*\*)?Trigger Words:(?:\*\*)?\s*(.*?)(?=\n(?:\*\*)?[A-Z][a-zA-Z\s]+:(?:\*\*)?|\n\n(?:\*\*)?Facts of the Case|\Z)', out1_proc, re.DOTALL)
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
                    sep = ',' if (mod_num == 'QW' and ';' not in line) else ';'
                    for sub in line.split(sep):
                        sub = sub.strip()
                        if sub:
                            pills.append(f'<span class="trigger-pill">{html.escape(sub)}</span>')
            if pills:
                tw_html = f'<div class="trigger-container"><span class="trigger-title">KEY TOPICS & TRIGGERS:</span> {" ".join(pills)}</div>'
            out1_proc = out1_proc[:tw_match.start()] + out1_proc[tw_match.end():]

        # Convert Dispositive portion into blockquote accurately
        disp_match = re.search(r'(\*?\s*(?:\*\*)?Dispositive Portion:?(?:\*\*)?\s*)(.*?)(?=\n\*?\s*(?:\*\*)?Legal Analysis|\n\*?\s*(?:\*\*)?Brief Answers|\n\n###|\Z)', out1_proc, re.DOTALL | re.IGNORECASE)
        if disp_match:
            disp_body = parse_markdown_snippet(disp_match.group(2).strip())
            disp_quoted = f"\n\n##### Dispositive Portion\n\n<blockquote class=\"dispositive-quote\">{disp_body}</blockquote>\n\n"
            out1_proc = out1_proc[:disp_match.start()] + disp_quoted + out1_proc[disp_match.end():]

        out1_proc = enhance_out1_headings(out1_proc)
        out1_html = highlight_legal_terms(parse_markdown_snippet(out1_proc))

        # Enhance Output 2
        out2_proc = enhance_out2_sections(out2_text)
        out2_html = highlight_legal_terms(parse_markdown_snippet(out2_proc))

        # Check for Configuration Block in header_part
        config_box_html = ""
        config_m = re.search(r'\[CONFIGURATION BLOCK\](.*)', header_part, re.DOTALL)
        if config_m:
            cfg_text = config_m.group(1).strip()
            cfg_html = parse_markdown_snippet(cfg_text)
            config_box_html = f"""
            <div class="config-card">
              <div class="config-header">⚙️ CONFIGURATION & SYLLABUS FOCUS</div>
              <div class="config-body">{cfg_html}</div>
            </div>
            """

        section_html = f"""
    <!-- CASE {short_title} -->
    <section class="case-section" id="{slug}">
      <div class="case-grid">
        <!-- LEFT COLUMN: Full Verbatim Case Content -->
        <div class="case-main">
          <div class="case-header-card">
            <div class="case-num-badge">CASE {short_title.split()[0]}</div>
            <h4 id="{slug}-title">{short_title}</h4>
            <div class="case-meta">
              <span class="c-burgundy"><strong>{clean_name}</strong></span> • 
              <span class="c-teal">{gr_str}</span> • 
              <span>{date_str}</span> • 
              <span class="c-navy">Ponente: {ponente_str}</span>
            </div>
          </div>

          {config_box_html}
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
        sections_by_module[mod_num].append(section_html)

    return sections_by_module, case_toc_items, case_matrix_data

def build_full_html():
    raw_text = read_source()
    sections_by_mod, toc_items, matrix_data = build_case_sections(raw_text)

    # Build TOC options grouped hierarchically
    toc_options_html = ['<option value="" disabled selected>Select topic, module, or case...</option>']
    toc_options_html.append('<option value="#quiz-watchlist">▪ ★ Professor\'s Quiz Watchlist &amp; Expressly Named Cases</option>')
    toc_options_html.append('<option value="#expressly-named-cases">&nbsp;&nbsp;↳ Expressly Named Cases (9 Cases)</option>')
    toc_options_html.append('<option value="#administrative-unnamed-cases">&nbsp;&nbsp;↳ Administrative Matters &amp; Unnamed Cases Mentioned</option>')
    toc_options_html.append('<option value="#real-world-illustrations">&nbsp;&nbsp;↳ Real-World / Public-Figure Cases Used as Illustrations</option>')
    toc_options_html.append('<option value="#executive-overview">▪ I. Executive Overview & Master Procedural Flowchart</option>')
    toc_options_html.append('<option value="#three-doctrinal-pillars">▪ II. Three Procedural Pillars of Criminal Procedure Finals</option>')
    toc_options_html.append('<option value="#statutory-comparison-matrix">▪ III. Master Landmark Jurisprudence Matrix (28 Cases)</option>')
    
    # Module 06
    toc_options_html.append('<option value="#module-06-heading">▪ IV. Module 06: Rule 114 (Bail) Cases</option>')
    for slug, label, mnum in toc_items:
        if mnum == '06':
            toc_options_html.append(f'<option value="#{slug}">&nbsp;&nbsp;↳ {html.escape(label)}</option>')

    # Module 07
    toc_options_html.append('<option value="#module-07-heading">▪ V. Module 07: Rule 116 (Arraignment & Plea) Cases</option>')
    for slug, label, mnum in toc_items:
        if mnum == '07':
            toc_options_html.append(f'<option value="#{slug}">&nbsp;&nbsp;↳ {html.escape(label)}</option>')

    # Module 08
    toc_options_html.append('<option value="#module-08-heading">▪ VI. Module 08: Rule 117 (Motion to Quash & Double Jeopardy) Cases</option>')
    for slug, label, mnum in toc_items:
        if mnum == '08':
            toc_options_html.append(f'<option value="#{slug}">&nbsp;&nbsp;↳ {html.escape(label)}</option>')

    # Quiz Watchlist Express Cases
    toc_options_html.append('<option value="#module-qw-heading">▪ VII. Quiz Watchlist Express Cases (QW.1 – QW.2)</option>')
    for slug, label, mnum in toc_items:
        if mnum == 'QW':
            toc_options_html.append(f'<option value="#{slug}">&nbsp;&nbsp;↳ {html.escape(label)}</option>')

    # Build Matrix Table Rows
    matrix_rows = []
    for item in matrix_data:
        badge_text = "QUIZ" if item["module"] == "QW" else f"MOD {item['module']}"
        mod_badge = f'<span class="mod-badge mod-badge-{item["module"]}">{badge_text}</span>'
        matrix_rows.append(f"""
        <tr>
          <td>
            {mod_badge}<br>
            <a href="#{item['slug']}" class="matrix-link"><strong>{item['num']}</strong><br>{item['title']}</a>
          </td>
          <td><span class="c-teal">{item['citation']}</span></td>
          <td>
            <span class="topic-tag">{item['rule']}</span><br>
            <span class="topic-sub">{item['topic']}</span>
          </td>
          <td class="matrix-issue">{item['issue']}</td>
          <td class="matrix-doctrine">{item['doctrine']}</td>
        </tr>
        """)
    matrix_table_html = "\n".join(matrix_rows)

    mod_06_cases_html = "\n".join(sections_by_mod['06'])
    mod_07_cases_html = "\n".join(sections_by_mod['07'])
    mod_08_cases_html = "\n".join(sections_by_mod['08'])
    mod_qw_cases_html = "\n".join(sections_by_mod['QW'])

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Criminal Procedure Finals: Complete Landmark Jurisprudence (Modules 06, 07 & 08 — 26 Cases)</title>
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
      margin-top: 3rem;
      margin-bottom: 1rem;
      border-bottom: 2px solid #E2E8F0;
      padding-bottom: 0.4rem;
    }}
    .module-banner {{
      background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
      color: #FFFFFF;
      padding: 1.25rem 1.75rem;
      border-radius: 8px;
      margin-top: 3rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 4px 6px -1px rgba(30, 58, 138, 0.2);
    }}
    .module-banner h2 {{
      color: #FFFFFF;
      margin: 0;
      padding: 0;
      border-bottom: none;
      font-size: 1.45rem;
      letter-spacing: 0.02em;
    }}
    .module-banner-sub {{
      font-size: 0.88rem;
      color: #DBEAFE;
      margin-top: 0.35rem;
      font-weight: 400;
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

    /* CONFIGURATION CARD */
    .config-card {{
      background: #F8FAFC;
      border: 1px solid #CBD5E1;
      border-left: 4px solid #64748B;
      border-radius: 6px;
      padding: 0.85rem 1.15rem;
      margin: 1rem 0;
      font-size: 0.88rem;
    }}
    .config-header {{
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      color: #475569;
      text-transform: uppercase;
      margin-bottom: 0.35rem;
    }}
    .config-body ul {{
      margin: 0.25rem 0 0.25rem 1.2rem;
    }}
    .config-body li {{
      margin-bottom: 0.25rem;
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
      margin-bottom: 0.2rem;
    }}
    .topic-sub {{
      font-size: 0.78rem;
      color: #64748B;
      display: block;
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
    .mod-badge {{
      display: inline-block;
      font-size: 0.65rem;
      font-weight: 800;
      padding: 1px 5px;
      border-radius: 3px;
      margin-bottom: 0.25rem;
      letter-spacing: 0.04em;
    }}
    .mod-badge-06 {{ background: #FEF3C7; color: #92400E; }}
    .mod-badge-07 {{ background: #E0E7FF; color: #3730A3; }}
    .mod-badge-08 {{ background: #FCE7F3; color: #9D174D; }}
    .mod-badge-QW {{ background: #FFEDD5; color: #9A3412; }}

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
      min-height: 520px;
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

    /* PROFESSOR QUIZ WATCHLIST BANNER & CARDS */
    .quiz-watchlist-section {{
      background: #FFFBEB;
      border: 1.5px solid #FDE68A;
      border-top: 5px solid #C2410C;
      border-radius: 10px;
      padding: 1.75rem 2rem;
      margin: 1.5rem 0 2.5rem 0;
      box-shadow: 0 4px 10px -2px rgba(194, 65, 12, 0.08);
    }}
    .watchlist-header-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      border-bottom: 2px solid #FDE68A;
      padding-bottom: 0.85rem;
      margin-bottom: 1.25rem;
    }}
    .watchlist-badge {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background: #C2410C;
      color: #FFFFFF;
      padding: 0.25rem 0.65rem;
      border-radius: 4px;
    }}
    .watchlist-title {{
      margin: 0.35rem 0 0 0;
      font-size: 1.35rem;
      font-weight: 800;
      color: #7C2D12;
    }}
    .watchlist-subtitle {{
      font-size: 0.9rem;
      color: #9A3412;
      margin: 0.25rem 0 0 0;
      font-weight: 500;
    }}
    .watchlist-sub-h3 {{
      color: var(--color-navy);
      font-size: 1.15rem;
      font-weight: 800;
      margin-top: 1.5rem;
      margin-bottom: 0.85rem;
      padding-bottom: 0.35rem;
      border-bottom: 1.5px solid #FCD34D;
    }}
    .watchlist-list {{
      margin: 0.5rem 0 1.25rem 1.35rem;
      padding: 0;
    }}
    .watchlist-list > li {{
      margin-bottom: 0.9rem;
      padding: 0.75rem 1rem;
      background: #FFFFFF;
      border: 1px solid #FDE68A;
      border-left: 4px solid var(--color-navy);
      border-radius: 6px;
    }}
    .watchlist-list > li.quiz-priority {{
      border-left: 4px solid #C2410C;
      background: #FFF7ED;
    }}
    .watchlist-list ul {{
      margin: 0.4rem 0 0.2rem 1.2rem;
    }}
    .watchlist-list ul li {{
      margin-bottom: 0.25rem;
      font-size: 0.94rem;
    }}
    .watchlist-jump {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 700;
      color: #1E3A8A;
      background: #E0E7FF;
      border: 1px solid #C7D2FE;
      padding: 0.12rem 0.5rem;
      border-radius: 9999px;
      text-decoration: none;
      margin-left: 0.4rem;
      vertical-align: middle;
    }}
    .watchlist-jump:hover {{
      background: #1E3A8A;
      color: #FFFFFF;
    }}
    .watchlist-grid-cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 0.85rem;
      margin-top: 0.75rem;
    }}
    .watchlist-mini-card {{
      background: #FFFFFF;
      border: 1px solid #FDE68A;
      border-radius: 6px;
      padding: 0.85rem 1rem;
      font-size: 0.92rem;
    }}
    .watchlist-mini-card ul {{
      margin: 0.35rem 0 0 1.15rem;
    }}
    .watchlist-hr {{
      border: 0;
      height: 1px;
      background-color: #FCD34D;
      margin: 1.5rem 0;
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
      <span class="nav-label">FINALS NAVIGATION:</span>
      <select id="toc-select" class="nav-dropdown" onchange="if(this.value) {{ document.querySelector(this.value).scrollIntoView({{behavior: 'smooth'}}); }}">
        {' '.join(toc_options_html)}
      </select>
    </div>
  </nav>

  <div class="document-container">
    <h1>Criminal Procedure Finals: Master Landmark Jurisprudence</h1>
    <div class="doc-subtitle">Comprehensive Academic Digests, High-Yield Recitation Briefs & Strategic Snapshot Panels • Modules 06 (Rule 114: Bail), 07 (Rule 116: Arraignment & Plea), 08 (Rule 117: Motion to Quash, Double Jeopardy & Provisional Dismissal), and Quiz Watchlist Express Cases — Complete 28 Cases</div>

    <!-- PROFESSOR QUIZ WATCHLIST & EXPRESSLY NAMED CASES -->
    <section class="quiz-watchlist-section" id="quiz-watchlist">
      <div class="watchlist-header-bar">
        <div>
          <span class="watchlist-badge">★ UPCOMING QUIZ WATCHLIST</span>
          <h2 class="watchlist-title" style="border-bottom: none; padding-bottom: 0;">Cases &amp; Authorities Expressly Mentioned by the Judge / Professor</h2>
          <p class="watchlist-subtitle">High-priority cases, administrative circulars, unnamed recent rulings, and real-world illustrations flagged during lecture discussions.</p>
        </div>
      </div>

      <h3 class="watchlist-sub-h3" id="expressly-named-cases">Expressly Named Cases</h3>
      <ol class="watchlist-list">
        <li>
          <span class="c-burgundy"><strong><em>People v. Pimentel</em></strong></span>
          <ul>
            <li>Mentioned when discussing the results of the previous quiz (students failed to read the assigned cases).</li>
          </ul>
        </li>
        <li>
          <span class="c-burgundy"><strong><em>Tolentino v. [unclear]</em></strong></span>
          <ul>
            <li>Mentioned alongside <span class="c-burgundy"><em>People v. Pimentel</em></span> regarding the previous quiz (name partially unclear in the recording).</li>
          </ul>
        </li>
        <li>
          <span class="c-burgundy"><strong><em>Leviste v. Court of Appeals</em></strong></span> <a href="#case-06-5-leviste-v-ca" class="watchlist-jump">Jump to Full Digest (06.5) ↓</a>
          <ul>
            <li><strong>Topic:</strong> Discretionary bail pending appeal (<span class="c-teal"><strong>Rule 114, Sec. 5</strong></span>).</li>
            <li><strong>Doctrine:</strong> The accused was charged with murder and convicted of homicide. <span class="c-green">The Court of Appeals has discretion to deny bail even if none of the enumerated bail-negating circumstances are present, because <em>"any other circumstance"</em> is not exclusive; courts apply a two-stage determination.</span></li>
          </ul>
        </li>
        <li>
          <span class="c-burgundy"><strong><em>Mendoza v. Alarma</em></strong></span> <em>(also citing <span class="c-burgundy"><strong>Mendoza v. CA</strong></span>)</em> <a href="#case-06-4-mendoza-v-alarma" class="watchlist-jump">Jump to Full Digest (06.4) ↓</a>
          <ul>
            <li><strong>Topic:</strong> Forfeiture of bail / property bond (<span class="c-teal"><strong>Rule 114, Sec. 21</strong></span>).</li>
            <li><strong>Doctrine:</strong> Emphasizes the <span class="c-green"><strong><u>mandatory two-step procedure</u></strong></span>: (1) an order of forfeiture giving the bondsmen 30 days to produce the accused and show cause, followed by (2) a separate <span class="c-green"><strong>judgment on the bond</strong></span> (which must become final after 15 days) before a writ of execution and public auction can validly issue.</li>
          </ul>
        </li>
        <li>
          <span class="c-burgundy"><strong><em>Borlongan v. Peña</em></strong></span> <a href="#case-06-2-borlongan-v-pena" class="watchlist-jump">Jump to Full Digest (06.2) ↓</a>
          <ul>
            <li><strong>Topic:</strong> Bail not a bar to objections (<span class="c-teal"><strong>Rule 114, Sec. 26</strong></span>).</li>
            <li><strong>Doctrine:</strong> <span class="c-green">Applying for or posting bail does not automatically waive objections to an illegal arrest or lack of/irregular preliminary investigation. Waiver applies only upon voluntarily entering a plea and actively participating in trial.</span></li>
          </ul>
        </li>
        <li>
          <span class="c-burgundy"><strong><em>Yasa v. Chavez</em></strong></span> <a href="#case-qw-1-yasa-v-chavez" class="watchlist-jump">Jump to Full Digest (QW.1) ↓</a>
          <ul>
            <li><strong>Topic:</strong> Who may appeal criminal vs. civil aspects.</li>
            <li><strong>Doctrine:</strong> <span class="c-green">Only the Office of the Solicitor General (OSG) can bring an appeal or represent the People on the criminal aspect before the Court of Appeals or Supreme Court. A private complainant lacks legal standing to appeal a criminal acquittal or dismissal via demurrer to evidence (only the civil aspect may be appealed).</span></li>
          </ul>
        </li>
        <li class="quiz-priority">
          <span class="c-burgundy"><strong><em>Ivler v. Modesto</em> / <em>Ivler v. Modesto-San Pedro</em></strong></span> <a href="#case-08-8-ivler-v-modesto-san-pedro" class="watchlist-jump">Jump to Full Digest (08.8) ↓</a>
          <ul>
            <li><strong>Topic:</strong> <span class="c-green"><strong>Double jeopardy</strong></span> and reckless imprudence (<span class="c-teal"><strong>Article 365, RPC</strong></span>).</li>
            <li><strong>Doctrine:</strong> <span class="c-green">Pleading guilty to the lesser offense bars subsequent prosecution for reckless imprudence resulting in homicide. All resulting effects of a single reckless act must be incorporated into one charge; complex crime rules do not apply.</span></li>
            <li><span class="c-rust"><strong>Quiz Note:</strong></span> Flagged by the professor as very important for the quiz.</li>
          </ul>
        </li>
        <li>
          <span class="c-burgundy"><strong><em>People v. Galman</em></strong></span>
          <ul>
            <li><strong>Topic:</strong> Exception to <span class="c-green"><strong>double jeopardy</strong></span>.</li>
            <li><strong>Doctrine:</strong> <span class="c-rust"><strong><u>Double jeopardy cannot be invoked when the prosecution was denied due process (not given an opportunity to present evidence).</u></strong></span></li>
          </ul>
        </li>
        <li>
          <span class="c-burgundy"><strong><em>Crespo v. Mogul</em></strong></span>
          <ul>
            <li><strong>Context:</strong> Mentioned when commenting on the midterm exam results (<em>"first year pa lang dapat alam ninyo na 'yon"</em>).</li>
          </ul>
        </li>
      </ol>

      <hr class="watchlist-hr">

      <h3 class="watchlist-sub-h3" id="administrative-unnamed-cases">Administrative Matters &amp; Unnamed Cases Mentioned</h3>
      <div class="watchlist-grid-cards">
        <div class="watchlist-mini-card">
          <strong>Rules on Extradition Proceedings (<span class="c-teal">A.M. No. 22-03-29-SC</span>)</strong>
          <ul>
            <li><span class="c-teal"><strong>Rule 3, Sec. 1</strong></span> — Guidelines on bail in extradition proceedings.</li>
          </ul>
        </div>
        <div class="watchlist-mini-card">
          <strong>Guidelines for Continuous Trial of Criminal Cases (<span class="c-teal">A.M. No. 15-06-10-SC</span>)</strong>
          <ul>
            <li>Covers periods for arraignment/trial and allowable grounds for postponement (<em>physical inability</em> of counsel and <em>force majeure</em>).</li>
          </ul>
        </div>
        <div class="watchlist-mini-card">
          <strong>Unnamed Recent Supreme Court Case on Battered Woman Syndrome</strong> <a href="#case-qw-2-people-v-xxx271087" class="watchlist-jump">Jump to Full Digest: People v. XXX271087 (QW.2) ↓</a>
          <ul>
            <li>Wife was acquitted of killing her husband (discussed under <span class="c-teal"><strong>Rule 117, Sec. 3(h)</strong></span> on legal excuse/justification and absolutory causes).</li>
          </ul>
        </div>
        <div class="watchlist-mini-card">
          <strong>Unnamed Recent Supreme Court Case on <span class="c-teal">P.D. 1602</span> (Illegal Gambling)</strong>
          <ul>
            <li>For conviction, police officers must prove both the <strong>operator</strong> and the <strong>amount of the bet</strong>.</li>
          </ul>
        </div>
        <div class="watchlist-mini-card">
          <strong>Unnamed Court of Appeals Reversal</strong>
          <ul>
            <li>A lower court conviction was reversed because the identity of the accused was not established during the proceedings.</li>
          </ul>
        </div>
      </div>

      <hr class="watchlist-hr">

      <h3 class="watchlist-sub-h3" id="real-world-illustrations">Real-World / Public-Figure Cases Used as Illustrations</h3>
      <ul class="watchlist-list" style="list-style-type: disc;">
        <li><strong>Antonio Trillanes</strong> — Peninsula incident (bail in the military is not allowed).</li>
        <li><strong>Joma Sison</strong> — Netherlands (political crimes / lack of extradition treaty).</li>
        <li><strong>Gloria Macapagal Arroyo &amp; Leila de Lima</strong> — DOJ travel restriction, hospital arrest, and detention.</li>
        <li><strong>Alice Guo</strong> — Property bond example.</li>
        <li><strong>Juan Ponce Enrile</strong> — Health and age considered in granting bail.</li>
        <li><strong>Bong Revilla &amp; Jinggoy Estrada</strong> — Sandiganbayan bail grant vs. denial and 90-day suspension; <span class="c-teal"><strong>Rule 65</strong></span> <em>certiorari</em> to the Supreme Court.</li>
        <li><strong>Sara Duterte</strong> — Voluntary surrender / posting bail; impeachment subpoena and right against self-incrimination hypothetical.</li>
        <li><strong>Kian delos Santos</strong> — Presumption of innocence / drug war context.</li>
      </ul>
    </section>

    <!-- SECTION I: EXECUTIVE OVERVIEW & PROCEDURAL FLOWCHART -->
    <h3 id="executive-overview">I. Executive Overview & Master Procedural Flowchart</h3>
    <p>
      This master consolidated reviewer packages the twenty-eight (28) landmark Supreme Court decisions governing the Criminal Procedure Finals syllabus: <span class="c-teal"><strong>Rule 114 (Bail)</strong></span>, <span class="c-teal"><strong>Rule 116 (Arraignment and Plea)</strong></span>, and <span class="c-teal"><strong>Rule 117 (Motion to Quash, Double Jeopardy & Provisional Dismissal)</strong></span> of the Revised Rules of Criminal Procedure, together with the expressly named Quiz Watchlist cases (<span class="c-teal"><strong>Rule 119, Sec. 23 Demurrer & R.A. 9262, Sec. 26 BWS Defense</strong></span>).
    </p>

    <!-- INTERACTIVE PAN-AND-ZOOM MERMAID DIAGRAM -->
    <div class="diagram-wrapper">
      <div class="diagram-toolbar">
        <span class="diagram-label">MASTER PROCEDURAL DECISION ARCHITECTURE: RULES 114, 116 & 117 <span class="diagram-hint">(Drag to pan • Scroll to zoom • ⛶ for Fullscreen)</span></span>
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
  START(["CRIMINAL ACTION INITIATED"]) --> BAIL_STAGE{{"Bail Determination (Rule 114)"}}

  %% RULE 114 BRANCH
  BAIL_STAGE -- "Capital Offense / Life Imprisonment" --> SUMMARY_HEARING["People v. Tanes (06.1)<br/>• Burden on Prosecution to prove evidence of guilt is strong<br/>• Unexcused non-compliance with Sec. 21 RA 9165 compromises corpus delicti<br/>• Evidence of guilt not strong -> Accused entitled to bail"]
  BAIL_STAGE -- "Posting Bail & Challenging Arrest" --> BORLONGAN["Borlongan v. Peña (06.2)<br/>• Sec. 26: Posting bail NOT a waiver of illegal arrest or lack of prelim invest.<br/>• Objection must be raised prior to plea<br/>• Overruled prior automatic waiver doctrine"]
  BAIL_STAGE -- "Motion to Cancel Recommended Bail" --> SAN_MIGUEL["San Miguel v. Maceda (06.3)<br/>• Procedural Due Process: Notice & hearing strictly mandatory<br/>• Cancelling bail 2 days before hearing without hearing is misconduct"]
  BAIL_STAGE -- "Bail Bond Confiscation & Execution" --> MENDOZA["Mendoza v. Alarma (06.4)<br/>• Sec. 21: Order of forfeiture is purely INTERLOCUTORY<br/>• Formal judgment on the bond mandatory before execution against property"]
  BAIL_STAGE -- "Bail Pending Appeal (Post-RTC Conviction)" --> LEVISTE["Leviste v. Court of Appeals (06.5)<br/>• Sec. 5: Presumption of innocence ends upon conviction<br/>• Bail is purely DISCRETIONARY (grave caution & strong reasons)<br/>• Absence of Par. 3 circumstances does NOT make bail automatic"]

  %% RULE 116 ARRAIGNMENT BRANCH
  BAIL_STAGE --> ARRN["Arraignment & Plea (Rule 116)"]

  ARRN -- "Custody of Law vs. Jurisdiction" --> MIRANDA["Miranda v. Tuliao (07.1)<br/>• Custody of law required ONLY in applications for bail<br/>• Motion to quash arrest warrant is a special appearance<br/>• No custody required to assail jurisdiction over person"]
  ARRN -- "Unconditional Plea of Not Guilty" --> GANDAROSA["Gandarosa v. Flores (07.2)<br/>• Unconditional plea waives preliminary investigation<br/>• Constitutes abandonment of pending DOJ petition for review<br/>• Court relieved of duty to independently evaluate probable cause"]
  ARRN -- "Arraignment Before Incompetent Court" --> ZAPATOS["Zapatos v. People (07.3)<br/>• Arraignment before court lacking subject-matter jurisdiction is void<br/>• First jeopardy never attached (RTC vs. Sandiganbayan)<br/>• Physical evidence proves lawful self-defense"]
  ARRN -- "Arraignment on Superseded Original Information" --> CABACANGAN["Cabacangan v. Concepcion (07.4)<br/>• Amended information completely supersedes original<br/>• Timely objection by counsel negates waiver<br/>• Mandatory arraignment on amended charge"]
  ARRN -- "Plea of Guilty to Capital Offense" --> CAPITAL_PLEA{{"Capital Plea Doctrines"}}
  CAPITAL_PLEA -- "Plea for Lesser Penalty" --> COMENDADOR["People v. Comendador (07.5)<br/>• Appeal for lesser penalty is NOT a conditional plea<br/>• Reception of evidence mandatory; disproved aggravating circumstances rejected"]
  CAPITAL_PLEA -- "Plea Bargaining for Penalty" --> MAGAT_PLEA["People v. Magat (07.6, 07.9, 08.1)<br/>• Bargaining solely for penalty is VOID AB INITIO<br/>• Treated as plea of not guilty; no double jeopardy attaches"]
  CAPITAL_PLEA -- "Defective Searching Inquiry" --> DOCUMENTO["People v. Documento (07.11)<br/>• Improvident plea does not void conviction when<br/>independent evidence proves guilt beyond reasonable doubt"]
  ARRN -- "Self-Defense Testimony after Guilty Plea" --> BALISACAN["People v. Balisacan (07.7)<br/>• Exculpatory testimony vacates plea of guilty ipso facto<br/>• Summary acquittal without trial is void; no double jeopardy"]
  ARRN -- "Pre-Trial Plea Bargaining" --> PLEA_BARGAIN{{"Plea Bargaining Framework (Sec. 2)"}}
  PLEA_BARGAIN -- "Lesser Included Offense (Consent of Pros & Offended)" --> DAAN["Daan v. Sandiganbayan (07.8)<br/>• Sec. 2: Lesser included offenses (Art. 172 in 171; Art. 218 in 217)<br/>• Arbitrary refusal is grave abuse of discretion"]
  PLEA_BARGAIN -- "Unaccepted Pre-Trial Offer" --> DAWATON["People v. Dawaton (07.10)<br/>• Unaccepted offer to plead guilty to homicide does NOT mitigate murder<br/>• Treachery on sleeping/drunk victim"]
  ARRN -- "Affirmative Defense: Battered Woman Syndrome" --> XXX_BWS["People v. XXX271087 (QW.2)<br/>• Sec. 26 RA 9262: Two full cycles of violence + expert psychiatric proof<br/>• Exempt from criminal & civil liability; police reports not mandatory"]

  %% RULE 117 MOTION TO QUASH & DOUBLE JEOPARDY BRANCH
  ARRN --> MTQ{{"Motion to Quash (Rule 117)"}}

  MTQ -- "Lack of Probable Cause" --> ALBA["People v. Sandiganbayan (Alba) (08.2)<br/>• Absence of PC is NOT an authorized ground to quash under Sec. 3<br/>• Summary pre-trial acquittal violates State due process; void"]
  MTQ -- "Failure to Charge an Offense (Sec. 3[a])" --> HYPO{{"Hypothetical Admission Test"}}
  HYPO -- "Conspiracy as Mode of Commission" --> LAZARTE["Lazarte v. Sandiganbayan (08.3)<br/>• Ultimate facts & community of design suffice<br/>• Specific overt acts are evidentiary; GOCC managers under Sandiganbayan"]
  HYPO -- "Private Co-Conspirator in Graft" --> GO["Go v. Sandiganbayan (08.5)<br/>• Private persons liable under Sec. 3(g) RA 3019 via conspiracy<br/>• Sec. 3(a) defense never waived (Sec. 9)"]
  MTQ -- "Lack of Jurisdiction (Sec. 3[b])" --> SERANA["Serana v. Sandiganbayan (08.4)<br/>• Estafa in relation to office falls under Sandiganbayan<br/>• UP Student Regent is a public officer under Sec. 4(A)(1)(g)"]

  %% DOUBLE JEOPARDY & PROVISIONAL DISMISSAL
  MTQ -- "Double Jeopardy (Sec. 3[i] & Sec. 7)" --> DJ_BRANCH{{"Double Jeopardy Invocations"}}
  DJ_BRANCH -- "Finality-of-Acquittal Rule" --> ACQUITTAL["Castro v. People (08.6) & People v. Asis (08.7)<br/>• Errors of judgment unassailable by certiorari<br/>• Acquittal is immediately final; certiorari lies only for sham trial / ouster"]
  DJ_BRANCH -- "Demurrer Acquittal & OSG Standing" --> YASA["Yasa v. Chavez (QW.1)<br/>• Private complainant lacks standing on criminal aspect without OSG<br/>• Demurrer acquittal is adjudication on merits -> double jeopardy"]
  DJ_BRANCH -- "Quasi-Crimes (Art. 365, RPC)" --> IVLER["Ivler v. Modesto-San Pedro (08.8)<br/>• Reckless imprudence is a single indivisible quasi-offense<br/>• Splitting charges prohibited; prior conviction bars second charge"]
  DJ_BRANCH -- "Same Act vs. Same Offense" --> NIERRAS["Nierras v. Dacuycuy (08.9)<br/>• Double jeopardy bars same OFFENSE, not same ACT<br/>• BP 22 (malum prohibitum) & Estafa (malum in se) distinct"]

  MTQ -- "Provisional Dismissal (Sec. 8)" --> PROV_DISMISS["People v. Lacson (08.10)<br/>• Conditions sine qua non: Express consent of accused + notice to ALL heirs<br/>• 2-year time-bar applies PROSPECTIVELY from Dec. 1, 2000"]

  classDef navyNode fill:#EFF6FF,stroke:#1E3A8A,stroke-width:2px,color:#1E3A8A;
  classDef tealNode fill:#F0FDFA,stroke:#0F766E,stroke-width:2px,color:#0F766E;
  classDef greenNode fill:#ECFDF5,stroke:#166534,stroke-width:2px,color:#166534;
  classDef rustNode fill:#FFF7ED,stroke:#C2410C,stroke-width:2px,color:#C2410C;

  class START,ARRN,BAIL_STAGE,MTQ navyNode;
  class MAGAT_PLEA,ALBA,ACQUITTAL,YASA,IVLER,BALISACAN,SAN_MIGUEL,MENDOZA rustNode;
  class LAZARTE,GO,SERANA,NIERRAS,MIRANDA,CABACANGAN,ZAPATOS tealNode;
  class SUMMARY_HEARING,BORLONGAN,LEVISTE,COMENDADOR,DOCUMENTO,DAAN,DAWATON,PROV_DISMISS,XXX_BWS greenNode;
          </pre>
        </div>
      </div>
    </div>

    <!-- SECTION II: THREE DOCTRINAL PILLARS -->
    <h3 id="three-doctrinal-pillars">II. The Three Doctrinal Pillars of Criminal Procedure Finals</h3>
    <div class="ui-box">
      <div class="ui-grid">
        <div class="ui-col">
          <div class="ui-icon">🔓</div>
          <div class="ui-kicker">MODULE 06: RULE 114</div>
          <div class="ui-title">Bail & Provisional Liberty</div>
          <div class="ui-sub"><strong>5 Cases:</strong> Capital offense summary hearings (Tanes), Non-waiver of illegal arrest (Borlongan), Due process in cancellation (San Miguel), Interlocutory forfeiture vs. Judgment on bond (Mendoza), Discretionary post-conviction bail (Leviste).</div>
        </div>
        <div class="ui-col">
          <div class="ui-icon">⚖️</div>
          <div class="ui-kicker">MODULE 07: RULE 116</div>
          <div class="ui-title">Arraignment & Plea</div>
          <div class="ui-sub"><strong>11 Cases:</strong> Custody of law vs. Special appearance (Miranda), Unconditional arraignment waiver (Gandarosa), Incompetent court void plea (Zapatos), Amended information (Cabacangan), Capital pleas & Searching inquiry (Comendador, Magat, Balisacan, Daan, Dawaton, Documento).</div>
        </div>
        <div class="ui-col">
          <div class="ui-icon">🛡️</div>
          <div class="ui-kicker">MODULE 08: RULE 117</div>
          <div class="ui-title">Quashal & Double Jeopardy</div>
          <div class="ui-sub"><strong>10 Cases:</strong> Lack of PC not ground to quash (Alba), Conspiracy facial sufficiency (Lazarte), GOCC & Student Regent jurisdiction (Serana), Private co-conspirators in graft (Go), Finality of acquittal (Castro, Asis), Quasi-crimes (Ivler), Same act vs. Offense (Nierras), Provisional dismissal time-bar (Lacson).</div>
        </div>
      </div>
    </div>

    <!-- SECTION III: MASTER COMPARISON MATRIX -->
    <h3 id="statutory-comparison-matrix">III. Master Landmark Jurisprudence Matrix (Complete 28 Cases)</h3>
    <p>Comprehensive comparative lookup table cross-referencing all 28 decisions across Modules 06, 07, 08, and Quiz Watchlist Express Cases:</p>

    <div style="overflow-x: auto;">
      <table class="ui-table">
        <thead>
          <tr>
            <th style="width: 15%;">Module & Case</th>
            <th style="width: 15%;">Citation & Date</th>
            <th style="width: 15%;">Rule & Concept Focus</th>
            <th style="width: 25%;">Core Recitation Issue</th>
            <th style="width: 30%;">Recitation Doctrine / Bar Takeaway</th>
          </tr>
        </thead>
        <tbody>
          {matrix_table_html}
        </tbody>
      </table>
    </div>

    <hr>

    <!-- SECTION IV: MODULE 06 CASE DIGESTS -->
    <div class="module-banner" id="module-06-heading">
      <h2>IV. Module 06 — Rule 114 (Bail) Landmark Jurisprudence</h2>
      <div class="module-banner-sub">Cases 06.1 to 06.5: Capital Offenses, Non-Waiver of Illegal Arrest, Cancellation Due Process, Bond Forfeiture & Post-Conviction Discretionary Bail</div>
    </div>

    {mod_06_cases_html}

    <hr>

    <!-- SECTION V: MODULE 07 CASE DIGESTS -->
    <div class="module-banner" id="module-07-heading">
      <h2>V. Module 07 — Rule 116 (Arraignment & Plea) Landmark Jurisprudence</h2>
      <div class="module-banner-sub">Cases 07.1 to 07.11: Custody of the Law, Arraignment Waivers, Superseded Informations, Capital Pleas, Searching Inquiries & Plea Bargaining</div>
    </div>

    {mod_07_cases_html}

    <hr>

    <!-- SECTION VI: MODULE 08 CASE DIGESTS -->
    <div class="module-banner" id="module-08-heading">
      <h2>VI. Module 08 — Rule 117 (Motion to Quash & Double Jeopardy) Landmark Jurisprudence</h2>
      <div class="module-banner-sub">Cases 08.1 to 08.10: Grounds for Quashal, Jurisdiction, Finality of Acquittal, Single Negligent Act in Quasi-Crimes & Section 8 Provisional Dismissal</div>
    </div>

    {mod_08_cases_html}

    <hr>

    <!-- SECTION VII: QUIZ WATCHLIST EXPRESS CASES -->
    <div class="module-banner" id="module-qw-heading" style="background: linear-gradient(135deg, #9A3412 0%, #C2410C 100%); border-left-color: #FEF3C7;">
      <h2>VII. Quiz Watchlist Express Cases — Full Digests (2026 Landmark Rulings)</h2>
      <div class="module-banner-sub">Cases QW.1 to QW.2: Private Complainant's Standing & Demurrer Acquittal Double Jeopardy (Yasa v. Chavez) • Affirmative Defense of Battered Woman Syndrome (People v. XXX271087)</div>
    </div>

    {mod_qw_cases_html}

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

    // Touch events for tablets / mobile
    document.addEventListener('touchstart', (e) => {{
      const viewport = e.target.closest('.diagram-viewport');
      if (!viewport || e.touches.length !== 1) return;
      const container = viewport.querySelector('.diagram-container');
      if (!container) return;
      const touch = e.touches[0];
      viewport.classList.add('is-dragging');
      activeDiagramDrag = {{
        viewport,
        container,
        startX: touch.clientX - parseFloat(container.dataset.panX || '0'),
        startY: touch.clientY - parseFloat(container.dataset.panY || '0')
      }};
    }}, {{ passive: true }});

    document.addEventListener('touchmove', (e) => {{
      if (!activeDiagramDrag || e.touches.length !== 1) return;
      const touch = e.touches[0];
      activeDiagramDrag.container.dataset.panX = touch.clientX - activeDiagramDrag.startX;
      activeDiagramDrag.container.dataset.panY = touch.clientY - activeDiagramDrag.startY;
      updateDiagramTransform(activeDiagramDrag.container);
    }}, {{ passive: true }});

    document.addEventListener('touchend', () => {{
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
        '#quiz-watchlist, #expressly-named-cases, #administrative-unnamed-cases, #real-world-illustrations, #executive-overview, #three-doctrinal-pillars, #statutory-comparison-matrix, #module-06-heading, #module-07-heading, #module-08-heading, #module-qw-heading, .case-section'
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
    print(f"File size: {os.path.getsize(OUTPUT_HTML_PATH)} bytes")

if __name__ == "__main__":
    build_full_html()
