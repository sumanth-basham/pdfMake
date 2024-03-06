import fitz  # Import PyMuPDF

def add_notebook_lines_to_pdf(input_pdf_path, output_pdf_path, skip_pages=None):
    original_pdf = fitz.open(input_pdf_path)
    new_pdf = fitz.open()

    if skip_pages is None:
        skip_pages = []

    # Parameters for notebook lines
    line_distance = 50  # Distance between lines, adjust as needed
    margin = 10  # Margin for the notebook lines, adjust as needed

    for page_num in range(len(original_pdf)):
        if page_num in skip_pages or any(start <= page_num <= end for start, end in skip_pages):
            # Copy the page without adding lines if it's in the skip list
            original_page = original_pdf.load_page(page_num)
            new_page = new_pdf.new_page(width=original_page.rect.width, height=original_page.rect.height)
            new_page.show_pdf_page(new_page.rect, original_pdf, page_num)
            continue

        original_page = original_pdf.load_page(page_num)
        # Create a new PDF page in landscape mode with twice the width to accommodate the ruled lines
        new_page = new_pdf.new_page(width=original_page.rect.width * 2, height=original_page.rect.height)

        # Define the area to insert the original page content (left half)
        clip_rect = fitz.Rect(0, 0, original_page.rect.width, original_page.rect.height)
        new_page.show_pdf_page(clip_rect, original_pdf, page_num)

        # Adjusting top and bottom margins for the lines
        top_margin = line_distance * 1.25  # Two lines space at the top
        bottom_margin = original_page.rect.height - line_distance * 1.25  # Two lines space at the bottom

        # Add horizontal ruled lines across the right half, with top and bottom spacing
        for y in range(int(top_margin), int(bottom_margin), line_distance):
            start_point = (original_page.rect.width + margin, y)
            end_point = (original_page.rect.width * 2 - margin, y)
            new_page.draw_line(start_point, end_point)

        # Add a vertical line for the margin
        new_page.draw_line((original_page.rect.width + margin, top_margin),
                           (original_page.rect.width + margin, bottom_margin))

    new_pdf.save(output_pdf_path)

# Example usage
add_notebook_lines_to_pdf("ML_Mastery_Python.pdf", "ML_4.pdf", skip_pages=[(0, 9)])
