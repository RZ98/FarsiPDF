from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display

def create_pdf_with_table(output_file, data):
    def utf8_converter(text):
        rehaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(rehaped_text)
        return bidi_text
    # Register a font that supports Persian characters
    pdfmetrics.registerFont(TTFont('Persian', 'Path_to_your_font_file.ttf'))  # Replace 'Path_to_your_font_file.ttf' with the actual path

    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)

    # Define the style for Persian text
    persian_style = ParagraphStyle(name='PersianStyle', fontName='Persian', alignment=1)  # 1 means center alignment

    # Create a list to hold all the data for the table
    table_data = []

    # Add Persian text
    for row in data:
        table_data.append([Paragraph(utf8_converter(cell), persian_style) for cell in row])

    # Define table
    table = Table(table_data)

    # Define custom style for center alignment
    center_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')])

    # Apply custom style to each cell
    for i in range(len(data)):
        for j in range(len(data[0])):
            table.setStyle(center_style)

    # Add custom style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignment of cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font style for header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header row
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Background color for other rows
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines
    ])

    table.setStyle(style)

    # Build PDF document
    doc.build([table])

# Example data
data = [
    ['نام', 'سن', 'شغل'],
    ['آرمین', '30', 'مهندس نرم‌افزار'],
    ['نگار', '25', 'طراح گرافیک'],
    ['محمد', '35', 'مدیر فنی']
]

# Output PDF file
output_file = "table.pdf"

# Generate PDF with table
create_pdf_with_table(output_file, data)

print("PDF created successfully.")
