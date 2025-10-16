# 📊 Quadrant Stock Analyzer

**Aplikasi analisis saham Indonesia berbasis metodologi Quadrant (Mandiri Investasi)** untuk mengklasifikasikan saham ke dalam 4 kategori: **STAR**, **GROWTH**, **VALUE**, atau **DOG**.

![Quadrant Matrix](https://img.shields.io/badge/Quadrant-Matrix-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)

---

## 🎯 Fitur Utama

- ✅ **Company Score Calculator** - Menghitung fundamental score (VCS + VC + FP)
- ✅ **Stock Score Calculator** - Menghitung valuation + growth momentum score
- ✅ **Quadrant Classification** - Klasifikasi otomatis ke STAR/GROWTH/VALUE/DOG
- ✅ **Interactive Dashboard** - Visualisasi matrix dan scoring breakdown
- ✅ **Excel Export** - Export hasil analisis ke Excel
- ✅ **Multi-Stock Comparison** - Bandingkan multiple stocks dalam satu matrix

---

## 📚 Metodologi Quadrant

Metodologi Quadrant menggunakan 2 dimensi untuk mengklasifikasikan saham:

### 1. Company Score (CS) - X-axis
Mengukur **kualitas fundamental** melalui 3 pilar:

**a. Value Creation Sustainability (VCS) - 50% weight**
- Company Lifecycle (1-4)
- Porter's Five Forces (1-4)
- Management Quality (1-4)
- ESG Score (1-4)

**b. Value Creation (VC) - 35% weight**
- ROA trends (3yr future vs 2yr historical)
- EBIT Margin trends
- Sales Growth (vs GDP + historical acceleration)
- Profit Growth (vs GDP + historical acceleration)

**c. Financial Power (FP) - 15% weight**
- OCF/EBIT ratio trends
- Equity/Asset ratio trends
- Cash/Total Asset ratio trends

### 2. Stock Score (SS) - Y-axis
Mengukur **attractiveness untuk investasi**:

**a. Valuation - 65% weight**
- Model Target Price (DCF, multiples)
- Relative Valuation (PE, PBV bands)
- Blended upside potential

**b. Growth Score - 35% weight**
- Blended-Forward Revenue Growth
- Blended-Forward EBIT Growth
- Blended-Forward Net Profit Growth

---

## 🗂️ The 4 Quadrants

| Quadrant | CS | SS | Karakteristik | Strategy |
|----------|----|----|---------------|----------|
| **⭐ STAR** | High (>3.0) | High (>3.0) | Strong fundamentals + Attractive valuation | **STRONG BUY** |
| **📈 GROWTH** | Low (<3.0) | High (>3.0) | Weak fundamentals + Attractive valuation | **BUY** (Speculative) |
| **💎 VALUE** | High (>3.0) | Low (<3.0) | Strong fundamentals + Expensive valuation | **HOLD** (Wait) |
| **🐕 DOG** | Low (<3.0) | Low (<3.0) | Weak fundamentals + Expensive valuation | **SELL/AVOID** |

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/quadrant-stock-analyzer.git
cd quadrant-stock-analyzer

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

---

## 📖 Cara Menggunakan

### 1. Input Data Saham

**Tab: Company Information**
- Masukkan ticker, nama perusahaan, sektor, harga saham
- Input data market cap dan shares outstanding

**Tab: Qualitative Scores (VCS)**
- Company Lifecycle: 1-4 (1=Start-up, 4=Growth)
- Porter's Five Forces: 1-4 untuk setiap force
- Management Quality: 1-4
- ESG Score: 1-4 untuk E, S, G

**Tab: Financial Data**
- Input historical data (2 years): Revenue, EBIT, Net Income, Assets, Equity, Cash, OCF
- Input projected data (3 years): Same metrics
- System akan otomatis menghitung discrepancy dan scoring

**Tab: Valuation & Growth**
- Model Target Price (dari DCF atau multiples)
- Current Price
- Blended-Forward Growth rates (Revenue, EBIT, Net Profit)

### 2. Calculate Scores

Klik tombol **"Calculate Scores"** untuk:
- Menghitung Company Score (CS)
- Menghitung Stock Score (SS)
- Klasifikasi ke Quadrant
- Generate visualisasi

### 3. View Results

**Quadrant Matrix Chart**
- Visualisasi posisi saham di matrix
- Color-coded berdasarkan quadrant

**Score Breakdown**
- Detail breakdown untuk setiap component
- Weighted contribution
- Comparison dengan threshold

**Investment Recommendation**
- Rating (Strong Buy / Buy / Hold / Sell)
- Target Price
- Risk-Reward Assessment

### 4. Export Results

Klik **"Export to Excel"** untuk download hasil analisis dalam format Excel dengan multiple sheets.

---

## 📁 Struktur Project

```
quadrant-stock-analyzer/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
│
├── src/
│   ├── calculator.py           # Score calculation logic
│   ├── classifier.py           # Quadrant classification
│   └── visualizer.py           # Chart and visualization
│
├── utils/
│   ├── data_validator.py       # Input validation
│   ├── excel_exporter.py       # Excel export functionality
│   └── helpers.py              # Helper functions
│
├── data/
│   └── sample_data.json        # Sample data untuk testing
│
└── assets/
    ├── logo.png                # App logo
    └── quadrant_guide.pdf      # Methodology guide
```

---

## 🧮 Scoring Rules

### Value Creation (VC) Metrics

| Metric | Score 4 | Score 3 | Score 2 | Score 1 |
|--------|---------|---------|---------|---------|
| ROA Discrepancy | >20 bps | 15-20 bps | 10-15 bps | <10 bps |
| EBIT Margin Disc | >10 bps | 5-10 bps | 0-5 bps | <0 bps |
| Sales vs GDP | >4 bps | 4-0 bps | -2 to 0 | <-2 bps |
| Profit vs GDP | >4 bps | 4-0 bps | -2 to 0 | <-2 bps |

### Financial Power (FP) Metrics

| Metric | Score 4 | Score 3 | Score 2 | Score 1 |
|--------|---------|---------|---------|---------|
| OCF/EBIT Disc | >10 bps | 5-10 bps | 0-5 bps | <0 bps |
| Equity/Asset Disc | >10 bps | 5-10 bps | 0-5 bps | <0 bps |
| Cash/Asset Disc | >10 bps | 5-10 bps | 0-5 bps | <0 bps |

### Stock Score Metrics

| Metric | Score 4 | Score 3 | Score 2 | Score 1 |
|--------|---------|---------|---------|---------|
| Valuation Upside | >30% | 15-30% | 0-15% | <0% |
| Growth Rate | >50% | 25-50% | 5-25% | <5% |

---

## 📊 Contoh Hasil

### AMRT (PT Sumber Alfaria Trijaya Tbk)

**Scores:**
- Company Score (CS): 2.66
- Stock Score (SS): 3.30

**Quadrant: GROWTH** 📈

**Breakdown:**
- VCS: 3.2 (Lifecycle 3.5, Porter 3.0, Management 3.0, ESG 3.3)
- VC: 2.1 (ROA 1.0, EBIT Margin 2.0, Sales Growth 2.0, Profit Growth 3.5)
- FP: 2.0 (OCF/EBIT 2.0, Equity/Asset 2.0, Cash/Asset 2.0)
- Valuation: 4.0 (34% upside)
- Growth Score: 2.0 (14-16% growth)

**Recommendation:** **BUY**
- Target Price: IDR 2,966
- Current Price: IDR 2,210
- Upside: 34.2%

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Export**: OpenPyXL

---

## 📝 To-Do / Future Enhancements

- [ ] Integration dengan API data saham (Yahoo Finance, IDX)
- [ ] Auto-fetch financial data dari Bloomberg/Reuters
- [ ] Historical tracking untuk monitoring score changes
- [ ] Portfolio optimization berdasarkan Quadrant allocation
- [ ] Backtesting untuk validate methodology
- [ ] Mobile-responsive design
- [ ] Multi-language support (EN/ID)
- [ ] PDF report generation

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Developer**: Your Name  
**Email**: your.email@example.com  
**LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourprofile)  
**GitHub**: [Your GitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Metodologi Quadrant dikembangkan oleh **Mandiri Investasi**
- Terinspirasi dari Quadrant Teach In (May 2025)
- Thanks to Streamlit community untuk amazing framework

---

## ⚠️ Disclaimer

Aplikasi ini dibuat untuk tujuan **edukasi dan riset**. Bukan merupakan rekomendasi investasi. Pengguna harus melakukan due diligence sendiri dan berkonsultasi dengan financial advisor sebelum membuat keputusan investasi.

**Past performance is not indicative of future results.**

---

**Made with ❤️ for Indonesian Stock Market Investors**

