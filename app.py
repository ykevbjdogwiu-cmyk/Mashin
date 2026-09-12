import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO

st.set_page_config(page_title="Masheni Box Studio - استوديو الفلات لاي", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #4B2E2B; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛍️ Masheni Box Studio - استوديو تنسيق المنتجات")
st.write("ارفع صورة ملابسك، وسيتم دمجها وتنسيقها داخل خلفية الاستوديو الاحترافية (Flat Lay) فوراً وبدون أي انتظار.")

# رفع صورة المنتج
uploaded_file = st.file_uploader("اختر صورة قطعة الملابس...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # فتح صورة المنتج الأصلية
    product_img = Image.open(uploaded_file).convert("RGBA")
    st.image(product_img, caption="صورة المنتج الأصلية", use_container_width=True)
    
    if st.button("🚀 توليد وتنسيق الصورة فوراً"):
        with st.spinner("جاري دمج قطعة الملابس وتنسيق الاستوديو الفاخر..."):
            try:
                # 1. إنشاء خلفية استوديو أنيقة وناعمة (لون بيج/أبيض كتاني دافئ مطابق للاستوديو)
                studio_width, studio_height = 1000, 1000
                background = Image.new("RGBA", (studio_width, studio_height), (245, 243, 240, 255))
                
                # 2. تحسين مظهر صورة المنتج وزيادة حدتها قليلاً لتلائم التصميم التجاري
                enhancer = ImageEnhance.Color(product_img)
                product_img = enhancer.enhance(1.1)
                
                # 3. ضبط حجم صورة الملابس لتناسب التنسيق الاحترافي (عرض 550 بكسل مع الحفاظ على الأبعاد)
                basewidth = 550
                wpercent = (basewidth / float(product_img.size[0]))
                hsize = int(float(product_img.size[1]) * float(wpercent))
                product_resized = product_img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
                
                # 4. حساب موضع التمركز لتكون القطعة في منتصف الخلفية تماماً
                pos_x = (studio_width - basewidth) // 2
                pos_y = (studio_height - hsize) // 2
                
                # 5. دمج قطعة الملابس فوق خلفية الاستوديو بسلاسة
                background.paste(product_resized, (pos_x, pos_y), product_resized)
                
                # تجهيز الصورة النهائية المدمجة
                final_output = background.convert("RGB")
                
                st.success("تم تنسيق وتوليد الصورة الاحترافية بنجاح!")
                st.image(final_output, caption="الصورة النهائية بتنسيق الاستوديو الفاخر", use_container_width=True)
                
                # 6. زر التحميل المباشر للصورة النهائية بجودة عالية
                buf = BytesIO()
                final_output.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 تحميل الصورة النهائية بجودة عالية",
                    data=byte_im,
                    file_name="masheni_studio_flat_lay.jpg",
                    mime="image/jpeg"
                )
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة والدمج: {e}")
