## Post AG - Vorlage mit Absender Letter Template using ReportLab
# Last update: 2023-09-03


"""
About: Fill variables (of a given dataset input) into the Austrian Post AG - Vorlage mit Absender letter template using ReportLab library in Python.

Template: https://www.einfach-brief.at/fe/vorlagen
"""


###############
# Initial Setup
###############

# Erase all declared global variables
globals().clear()


# Import packages
import os
import re

from babel.dates import format_date
import pandas as pd
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, KeepInFrame, Table, TableStyle


# Set working directory
# os.chdir(path=os.path.join(os.path.expanduser('~'), 'Downloads'))


###########
# Functions
###########


def create_table_frame(
    *,
    document,
    text,
    frameWidth,
    frameHeight,
    frameHPosition,
    frameVPosition,
    fontName='Arial',
    fontSize=11,
    textColor='black',
    textHAlign=TA_LEFT,
    textVAlign='TOP',
    textLeftPadding=0,
    textRightPadding=0,
    textTopPadding=0,
    textBottomPadding=0,
    showBoundary=True,
):
    """All flowables have an hAlign property: ('LEFT', 'RIGHT', 'CENTER' or 'CENTRE'). For paragraphs, which fill the full width of the frame, this has no effect."""
    ## Text

    # Add HTML paragraph breaks
    text = re.sub(pattern=r'\n', repl='<br/>', string=text)

    # Create ReportLab Paragraph object and apply font styles to text
    text = Paragraph(
        text,
        ParagraphStyle(
            name='',
            fontName=fontName,
            fontSize=fontSize,
            leading=(12 if fontSize >= 10 else 9),
            textColor=textColor,
            alignment=textHAlign,
        ),
        encoding='utf-8',
    )

    # In case of long text: shrink to fit inside table frame
    text = KeepInFrame(
        maxWidth=0,
        maxHeight=0,
        content=[text],
        mode='shrink',
        # hAlign=textHAlign,
        # vAlign=textVAlign,
        # fakeWidth=False,
    )

    ## Table

    # Create ReportLab Table object
    table = Table(
        data=[[text]],
        colWidths=frameWidth,
        rowHeights=frameHeight,
        spaceBefore=0,
        spaceAfter=0,
        # hAlign=textHAlign,
        # vAlign=textVAlign,
    )

    # Set table style
    table.setStyle(
        TableStyle(
            [
                ('LEFTPADDING', (0, 0), (-1, -1), textLeftPadding),
                ('RIGHTPADDING', (0, 0), (-1, -1), textRightPadding),
                ('TOPPADDING', (0, 0), (-1, -1), textTopPadding),
                ('BOTTOMPADDING', (0, 0), (-1, -1), textBottomPadding),
                ('VALIGN', (0, 0), (-1, -1), textVAlign),
            ],
        ),
    )

    # Horizontal alignment
    # if textHAlign == TA_CENTER:
    #     table.setStyle(TableStyle([
    #         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #     ]))
    # if textHAlign == TA_LEFT or textHAlign == TA_JUSTIFY:
    #     table.setStyle(TableStyle([
    #         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    #     ]))
    # else:
    #     pass

    # Show boundary
    if showBoundary is True:
        table.setStyle(
            TableStyle(
                [
                    ('GRID', (0, 0), (-1, -1), 0.5, 'black'),
                ],
            ),
        )

    else:
        pass

    table.wrap(0, 0)

    # Table location
    table.drawOn(document, frameHPosition, (A4[1] - frameVPosition - frameHeight))


