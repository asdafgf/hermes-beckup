---
name: document-research-compilation
description: >-
  Internetten kaynak bularak yerel dosya sisteminde belge toplama, klasörleme ve Word/PDF raporu oluşturma.
  Use this when the user asks to find documents on a topic from the web, download them, organize in a folder,
  and create a summary/compilation document.
version: "1.0"
triggers:
  - "internette ... ara / bul / indir"
  - "word belgesine kaydet / rapor oluştur"
  - "belgeleri topla / klasörle"
  - "sunum standı / verileri hazırla"
  - "dökümanları bir araya getir"
---

# Document Research & Compilation Skill

## Purpose
When a user asks you to search the web for documents on a specific topic, download them, organize them in a local folder, and create a compilation/Word document — follow this workflow.

## Workflow

### Phase 1: Understand the Request
1. Clarify **what** to search for (topic, keywords, document type: PDF/DOC/XLS/PPT)
2. Clarify **where** to save (Desktop folder, custom path)
3. Clarify **output format** (Word docx, PDF, or just collected files)

### Phase 2: Web Research
1. Run multiple `web_search` calls with varied Turkish/English keywords
2. Extract content from top results using `web_extract` for deeper detail
3. Look specifically for:
   - `*musteri*`, `*memnuniyet*`, `*anket*`, `*müşteri*` (Turkish documents)
   - ISO standard numbers, official forms, academic theses
   - Direct download links (.doc, .docx, .xls, .xlsx, .pdf, .pptx)

### Phase 3: Download & Organize
1. Create the target folder structure:
   ```bash
   mkdir -p "/c/Users/eymen/Desktop/<klasor_adi>/{dokumanlar,gorseller,kaynaklar}"
   ```
   Always create three subfolders: `dokumanlar/` for text/PDF files, `gorseller/` for images and diagrams, `kaynaklar/` for metadata files.

2. Use `curl -sL -o "<filename>" "<url>"` for each file
   - Name files descriptively in Turkish (e.g., `ic_musteri_memnuniyet_anket_formu.xls`)

3. Run downloads IN PARALLEL (multiple simultaneous curl calls) for speed

4. For image searches: run separate `web_search` calls for visual content (diagrams, flow charts, process maps) alongside document searches. ResearchGate, Creately, and ConceptDraw often host relevant diagrams.
3. Run downloads IN PARALLEL (multiple simultaneous curl calls) for speed
4. After all downloads, list the folder with `ls -lhS` to verify

### Phase 3.1: Organize into Subfolders
Create a structured archive, not a flat file dump:
- `dokumanlar/` — markdown extracts, PDFs, HTML pages, DOCX files
- `gorseller/` — images, diagrams, screenshots (JPEG, PNG, SVG)
- `kaynaklar/` — metadata JSON, source URL lists, provenance tracker

Create a `kaynaklar/kaynak_listesi.json` with:
```json
{
  "topic": "...",
  "download_date": "2026-05-11",
  "dokumanlar": [
    {"file": "kaynak_1.md", "source": "Site Adi - Sayfa Basligi"}
  ],
  "gorseller": [
    {"file": "diyagram.jpg", "source": "URL"}
  ]
}
```

### Phase 4: Compilation Document (Word)
1. Install python-docx if needed: `pip install python-docx -q`
2. Use Python (via terminal) to create a structured Word document:
   - **Cover page** with title, subtitle, date, source info
   - **Numbered sections** with headings (h1, h2)
   - **Tables** for structured data (use `style='Light Grid Accent 1'`)
   - **Bullet lists** for features, benefits, factors
   - **Bold+normal text pairs** for labeled descriptions
3. Save path must use forward slashes (`/`) in Python, not backslashes
4. If the target folder has Turkish characters (ü, ı, ş, ç, ö, ğ), save to Temp first then `cp` to target:

```bash
# Save to Temp first (avoids UTF-8 path issues in python-docx)
python.exe "C:/Users/eymen/AppData/Local/Temp/make_doc.py"
# Then copy to target
cp "/c/Users/eymen/AppData/Local/Temp/output.docx" "/c/Users/eymen/Desktop/hedef_klasor/output.docx"
```

### Phase 5: Update an Existing Document (Append Mode)

When the user already has a Word document and wants to add gathered materials to it:

1. Load the existing doc: `doc = Document('path/to/existing.docx')`
2. Add a page break and new section heading (e.g. "10. Toplanan Dokumanlar ve Kaynaklar")
3. List each downloaded file with its description and source URL
4. Save back to the same path
5. Preserve all original content — only append

Example pattern:
```python
from docx import Document
from docx.shared import Pt, RGBColor, Cm
doc = Document('mevcut_belge.docx')
doc.add_page_break()
h = doc.add_heading('10. TOPLANAN DOKUMANLAR', level=1)
for run in h.runs:
    run.font.color.rgb = RGBColor(0, 51, 102)
doc.save('mevcut_belge.docx')
```

### Phase 6: Verify the Result
1. List the target folder: `ls -lhS "/c/Users/eymen/Desktop/<klasor>/"`
2. Confirm the Word doc opens (check file size > 10KB)
3. Tell the user exactly where everything is stored

## Windows Python-docx Path Workaround

On Windows with Turkish characters in folder names (Masaüstü, ic_musteri etc.), python-docx's internal zip writer fails with `FileNotFoundError` even though `os.path.exists()` returns True. **Workaround: save to Temp, then copy.**

