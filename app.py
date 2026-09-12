import streamlit as st
from PIL import Image, ImageEnhance
from io import BytesIO
from rembg import remove

st.set_page_config(page_title="Masheni Box Studio - استوديو الفلات لاي", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #4B2E2B; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ Masheni Box Studio - استوديو تنسيق المنتجات")
st.write("ارفع صورة ملابسك، وسيقوم النظام بإزالة الخلفية القديمة ووضعها باحترافية داخل استوديو الفلات لاي الفاخر.")

# رفع صورة المنتج
uploaded_file = st.file_uploader("اختر صورة قطعة الملابس...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="صورة المنتج الأصلية", use_container_width=True)
    
    if st.button("🚀 إزالة الخلفية وتنسيق الصورة باحترافية"):
        with st.spinner("جاري إزالة الخلفية ودمج قطعة الملابس في الاستوديو الفاخر..."):
            try:
                # 1. إزالة الخلفية الأصلية تلقائياً وعزل قطعة الملابس وحدها بشفافية
                input_bytes = uploaded_file.getvalue()
                output_bytes = remove(input_bytes)
                product_cutout = Image.open(BytesIO(output_bytes)).convert("RGBA")
                
                # 2. إنشاء خلفية استوديو مربعة وناعمة (لون أبيض كتاني دافئ)
                studio_width, studio_height = 1000, 1000
                background = Image.new("RGBA", (studio_width, studio_height), (248, 246, 242, 255))
                
                # 3. ضبط حجم قطعة الملابس المعزولة لتناسب وسط الاستوديو
                basewidth = 650
                wpercent = (basewidth / float(product_cutout.size[0]))
                hsize = int(float(product_cutout.size[1]) * float(wpercent))
                product_resized = product_cutout.resize((basewidth, hsize), Image.Resampling.LANCZOS)
                
                # 4. حساب إحداثيات التمركز لتكون القطعة في المنتصف تماماً
                pos_x = (studio_width - basewidth) // 2
                pos_y = (studio_height - hsize) // 2
                
                # 5. دمج القطعة المعزولة فوق خلفية الاستوديو بسلاسة تامة
                background.paste(product_resized, (pos_x, pos_y), product_resized)
                
                # تجهيز الصورة النهائية
                final_output = background.convert("RGB")
                
                st.success("تمت إزالة الخلفية والتنسيق الاحترافي بنجاح!")
                st.image(final_output, caption="الصورة النهائية بعد عزل الخلفية والدمج الفاخر", use_container_width=True)
                
                # 6. زر التحميل المباشر
                buf = BytesIO()
                final_output.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 تحميل الصورة النهائية بجودة عالية",
                    data=byte_im,
                    file_name="masheni_clean_flat_lay.jpg",
                    mime="image/jpeg"
                )
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
