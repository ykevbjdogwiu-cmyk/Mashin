import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Masheni Box Studio", layout="centered")

st.title("🛍️ استوديو تعديل صور المنتجات الذكي")
st.write("ارفع صورة المنتج، وسيقوم الذكاء الاصطناعي بإعادة صياغتها وتنسيقها كصورة احترافية.")

api_key = st.text_input("أدخل مفتاح Google Gemini API Key:", type="password")

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
        "on the mid-right, and an artistic magazine corner in the bottom-left. Lighting is bright, soft, and natural daylight "
        "coming from the side, creating gentle and realistic shadows. Digitally ironed and smoothed out, free of wrinkles. "
        "High-end fashion catalog style, photorealistic, hyper-detailed."
    )
    
    prompt = st.text_area("تعليمات التنسيق (البرومبت):", value=default_prompt, height=150)
    
    if st.button("🚀 ابدأ معالجة وتوليد الصورة الاحترافية"):
        if not api_key:
            st.error("الرجاء إدخال مفتاح الـ API أولاً.")
        else:
            with st.spinner("جاري معالجة الصورة وإعادة تنسيقها... يرجى الانتظار قليلاً"):
                try:
                    genai.configure(api_key=api_key)
                    # استخدام النموذج المناسب للتعامل مع الصور والمهام البصرية
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # إرسال الصورة والطلب
                    response = model.generate_content([prompt, image])
                    
                    st.success("تمت المعالجة بنجاح!")
                    
                    # محاولة عرض النتيجة إذا تضمنت صورة أو عرض النص الإرشادي بدقة
                    try:
                        # في حال عاد النموذج بصورة أو بيانات بصرية
                        st.image(response.text, caption="الصورة الناتجة المنسقة")
                    except:
                        # عرض النص والنتيجة التي أنتجها النموذج لتوضيح الخطوة التالية
                        st.markdown(response.text)
                        
                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")
