import streamlit as st
from PIL import Image
import google.generativeai as genai
import urllib.parse
from io import BytesIO
import requests

st.set_page_config(page_title="Masheni Box Studio - استوديو الفلات لاي", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #4B2E2B; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ Masheni Box Studio - استوديو تنسيق المنتجات")
st.write("ارفع صورة ملابسك، وسيقوم الذكاء الاصطناعي بوضعها داخل خلفية الاستوديو الاحترافية (Flat Lay) تماماً مثل الصور الإعلانية الفاخرة.")

# مفتاح الـ API الخاص بك
api_key = "AIzaSyDqq2enocDxR8NSUtJ2oCC-oiWRKVnxeL4"

# رفع صورة المنتج
uploaded_file = st.file_uploader("اختر صورة قطعة الملابس...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="صورة المنتج الأصلية", use_container_width=True)
    
    if st.button("🚀 تحويل وتنسيق الصورة بنفس النمط الاحترافي"):
        if not api_key:
            st.error("الرجاء التأكد من مفتاح الـ API.")
        else:
            with st.spinner("جاري دمج وتنسيق قطعة الملابس داخل الاستوديو الاحترافي... يرجى الانتظار"):
                try:
                    genai.configure(api_key=api_key)
                    
                    # الخطوة 1: تحليل دقيق لقطعة الملابس وتوجيهها لتطابق النمط المطلوب بدقة
                    model = genai.GenerativeModel('gemini-3.6-flash')
                    analysis_response = model.generate_content([
                        "Analyze this clothing item precisely (color, exact fabric, straps, lace, or details). "
                        "Write a professional e-commerce flat lay photography prompt featuring this exact item beautifully and neatly arranged "
                        "in the center on a luxurious soft white textured linen bedsheet background. "
                        "Surrounding items must include: a bunch of delicate white baby's breath flowers, a glass perfume bottle (like Chanel), "
                        "a beige satin scrunchie in the top-right, and a small gold dish with jewelry on the right side. "
                        "Bright natural lighting, high-end commercial fashion catalog style, photorealistic, 8k.",
                        image
                    ])
                    
                    image_prompt = analysis_response.text.strip()
                    
                    # الخطوة 2: إرسال الطلب لمحرك الرسم لتوليد الصورة المطابقة للنمط الفاخر
                    encoded_prompt = urllib.parse.quote(image_prompt)
                    ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1000&height=1000&nologo=true"
                    
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    img_response = requests.get(ai_image_url, headers=headers, timeout=35)
                    
                    if img_response.status_code == 200 and len(img_response.content) > 1000:
                        generated_img = Image.open(BytesIO(img_response.content))
                        
                        st.success("تم تنسيق وتوليد الصورة الاحترافية بنجاح!")
                        st.image(generated_img, caption="الصورة النهائية بنفس نمط الاستوديو الاحترافي", use_container_width=True)
                        
                        # زر التحميل المباشر
                        buf = BytesIO()
                        generated_img.save(buf, format="JPEG", quality=95)
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label="📥 تحميل الصورة النهائية بجودة عالية",
                            data=byte_im,
                            file_name="masheni_studio_flat_lay.jpg",
                            mime="image/jpeg"
                        )
                    else:
                        st.error("عذراً، حدث تأخير في الاستجابة من خادم الرسم. يرجى المحاولة مرة أخرى بالنقر على الزر.")
                        
                except Exception as e:
                    st.error(f"حدث خطأ أثناء المعالجة: {e}")
