import streamlit as st
from PIL import Image
import google.generativeai as genai
import base64
io_bytes = None

st.set_page_config(page_title="Masheni Box Studio", layout="centered")

st.title("🛍️ استوديو تعديل وتوليد صور المنتجات الذكي")
st.write("ارفع صورة المنتج، وسيقوم الذكاء الاصطناعي بمعالجتها وتوليد الصورة الاحترافية المنسقة فوراً.")

# مفتاح الـ API الخاص بك
api_key = "AIzaSyDqq2enocDxR8NSUtJ2oCC-oiWRKVnxeL4"

uploaded_file = st.file_uploader("اختر صورة المنتج (ملابس، فستان، قميص...)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="الصورة الأصلية للمنتج", use_container_width=True)
    
    default_prompt = (
        "Professional e-commerce flat lay photography. The exact clothing product from the uploaded image "
        "must be perfectly preserved with its original color, fabric texture, and details, neatly and aesthetically arranged "
        "in the center. The background is a luxurious, soft white textured linen bedsheet. Surrounding the main garment "
        "are high-end branding props placed harmoniously: a bunch of delicate white baby's breath flowers in the top-left corner, "
        "a glass bottle of perfume on the middle-left, a beige satin scrunchie in the top-right, a small gold dish with jewelry "
        "on the mid-right. Lighting is bright, soft, and natural daylight. High-end fashion catalog style, photorealistic."
    )
    
    prompt = st.text_area("تعليمات التنسيق (البرومبت):", value=default_prompt, height=150)
    
    if st.button("🚀 توليد وتصدير الصورة الاحترافية"):
        if not api_key:
            st.error("الرجاء التأكد من مفتاح الـ API.")
        else:
            with st.spinner("جاري معالجة وتوليد الصورة الاحترافية عبر الذكاء الاصطناعي... يرجى الانتظار"):
                try:
                    genai.configure(api_key=api_key)
                    
                    # استخدام نموذج متطور يدعم المخرجات البصرية أو استدعاء التنسيق المناسب
                    model = genai.GenerativeModel('gemini-3.6-flash')
                    
                    response = model.generate_content([
                        "Generate a styled e-commerce flat lay image based on this prompt and input image: " + prompt, 
                        image
                    ])
                    
                    st.success("تمت المعالجة بنجاح!")
                    
                    # فحص واستخراج الصورة الناتجة من الاستجابة البرمجية
                    image_generated = False
                    if hasattr(response, 'candidates') and response.candidates:
                        for candidate in response.candidates:
                            if hasattr(candidate, 'content') and candidate.content.parts:
                                for part in candidate.content.parts:
                                    if hasattr(part, 'inline_data') and part.inline_data:
                                        image_data = base64.b64decode(part.inline_data.data)
                                        from io import BytesIO
                                        out_img = Image.open(BytesIO(image_data))
                                        st.image(out_img, caption="الصورة الاحترافية المنسقة الناتجة", use_container_width=True)
                                        
                                        # زر تحميل الصورة مباشرة
                                        buf = BytesIO()
                                        out_img.save(buf, format="PNG")
                                        byte_im = buf.getvalue()
                                        st.download_button(
                                            label="📥 تحميل الصورة النهائية",
                                            data=byte_im,
                                            file_name="styled_flat_lay_product.png",
                                            mime="image/png"
                                        )
                                        image_generated = True
                                        break
                    
                    if not image_generated:
                        # في حال عاد الاستجابة بنص وصف أو توجيه بصري
                        st.markdown(response.text)
                        st.info("ملاحظة: يمكنك استخدام الوصف أعلاه لتوليد النتيجة البصرية بدقة عالية.")
                        
                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة والتوليد: {e}")
