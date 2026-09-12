import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO

st.set_page_config(page_title="Masheni Box Studio", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #4B2E2B; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("📦 Masheni Box Studio - دمج وتوليد الصور")
st.write("ارفع صورة ملابسك، وسي进行了 الدمج الفوري لتظهر بتنسيق Flat Lay الاحترافي.")

# رفع صورة المنتج
uploaded_file = st.file_uploader("اختر صورة المنتج (PNG أو JPG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # فتح صورة المنتج الأصلية
    product_img = Image.open(uploaded_file).convert("RGBA")
    st.image(product_img, caption="صورة المنتج الأصلية", use_container_width=True)
    
    if st.button("🚀 دمج وتوليد صورة الاستوديو الاحترافية"):
        with st.spinner("جاري دمج المنتج وتنسيقه مع خلفية الاستوديو..."):
            try:
                # 1. إنشاء خلفية استوديو احترافية (لون بيج ناعم أو أبيض كتاني دافئ)
                studio_width, studio_height = 1000, 1000
                background = Image.new("RGBA", (studio_width, studio_height), (245, 243, 240, 255))
                
                # 2. تغيير حجم صورة المنتج لتناسب التنسيق الاحترافي (مثلاً عرض 500 بكسل مع الحفاظ على الأبعاد)
                basewidth = 500
                wpercent = (basewidth / float(product_img.size[0]))
                hsize = int(float(product_img.size[1]) * float(wpercent))
                product_resized = product_img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
                
                # 3. حساب إحداثيات التمركز ليكون المنتج في منتصف الخلفية تماماً
                pos_x = (studio_width - basewidth) // 2
                pos_y = (studio_height - hsize) // 2
                
                # 4. دمج المنتج فوق الخلفية الاستوديو
                background.paste(product_resized, (pos_x, pos_y), product_resized)
                
                # تحويل النتيجة النهائية إلى صيغة تظهر في المتصفح وتحمل
                final_output = background.convert("RGB")
                
                st.success("تم دمج وتوليد الصورة الاحترافية بنجاح!")
                st.image(final_output, caption="الصورة النهائية بتنسيق الاستوديو", use_container_width=True)
                
                # زر التحميل المباشر
                buf = BytesIO()
                final_output.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 تحميل الصورة النهائية بجودة عالية",
                    data=byte_im,
                    file_name="masheni_flat_lay_studio.jpg",
                    mime="image/jpeg"
                )
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء عملية الدمج: {e}")
