import streamlit as st
from PIL import Image
import tempfile
import os
from detect import detect_birds

# Page config
st.set_page_config(
    page_title="Poultry Health Monitor",
    page_icon="🐔",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("🐔 About This Project")
    st.markdown("""
    This AI-powered tool detects visual symptoms of disease in poultry 
    using a custom-trained YOLOv8 model.
    
    **How it works:**
    1. Upload a poultry image
    2. Model analyzes visual symptoms
    3. Get instant health classification
    
    **Detects:**
    - ✅ Healthy birds
    - 🔴 Disease symptoms (swelling, discoloration, lesions)
    """)
    
    st.divider()
    
    st.subheader("⚙️ Settings")
    confidence_threshold = st.slider(
        "Detection Confidence", 
        min_value=0.1, 
        max_value=0.9, 
        value=0.35, 
        step=0.05,
        help="Higher values = fewer but more confident detections"
    )
    
    st.divider()
    
    st.caption("Model: YOLOv8 Nano (custom trained)")
    st.caption("Dataset: 1,564 poultry images")
    st.caption("Classes: Healthy, Disease")

# ---------------- MAIN PAGE ----------------
st.title("🐔 Poultry Health Monitor")
st.markdown("##### AI-powered disease detection for poultry farms")
st.markdown("Upload a poultry image below to detect healthy and diseased birds automatically.")
st.divider()

# File uploader
uploaded_file = st.file_uploader(
    "Choose a poultry image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Original Image")
        st.image(uploaded_file, use_container_width=True)

    with st.spinner("🔍 Analyzing image..."):
        result = detect_birds(tmp_path, confidence=confidence_threshold)

    with col2:
        st.subheader("🎯 Detection Result")
        st.image(result["output_image"], use_container_width=True)

    st.divider()

    st.subheader("📊 Detection Summary")
    col3, col4, col5 = st.columns(3)

    with col3:
        st.metric("Total Birds Detected", result["total"])
    with col4:
        st.metric("✅ Healthy", result["healthy"])
    with col5:
        st.metric("🔴 Diseased", result["disease"])

    st.divider()

    if result["disease"] > 0:
        st.error(f"⚠️ **Alert:** {result['disease']} sick bird(s) detected! Isolate immediately to prevent spread.")
    elif result["total"] == 0:
        st.warning("⚠️ No birds detected. Try lowering the confidence threshold in the sidebar or use a clearer image.")
    else:
        st.success("✅ All detected birds appear healthy!")

    if result["detections"]:
        st.subheader("📋 Detailed Results")
        for i, d in enumerate(result["detections"]):
            status = "🔴 Disease" if d["class"] == "disease" else "✅ Healthy"
            st.write(f"**Bird {i+1}:** {status} — Confidence: {d['confidence']:.0%}")

    os.unlink(tmp_path)

else:
    st.info("👆 Please upload a poultry image to begin analysis.")
    
    with st.expander("ℹ️ Tips for best results"):
        st.markdown("""
        - Use clear, well-lit images
        - Focus on the bird's face/head area where symptoms are most visible
        - Avoid heavily cropped or zoomed images
        - Adjust the confidence threshold in the sidebar if needed
        """)

# Footer
st.divider()
st.caption("Built by Triveni Gadela | YOLOv8 + Streamlit | Poultry Health Monitoring System")