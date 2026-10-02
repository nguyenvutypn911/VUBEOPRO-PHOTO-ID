import streamlit as st
from rembg import remove
from PIL import Image
import io

# Cấu hình giao diện
st.set_page_config(page_title="App Ảnh Thẻ VubeoPro", layout="centered")
st.title("📸 App Tạo Ảnh Thẻ Tự Động")
st.write("Dành cho VubeoPro - Tách nền & Chỉnh cỡ ảnh")

# 1. Chọn ảnh
uploaded_file = st.file_uploader("Bước 1: Chọn ảnh từ máy của bạn", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Ảnh bạn vừa tải lên", width=300)
    
    # 2. Tùy chỉnh
    color = st.sidebar.radio("Bước 2: Chọn màu nền", ["Xanh dương", "Trắng"])
    bg_color = (0, 61, 113) if color == "Xanh dương" else (255, 255, 255)
    
    size_option = st.sidebar.selectbox("Bước 3: Chọn kích thước", ["3x4 cm", "4x6 cm"])
    target_size = (354, 472) if size_option == "3x4 cm" else (472, 709)

    # 3. Nút bấm xử lý
    if st.button("Bắt đầu tạo ảnh thẻ"):
        with st.spinner('Đang tách nền... vui lòng đợi tí nhé'):
            # Xử lý tách nền bằng AI
            input_data = uploaded_file.getvalue()
            output_data = remove(input_data)
            subject = Image.open(io.BytesIO(output_data)).convert("RGBA")
            
            # Tạo nền màu và ghép ảnh
            canvas = Image.new("RGBA", subject.size, bg_color)
            canvas.paste(subject, (0, 0), mask=subject)
            
            # Chỉnh về kích thước chuẩn
            final_img = canvas.convert("RGB").resize(target_size, Image.LANCZOS)
            
            # Hiển thị kết quả
            st.image(final_img, caption="Ảnh thẻ đã làm xong!")
            
            # Nút tải về
            buf = io.BytesIO()
            final_img.save(buf, format="JPEG", quality=95)
            st.download_button("Tải Ảnh Thẻ Về Máy", buf.getvalue(), "anh_the_vubeo.jpg", "image/jpeg")