def create_document(
    *,
    df,
    title,
    author='',
    output_directory,
    file_name='Output.pdf',
    subject='',
):
    # Create document
    document = Canvas(
        filename=os.path.join(output_directory, file_name),
        pagesize=A4,
        bottomup=1,
        pdfVersion=(1, 4),
    )
    document.setAuthor(author)
    document.setSubject(subject)
    document.setTitle(title)
    document.setCreator('')
    document.setProducer('')

    # Load Arial font
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arialbd.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Oblique', 'Ariali.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-BoldOblique', 'Arialbi.ttf'))

    pdfmetrics.registerFontFamily(
        'Arial',
        normal='Arial',
        bold='Arial-Bold',
        italic='Arial-Oblique',
        boldItalic='Arial-BoldOblique',
    )

    for index, row in df.iterrows():
        ### Document contents

        ## Title

        # Text
        text = """Max Mustermann
        Musterstr. 123 · 12345 Musterort"""

        # Create table frame
        create_table_frame(
            document=document,
            text=text,
            fontName='Arial',
            fontSize=12,
            textHAlign=TA_CENTER,
            textVAlign='MIDDLE',
            frameWidth=16 * cm,
            frameHeight=1.54 * cm,
            frameHPosition=2.5 * cm,
            frameVPosition=1.9 * cm,
            showBoundary=False,
        )

        ## Adressfeld Absender/Einschreiben

        # Text
        text = """Max Mustermann, Musterstr. 123, 12345 Musterort <i>(optional)</i>"""

        # Create table frame
        create_table_frame(
            document=document,
            text=text,
            fontName='Arial',
            fontSize=8,
            textHAlign=TA_LEFT,
            textVAlign='BOTTOM',
            textLeftPadding=0.5 * cm,
            textRightPadding=0.1 * cm,
            textTopPadding=0.3 * cm,
            textBottomPadding=0.1 * cm,
            frameWidth=9 * cm,
            frameHeight=1.5 * cm,
            frameHPosition=2 * cm,
            frameVPosition=4.7 * cm,
            showBoundary=False,
        )

        ## Adressfeld Adressblock

        # Text
        text = (
            """{gender}{name}
        {street}
        {postal_code} {city}
        {country}"""
        ).format(
            name=row['name'],
            gender='Frau '
            if row['gender'] == 'F'
            else ('Herr ' if row['gender'] == 'M' else ''),
            country=row['location_country'].upper(),
            postal_code=row['location_postal_code'],
            city=row['location_city'],
            street=row['location_street'],
        )

        # Create table frame
        create_table_frame(
            document=document,
            text=text,
            fontName='Arial',
            fontSize=11,
            textHAlign=TA_LEFT,
            textVAlign='MIDDLE',
            textLeftPadding=0.5 * cm,
            textRightPadding=2.5 * cm,  # Post Matrixcode Frankierung margin
            textTopPadding=0.1 * cm,
            textBottomPadding=0.1 * cm,
            frameWidth=9 * cm,
            frameHeight=3.1 * cm,
            frameHPosition=2 * cm,
            frameVPosition=6.2 * cm,
            showBoundary=False,
        )

        ## Date

        # Create variables
        city = 'Musterort'
        date = pd.Timestamp.now(tz='CET').date()

        # Text
        text = ("""{city}{date}""").format(
            city=city + ', ' if city != '' else '',
            # date=date.strftime('%d. %B %Y'),
            date=format_date(date, format='dd. MMMM yyyy', locale='de_DE'),
        )

        # Create table frame
        create_table_frame(
            document=document,
            text=text,
            fontName='Arial',
            fontSize=11,
            textHAlign=TA_RIGHT,
            textVAlign='TOP',
            frameWidth=6 * cm,
            frameHeight=0.5 * cm,
            frameHPosition=A4[0] - 2.5 * cm - 6 * cm,
            frameVPosition=9.8 * cm,
            showBoundary=False,
        )

        ## Inhalt

        # Text
        text = """<b>Betreff: Briefvorlage Standard mit Absender</b>


        Sehr geehrte*r Anwender*in der Tages-Post,

        bei diesem Dokument handelt es sich um eine einfache Vorlage für einen Brief, der über www.tages-post.at versendet werden kann und den Bestimmungen der Österreichischen Post bezüglich der Platzierung der Empfänger*innenadresse auf dem Briefbogen entspricht.

        Löschen Sie diesen Hinweis und ersetzen Sie den Text durch den von Ihnen gewünschten Text. Speichern Sie den Brief abschließend als PDF-Datei ab.

        <b>Das Anschriftenfeld:</b> Dieses haben wir in dieser Vorlage fest „verankert“, sodass es nicht verrutschen kann. Im Anschriftenfeld haben Sie insgesamt sechs Zeilen plus eine Zeile für die Rücksendeangabe zur Verfügung. Das Anschriftenfeld sollte einen Abstand von 6,2 cm vom oberen Seitenrand haben, damit es deutlich in einem Fenster-Kuvert sichtbar ist.
        *Wenn Sie Sendungen ins Ausland versenden, bitte das Land in GROSSBUCHSTABEN anführen.

        <b>Schriftarten, -größen und -stile:</b>
        Verwenden Sie zugunsten der Lesbarkeit im fortlaufenden Text keine Schrift, die kleiner als 10 Punkt ist, sowie keine ausgefallenen Schriftarten, wie zum Beispiel Schreibschrift. Verzichten Sie auf ausgefallene Schriftstile, wie zum Beispiel Kapitälchen im fortlaufenden Text. Wir empfehlen folgende Schriftarten: Arial, Times, Calibri und Helvetica

        Wir wünschen Ihnen viel Erfolg bei der Verfassung Ihrer Briefe. Laden Sie hierzu einfach Ihren abgespeicherten Brief im PDF-Format über www.tages-post.at hoch und wir drucken und versenden diesen gerne für Sie.

        Mit freundlichen Grüßen
        Ihr Tages-Post Team
        """

        # Create table frame
        create_table_frame(
            document=document,
            text=text,
            fontName='Arial',
            fontSize=11,
            textHAlign=TA_JUSTIFY,
            textVAlign='TOP',
            frameWidth=16 * cm,
            frameHeight=16.95 * cm,
            frameHPosition=2.5 * cm,
            frameVPosition=10.75 * cm,
            showBoundary=False,
        )

        document.showPage()

    # Save document
    document.save()


#########################
# AT Post Letter Template
#########################

# Create example DataFrame with names, gender and addresses
df = pd.DataFrame(
    data=[
        [
            'Eva Muster',
            'F',
            'Österreich',
            'Musterbundesland',
            '9875',
            'Musterstadt',
            'Musterstraße 1',
        ],
        [
            'Max Mustermann',
            'M',
            'Österreich',
            'Musterbundesland',
            '9875',
            'Musterstadt',
            'Musterstraße 1',
        ],
        [
            'Firma ABC',
            '',
            'Österreich',
            'Musterbundesland',
            '9875',
            'Industriestadt',
            'Industriestraße 1',
        ],
    ],
    index=None,
    columns=[
        'name',
        'gender',
        'location_country',
        'location_state',
        'location_postal_code',
        'location_city',
        'location_street',
    ],
    dtype=None,
)

# Create .pdf document
create_document(
    df=df,
    title='Post AG - Vorlage mit Absender',
    author='Post AG',
    output_directory=os.path.join(os.path.expanduser('~'), 'Downloads'),
    file_name='Post AG - Vorlage mit Absender.pdf',
)
