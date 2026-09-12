import streamlit as st
from PIL import Image
import google.generativeai as genai
import urllib.parse
from io import BytesIO
import requests

st.set_page_config(page_title="Masheni Box Studio - الاستوديو الذكي", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #4B2E2B; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ استوديو توليد وتعديل صور المنتجات بالذكاء الاصطناعي")
st.write("ارفع صورة ملابسك، وسيقوم الذكاء الاصطناعي برسمها وتنسيقها بتفاصيل Flat Lay الاحترافية فوراً.")

# مفتاح الـ API الخاص بك
api_key = "AIzaSyDqq2enocDxR8NSUtJ2oCC-oiWRKVnxeL4"

# رفع صورة المنتج
uploaded_file = st.file_uploader("اختر صورة قطعة الملابس (تيشيرت، قميص، فستان...)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="صورة المنتج الأصلية", use_container_width=True)
    
    if st.button("🚀 توليد ورسم الصورة النهائية بالذكاء الاصطناعي"):
        if not api_key:
            st.error("الرجاء التأكد من مفتاح الـ API.")
        else:
            with st.spinner("جاري تحليل وتوليد الصورة الاحترافية بالذكاء الاصطناعي... يرجى الانتظار"):
                try:
                    genai.configure(api_key=api_key)
                    
                    # الخطوة 1: تحليل صورة الملابس بدقة عبر Gemini
                    model = genai.GenerativeModel('gemini-3.6-flash')
                    analysis_response = model.generate_content([
                        "Analyze this clothing image precisely. Describe its exact color, type, and any text, logo, or print on it. Write a professional e-commerce flat lay photography prompt featuring this exact item neatly placed in the center on a luxury white linen background surrounded by elegant fashion props like perfume and flowers, photorealistic, 8k resolution.",
                        image
                    ])
                    
                    image_prompt = analysis_response.text
                    
                    # الخطوة 2: تحويل الوصف الذكي إلى صورة حقيقية مرسومة عبر محرك الرسم بالذكاء الاصطناعي
                    encoded_prompt = urllib.parse.quote(image_prompt)
                    ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1000&height=1000&nologo=true"
                    
                    # جلب الصورة الم تولدة وعرضها
                    img_response = requests.get(ai_image_url)
                    
                    if img_response.status_code == 200:
                        generated_img = Image.open(BytesIO(img_response.content))
                        
                        st.success("تم توليد وتعديل الصورة بنجاح!")
                        st.image(generated_img, caption="الصورة الاحترافية الناتجة بالذكاء الاصطناعي", use_container_width=True)
                        
                        # زر تحميل الصورة النهائية مباشرة
                        buf = BytesIO()
                        generated_img.save(buf, format="JPEG", quality=95)
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label="📥 تحميل الصورة النهائية بجودة عالية",
                            data=byte_im,
                            file_name="masheni_ai_flat_lay.jpg",
                            mime="image/jpeg"
                        )
                    else:
                        st.error("حدث خطأ أثناء معالجة الرسم، يرجى المحاولة مرة أخرى.")
                        
                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")
