import base64
import os
from typing import Literal

import numpy as np
import streamlit as st
from PIL import Image
from pdf2jpg import pdf2jpg # pip install pdf2jpg

# pip install common-utils
# pip install common
from common import create_tmp_sub_folder, try_remove

FOOTER_ROWS = 300
WHITE_VALUE = 255


def crop_white_space(arr: np.array) -> np.array:
    white_pixels = (arr == WHITE_VALUE)
    white_rows = list(np.all(white_pixels, axis=(1, 2)))
    last_non_white_row_idx = max(loc for loc, val in enumerate(white_rows) if not val)
    merged_arr = arr[:last_non_white_row_idx + FOOTER_ROWS]
    return merged_arr


def write_pdf(pdf_path: str, display_method: Literal["iframe", "images"] = "images") -> None:
    if display_method == "images":
        # Create temporary folder for generated image
        tmp_sub_folder_path = create_tmp_sub_folder()

        # Save images in that sub-folder
        result = pdf2jpg.convert_pdf2jpg(pdf_path, tmp_sub_folder_path, pages="ALL")
        images = []
        for image_path in result[0]["output_jpgfiles"]:
            images.append(np.array(Image.open(image_path)))

        # Create merged image from all images + remove irrelevant whitespace
        merged_arr = np.concatenate(images)
        merged_arr = crop_white_space(merged_arr)
        merged_path = os.path.join(tmp_sub_folder_path, "merged.jpeg")
        Image.fromarray(merged_arr).save(merged_path)

        # Display the image
        st.image(merged_path)
        try_remove(tmp_sub_folder_path)
    else:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f"""
            <iframe 
                src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0" 
                width="100%" height="300px" type="application/pdf"
            >
            </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)


def write_test_pdf() -> None:
    pdf_display = f"""
        <embed
          class="pdfobject"
          type="application/pdf"
          title="Embedded PDF"
          src="https://africau.edu/images/default/sample.pdf"
          style="overflow: auto; width: 100%; height: 100%;">            
    """
    st.markdown(pdf_display, unsafe_allow_html=True)


pdf_1 = './res/12-2023/52ª REUNIÃO ORDINÁRIA DO COMITÊ DE OPERAÇÃO E MANUTENÇÃO.pdf'


write_test_pdf()



write_pdf(pdf_1)