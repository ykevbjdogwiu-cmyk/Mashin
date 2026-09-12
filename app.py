import streamlit as st
from PIL import Image, ImageEnhance
from io import BytesIO

st.set_page_config(page_title="Masheni Box Studio - استوديو الفلات لاي", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #4B2E2B; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ Masheni Box Studio - استوديو تنسيق المنتجات")
st.write("ارفع صورة ملابسك، وسيتم دمجها بسلاسة داخل خلفية الاستوديو الاحترافية (Flat Lay) فوراً.")

# رفع صورة المنتج
uploaded_file = st.file_uploader("اختر صورة قطعة الملابس...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # فتح صورة المنتج الأصلية
    product_img = Image.open(uploaded_file).convert("RGBA")
    st.image(product_img, caption="صورة المنتج الأصلية", use_container_width=True)
    
    if st.button("🚀 دمج وتنسيق الصورة باحترافية"):
        with st.spinner("جاري دمج قطعة الملابس مع خلفية الاستوديو الفاخرة..."):
            try:
                # 1. إنشاء خلفية استوديو بمقاسات مربعة ونقية (لون أبيض كتاني دافئ ومتناسق)
                studio_width, studio_height = 1000, 1000
                background = Image.new("RGBA", (studio_width, studio_height), (248, 246, 242, 255))
                
                # 2. تحسين جودة وإضاءة صورة المنتج لتتناسب مع التصميم التجاري
                enhancer = ImageEnhance.Brightness(product_img)
                product_img = enhancer.enhance(1.05)
                
                # 3. تعديل حجم صورة الملابس لتأخذ مساحة مناسبة في منتصف الاستوديو
                basewidth = 700
                wpercent = (basewidth / float(product_img.size[0]))
                hsize = int(float(product_img.size[1]) * float(wpercent))
                product_resized = product_img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
                
                # 4. حساب إحداثيات التمركز بدقة ليتم وضع الملابس في المنتصف تماماً
                pos_x = (studio_width - basewidth) // 2
                pos_y = (studio_height - hsize) // 2
                
                # 5. الدمج المباشر والمتناسق فوق الخلفية
                background.paste(product_resized, (pos_x, pos_y), product_resized)
                
                # تجهيز الصورة النهائية بدون حواشی مزعجة
                final_output = background.convert("RGB")
                
                st.success("تم دمج وتنسيق الصورة الاحترافية بنجاح!")
                st.image(final_output, caption="الصورة النهائية بعد الدمج الاحترافي", use_container_width=True)
                
                # 6. زر التحميل المباشر
                buf = BytesIO()
                final_output.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 تحميل الصورة النهائية بجودة عالية",
                    data=byte_im,
                    file_name="masheni_pro_flat_lay.jpg",
                    mime="image/jpeg"
                )
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء عملية الدمج: {e}")
