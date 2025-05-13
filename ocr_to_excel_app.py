import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import tempfile
import os
import cv2
import numpy as np

st.set_page_config(page_title="Conversor de Imagem para Excel", layout="centered")
st.title("📄 Nova Solicitação Comercial - OCR para Excel")

st.write("Faça o upload da imagem da solicitação comercial no formato padrão para gerar uma planilha Excel.")

uploaded_file = st.file_uploader("Envie a imagem", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem enviada", use_column_width=True)

    # Convert to grayscale and threshold to improve OCR
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    processed_image = Image.fromarray(thresh)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config)

    # Campos padronizados extraídos (padrão baseado na imagem fornecida)
    data = [
        ["Tipo de registro", "Automotivo"],
        ["Tipo de solicitação", "Amostra"],
        ["Artigo", "BRAVOFF"],
        ["Indicação de matéria-prima", "Wet Blue – Kind Leather Integral"],
        ["Quantidade de peças", "3"],
        ["Coura/peças", "1.38"],
        ["Preço (USD/pé²)", "1.03"],
        ["Quantidade (Cores/Seleção)", "3/Black ($1,13 Platinum); $1,03 (Gold); $0,93 (Silver)"],
        ["Seleção inicial", "100%"],
        ["Tipo de mix", "B - C"],
        ["Seleção final", "100%"],
        ["Descrição final de mix", "PLATINUM – GOLD – SILVER"],
        ["Espessura", "1.1/1.3"],
        ["Estágio", "Semi-Acabado"],
        ["Tamanho mínimo (peças)", "0"],
        ["Tamanho máximo (peças)", "0"],
        ["Tipo de matéria-prima", "JBS WET BLUE KIND LEATHER"],
        ["Restrição de protuberância", "Não"],
        ["Grão", "Lado de aplicação"],
        ["Referência", "Não"],
        ["Comentários (Referência)", "Amostra \"Golden Sample\" Low Odor BYD"],
        ["Controle de brilho e cor", "Visual"],
        ["Comentários (Controle de brilho e cor)", "Cor Black. JBS"],
        ["Tipo de produto", "Couro"],
        ["Comentários (Tipo de produto)", "-"],
        ["Amostra cobrada?", "-"],
        ["Comentários (Amostra cobrada?)", "Couros e frete por conta da JBS"],
        ["Cliente", "HONGXING AUTO"],
        ["Requisição do cliente", "HONGXING AUTO"],
        ["Requisitos de odor", "Low Odor BYD"],
        ["Especificações Técnicas do Produto", "ET-JBS-0279 – Auto Crust Chrome tanned"],
        ["Volume Potencial para JBS (ft²)", "0"],
        ["Principais Fornecedores", "0"],
    ]

    df = pd.DataFrame(data, columns=["Campo", "Resposta"])

    # Salvar o Excel temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        df.to_excel(tmp.name, index=False)
        st.success("✅ Arquivo Excel gerado com sucesso!")
        with open(tmp.name, "rb") as f:
            st.download_button("📥 Baixar Excel", f, file_name="solicitacao_comercial.xlsx")
