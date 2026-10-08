import streamlit as st

def trim_string(text: str, trim_patterns: list[str]) -> str:
    """
    Membersihkan string dari daftar akhiran (suffix) yang disetting.
    Pattern yang lebih panjang akan diprioritaskan lebih dulu untuk menghindari parsial match.
    """
    # Urutkan pattern berdasarkan panjangnya (terpanjang dulu)
    sorted_patterns = sorted(trim_patterns, key=len, reverse=True)
    
    lines = text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        cleaned_line = line
        # Cek dan hapus suffix jika ada yang cocok
        for pattern in sorted_patterns:
            if pattern and cleaned_line.endswith(pattern):
                cleaned_line = cleaned_line[:-len(pattern)].strip()
                break  # Hapus satu match akhiran saja per baris
        
        cleaned_lines.append(cleaned_line)
        
    return "\n".join(cleaned_lines)

# --- CONFIG HALAMAN STREAMLIT ---
st.set_page_config(
    page_title="String Trimmer App",
    page_icon="✂️",
    layout="wide"
)

st.title("✂️ String Trimmer App")
st.markdown("Aplikasi untuk menghapus akhiran (*suffix*) teks secara otomatis berdasarkan settingan kustom.")

# Sidebar untuk Pengaturan Pattern
st.sidebar.header("⚙️ Pengaturan Trim")
default_patterns = " - B| - W| - EKS| Eks| - NON AKTIF| - REG| Reg"

trim_input = st.sidebar.text_area(
    "Daftar Trim Suffix (pisahkan dengan tanda pipe `|`):",
    value=default_patterns,
    height=150,
    help="Masukkan karakter/kata akhiran yang ingin dihapus, dipisahkan dengan tanda pipe |"
)

# Parse pattern dari input sidebar
patterns = [p.rstrip() for p in trim_input.split("|") if p != ""]

# Menampilkan daftar pattern aktif
st.sidebar.markdown("**Pattern Aktif:**")
st.sidebar.code(patterns)

# --- AREA UTAMA INPUT & OUTPUT ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Input Teks")
    default_text = "ATHAYA - W\nATHAYA Eks\nSURYA - B\nMAKMUR - NON AKTIF\nMERDEKA Reg"
    input_text = st.text_area(
        "Masukkan teks yang ingin di-trim (satu nama per baris):",
        value=default_text,
        height=300
    )

# Proses Trimming
output_text = ""
if input_text:
    output_text = trim_string(input_text, patterns)

with col2:
    st.subheader("📤 Hasil Output")
    st.text_area(
        "Hasil setelah di-trim:",
        value=output_text,
        height=300,
        disabled=True
    )
    
    # Tombol Download Hasil
    st.download_button(
        label="📥 Download Hasil (.txt)",
        data=output_text,
        file_name="hasil_trim.txt",
        mime="text/plain"
    )
