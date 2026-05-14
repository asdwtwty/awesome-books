"""
Minimal DOCX generator without python-docx dependency.
Creates valid .docx (OOXML) files using only stdlib zipfile + xml.
"""
import zipfile
import os

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="44"/><w:szCs w:val="44"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="240" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr><w:spacing w:before="200" w:after="60"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Code">
    <w:name w:val="Code"/>
    <w:pPr><w:spacing w:before="60" w:after="60"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr>
  </w:style>
</w:styles>'''

NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="-"/><w:lvlJc w:val="left"/></w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>'''


def escape_xml(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


class DocxWriter:
    def __init__(self):
        self.body_parts = []
    
    def add_heading(self, text, level=1):
        style = f"Heading{level}"
        self.body_parts.append(
            f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>'
            f'<w:r><w:t>{escape_xml(text)}</w:t></w:r></w:p>'
        )
    
    def add_paragraph(self, text, bold=False):
        rpr = '<w:rPr><w:b/></w:rPr>' if bold else ''
        self.body_parts.append(
            f'<w:p><w:r>{rpr}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>'
        )
    
    def add_bullet(self, text):
        self.body_parts.append(
            '<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r></w:p>'
        )
    
    def add_code_block(self, lines):
        for line in lines:
            self.body_parts.append(
                '<w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr>'
                f'<w:r><w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="18"/></w:rPr>'
                f'<w:t xml:space="preserve">{escape_xml(line)}</w:t></w:r></w:p>'
            )
    
    def add_table(self, headers, rows):
        """Add a simple table."""
        cols = len(headers)
        col_w = 9000 // cols  # distribute width
        
        tbl = '<w:tbl><w:tblPr><w:tblBorders>'
        for b in ['top','left','bottom','right','insideH','insideV']:
            tbl += f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        tbl += '</w:tblBorders></w:tblPr><w:tblGrid>'
        for _ in range(cols):
            tbl += f'<w:gridCol w:w="{col_w}"/>'
        tbl += '</w:tblGrid>'
        
        # header row
        tbl += '<w:tr>'
        for h in headers:
            tbl += (f'<w:tc><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr>'
                    f'<w:p><w:r><w:rPr><w:b/></w:rPr><w:t>{escape_xml(h)}</w:t></w:r></w:p></w:tc>')
        tbl += '</w:tr>'
        
        # data rows
        for row in rows:
            tbl += '<w:tr>'
            for cell in row:
                tbl += f'<w:tc><w:p><w:r><w:t xml:space="preserve">{escape_xml(str(cell))}</w:t></w:r></w:p></w:tc>'
            tbl += '</w:tr>'
        
        tbl += '</w:tbl>'
        self.body_parts.append(tbl)
        # add spacing after table
        self.body_parts.append('<w:p/>')
    
    def add_empty_line(self):
        self.body_parts.append('<w:p/>')
    
    def save(self, filepath):
        body_xml = '\n'.join(self.body_parts)
        document_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body>{body_xml}</w:body></w:document>'
        )
        
        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('[Content_Types].xml', CONTENT_TYPES)
            zf.writestr('_rels/.rels', RELS)
            zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
            zf.writestr('word/document.xml', document_xml)
            zf.writestr('word/styles.xml', STYLES)
            zf.writestr('word/numbering.xml', NUMBERING)
        
        return filepath
