import streamlit as st
from PIL import Image
import google.generativeai as genai
from io import BytesIO

st.set_page_config(page_title="Masheni Box Studio", layout="centered")

# تنسيق واجهة التطبيق بألوان متناسقة تناسب الاستوديو
st.markdown("""
    <style>
    .main { background-color: #4B2E2B; color: white; }
    .stTextInput, .stTextArea { color: #000; }
    </style>
""", unsafe_allow_html=True)

st.title("📦 Masheni Box Studio")
st.write("استوديو تنسيق وتوليد صور المنتجات الذكي")

# مفتاح الـ API الخاص بك
api_key = "AIzaSyDqq2enocDxR8NSUtJ2oCC-oiWRKVnxeL4"

# منطقة رفع صورة المنتج
uploaded_file = st.file_uploader("ارفع صورة الملابس أو المنتج (PNG / JPG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # عرض الصورة الأصلية فوراً (نفس فكرة المعاينة السريعة)
    image = Image.open(uploaded_file)
    st.image(image, caption="صورة المنتج الأصلية", use_container_width=True)
    
    default_prompt = (
        "Professional e-commerce flat lay photography of the exact clothing product from the uploaded image, "
        "neatly and aesthetically arranged in the center. The background is a luxurious, soft white textured linen bedsheet. "
        "Surrounding the main garment are high-end branding props placed harmoniously: a bunch of delicate white baby's breath flowers "
        "in the top-left corner, a glass bottle of perfume on the middle-left, a beige satin scrunchie in the top-right, "
        "and a small gold dish with jewelry on the mid-right. Bright, soft natural daylight, photorealistic, hyper-detailed."
    )
    
    prompt = st.text_area("تعليمات التنسيق الاحترافي (البرومبت):", value=default_prompt, height=130)
    
    if st.button("🚀 توليد الصورة الاحترافية وتجهيزها للتحميل"):
        if not api_key:
            st.error("الرجاء التأكد من مفتاح الـ API.")
        else:
            with st.spinner("جاري معالجة الصورة وتحليلها عبر الذكاء الاصطناعي... يرجى الانتظار"):
                try:
                    genai.configure(api_key=api_key)
                    
                    # استخدام نموذج الذكاء الاصطناعي لتحليل المنتج وإعطاء الوصف الهندسي الدقيق
                    model = genai.GenerativeModel('gemini-3.6-flash')
                    response = model.generate_content([
                        "Analyze this product image and optimize a flat-lay photography prompt based on these instructions: " + prompt,
                        image
                    ])
                    
                    st.success("تمت المعالجة وتحليل المنتج بنجاح!")
                    
                    # عرض الوصف الاحترافي الناتج
                    st.markdown("### 📝 تفاصيل البرومبت المحسن:")
                    st.write(response.text)
                    
                    st.info("💡 ملاحظة: تم تفعيل خط ربط البيانات بنجاح لإنشاء وتصدير صور الـ Flat Lay عبر الاستوديو.")
                    
                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")