```bash
# 1. In Python script, save to Temp
output = 'C:/Users/eymen/AppData/Local/Temp/10002_output.docx'
doc.save(output)

# 2. From bash, copy to target (bash handles UTF-8 paths fine)
cp "/c/Users/eymen/AppData/Local/Temp/10002_output.docx" \
   "/c/Users/eymen/OneDrive/Masaüstü/hedef_klasor/10002_output.docx"
```

Alternatively, use Anaconda Python's forward-slash path (`/`) with cp1254-encoded bytes:
```python
p_bytes = b'C:\\Users\\eymen\\OneDrive\\Masa\xfcst\xfc\\hedef.docx'  # \xfc = ü in cp1254
path = p_bytes.decode('cp1254')
```

## Sending the Document via Email (SMTP)

📎 **Referans:** `references/windows-security-audit.md` — Windows güvenlik taraması adımları (tasklist, netstat, Defender, yorumlama kılavuzu)

Gmail and Outlook **block direct password-based SMTP login**. The user MUST create a **Gmail App Password** (16 chars) for SMTP to work.

### First: Guide the User to Create an App Password

1. Tell the user to go to: https://myaccount.google.com/apppasswords
2. Sign in with their Gmail credentials
3. Select "App" → "Other (Custom name)" → type "Hermes" → "Generate"
4. The resulting 16-character code is the **app password** (NOT their regular password)
5. Ask the user to share this 16-char code

**Crucial: The user's regular Gmail password WILL NOT work for SMTP login.** If they keep giving you their regular password, you must repeatedly explain they need the App Password from that specific page, not their regular login password.

### Alternative Delivery Methods (When SMTP Fails)

If the user cannot or will not provide an App Password:

1. **Telegram media upload** — Copy the file to the image_cache directory and send it directly in the chat:
   ```bash
   cp "/source/path/file.docx" "/c/Users/eymen/AppData/Local/hermes/image_cache/file.docx"
   # Then respond with: MEDIA:/path/to/file
   ```
2. **TXT fallback** — If the user can't open DOCX on their phone, convert to plain text and send as .txt:
   ```python
   from docx import Document
   doc = Document(docx_path)
   with open(txt_path, 'w', encoding='utf-8') as f:
       for para in doc.paragraphs:
           f.write(para.text + '\n')
   ```
3. **Manual send** — Give the user the exact file path on their Desktop so they can attach it manually

### Gmail SMTP Config
```python
host = 'smtp.gmail.com'
port = 587
# User must enable 2-Step Verification then create App Password at:
# https://myaccount.google.com/ > Security > 2-Step Verification > App Passwords
```

### Sending with Attachment
```python
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain', 'utf-8'))

with open(filepath, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
    msg.attach(part)

context = ssl.create_default_context()
server = smtplib.SMTP(host, port, timeout=10)
server.starttls(context=context)
server.login(sender, app_password)  # MUST be App Password, not regular password
server.sendmail(sender, recipient, msg.as_string())
server.quit()
```

### SMTP Error Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Authentication unsuccessful` (535) | Wrong password or App Password needed | Guide user to create App Password |
| `Username and Password not accepted` | Regular password used instead of App Password | Must use App Password (16 chars) |
| `Connection timed out` | Port/firewall blocked | Try port 465 with SMTP_SSL instead of 587 |

## Python-docx Helper Patterns

### Imports
```python
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
```

### Key Functions to Include in Every Script
```python
def h0(text):   # Title heading (level=0, 22pt, dark blue)
def h1(text):   # Section heading (level=1, 16pt, medium blue)
def h2(text):   # Subsection heading (level=2, 13pt, medium blue)
def addp(text, bold=False, italic=False, bullet=False):
def addbp(bold_text, normal_text):  # Bold prefix + normal text
def addtable(headers, rows):        # Formatted table with Light Grid Accent 1 style
```

### Style Setup
```python
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3)
    section.right_margin = Cm(3)
```

## Pitfalls

1. **Python path issues on Windows**: `python-docx` may be installed in Anaconda but not in the default `python`. Always use the full path: `/c/Users/eymen/anaconda3/python.exe`. The hermes-agent venv has NO pip — use Anaconda's pip for package installation.
2. **Unicode in file paths**: Turkish characters (ü, ı, ş, ç, ö, ğ) in save paths cause `FileNotFoundError` in python-docx. Workaround: save to Temp first, then `cp` to the real path.
3. **curl on Windows/git-bash**: `curl` works in git-bash. Use `-sL` flags (silent, follow redirects). Add `-o` for output filename.
4. **Long Python one-liners in terminal**: Don't inline long Python scripts via `-c` — write to a `.py` file first using `write_file`, then execute it via the correct interpreter.
5. **web_extract timeout**: Some pages are large. If content is truncated, use additional `web_search` calls to find more specific sources.
6. **execute_code vs terminal**: The sandboxed `execute_code` may not share the same Python environment as `terminal`. When python-docx is only in Anaconda, `execute_code` won't find it. Use `terminal` with the full interpreter path instead.
7. **Gmail App Password loop**: If the user keeps giving their regular password despite repeated explanations, switch strategy — offer Telegram media upload or manual file path delivery instead of continuing to try SMTP.
