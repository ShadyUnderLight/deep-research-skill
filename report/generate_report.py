#!/usr/bin/env python3
"""Generate PDF report for 通宇通讯 (002792)"""

from fpdf import FPDF
import os

FONT_DIR = "/System/Library/Fonts"
PINGFANG = os.path.join(FONT_DIR, "PingFang.ttc")
STHEITI = os.path.join(FONT_DIR, "STHeiti Medium.ttc")

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("ping", "", os.path.join(
            "/System/Library/AssetsV2/com_apple_MobileAsset_Font8",
            "86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset",
            "AssetData", "PingFang.ttc"), uni=True)
        self.add_font("heiti", "", STHEITI, uni=True)

    def header(self):
        self.set_font("ping", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, "Deep Research Report | Tongyu Communication (002792)", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("ping", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, num, title):
        self.set_font("ping", "", 16)
        self.set_text_color(20, 60, 120)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(20, 60, 120)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("ping", "", 12)
        self.set_text_color(40, 80, 140)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def sub_sub_title(self, title):
        self.set_font("ping", "", 10)
        self.set_text_color(60, 60, 60)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("ping", "", 9)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("ping", "", 9)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(6, 5, "-")
        self.multi_cell(0, 5, text)
        self.ln(0.5)

    def tag(self, label, text, color):
        self.set_font("ping", "", 8)
        # tag label
        self.set_text_color(255, 255, 255)
        self.set_fill_color(*color)
        self.cell(self.get_string_width(label) + 4, 5, label, fill=True)
        # tag text
        self.set_text_color(30, 30, 30)
        self.set_font("ping", "", 9)
        self.cell(4)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def confirmed(self, text):
        self.tag("[CONFIRMED]", text, (40, 160, 80))

    def inference(self, text):
        self.tag("[INFERENCE]", text, (200, 160, 40))

    def uncertainty(self, text):
        self.tag("[UNCERTAIN]", text, (200, 80, 60))


def build_report():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # =========== COVER PAGE ===========
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("ping", "", 28)
    pdf.set_text_color(20, 60, 120)
    pdf.cell(0, 15, "Deep Research Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("ping", "", 22)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 12, "Tongyu Communication (002792)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("ping", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Generated: 2026-05-27 | Sources: Multiple Cross-Validated", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("ping", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, "Language: Chinese (Simplified) | Classification: Public Information", align="C", new_x="LMARGIN", new_y="NEXT")

    # Table of Contents
    pdf.add_page()
    pdf.set_font("ping", "", 16)
    pdf.set_text_color(20, 60, 120)
    pdf.cell(0, 10, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    toc = [
        "1. Executive Summary",
        "2. Business & Products",
        "3. Industry Position",
        "4. Customers & Application Scenarios",
        "5. Competitive Landscape",
        "6. Financial & Operational Key Signals (2024-2025)",
        "7. Bullish / Bearish Logic",
        "8. 1-3 Year Opportunities & Risks",
        "9. Information Confidence Level Summary",
        "10. Sources & References",
    ]
    pdf.set_font("ping", "", 10)
    pdf.set_text_color(30, 30, 30)
    for item in toc:
        pdf.cell(0, 7, item, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("ping", "", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 5, "Confidence Tags: [CONFIRMED] = cross-validated facts | [INFERENCE] = reasonable inference | [UNCERTAIN] = single source or unverifiable")
    pdf.ln(3)

    # =========== SECTION 1: EXECUTIVE SUMMARY ===========
    pdf.add_page()
    pdf.chapter_title("1", "Executive Summary")

    pdf.body_text(
        "Tongyu Communication (002792.SZ) is a leading Chinese manufacturer of communication antennas and RF components, "
        "headquartered in Zhongshan, Guangdong. Founded in 1996 and listed on the Shenzhen Stock Exchange in 2016, the company "
        "is a core supplier to global telecom equipment vendors (Huawei, ZTE, Nokia, Ericsson, Samsung) and operators "
        "(China Mobile, China Unicom, China Telecom, Vodafone). With over 700 patent families and 700 million+ antenna units deployed, "
        "Tongyu ranks 4th in China's base station antenna market (~7-8% share) behind Huawei, Comba, and CICT."
    )
    pdf.ln(1)
    pdf.body_text(
        "Key findings:\n"
        "- Revenue has declined from a peak of 1.64B RMB (2019) to 1.11B RMB (2025), reflecting the maturing of China's 5G buildout.\n"
        "- Net profit margin is thin at 3.69% (2025); traditional business faces pricing pressure and volume decline.\n"
        "- Satellite communication is the key growth pivot: 54M RMB in 2025 (+26% YoY), but still only 4.87% of revenue.\n"
        "- Overseas revenue grew to 40% of total with 31.65% gross margin, providing a profitable buffer.\n"
        "- The company is transitioning from traditional antenna supplier to 'Air-Space-Ground' integrated solution provider.\n"
        "- Analyst forecasts are highly divergent, suggesting significant uncertainty around the satellite revenue inflection."
    )

    # =========== SECTION 2: BUSINESS & PRODUCTS ===========
    pdf.add_page()
    pdf.chapter_title("2", "Business & Products")

    pdf.sub_title("2.1 Core Business")
    pdf.confirmed("R&D, manufacturing, and sales of communication antennas and RF components. Core products include base station antennas, RF devices, microwave antennas, satellite communication products, and FWA modules.")
    pdf.ln(2)

    pdf.sub_title("2.2 Major Product Lines")
    products = [
        "Base Station Antennas (BS Antennas): 5G Massive MIMO, multi-beam, air-to-ground antennas; 380MHz-6GHz frequency coverage supporting 2G to 5G seamless upgrade.",
        "Microwave Antennas (MW Antennas): Point-to-point microwave link antennas for backhaul networks.",
        "RF Components: Filters, duplexers for 4G/5G radio stations.",
        "Satellite Communication Products (Satcom): Satellite payloads, IoT terminals. Launched in 2023 via subsidiary in Hubei.",
        "Optical Communication Products: Fiber optic communication equipment (via 25.59% stake in Sichuan Guangwei).",
        "FWA Products: CPE, WiFi routers, FTTH.",
        "New Energy: Green battery swap ecosystem (est. 2025).",
        "MacroWiFi: Long-range outdoor WiFi coverage solution, 60%+ market share in niche segment.",
    ]
    for p in products:
        pdf.bullet(p)
    pdf.ln(1)

    pdf.sub_title("2.3 Technology Highlights")
    techs = [
        "First in China to develop mobile communication base station antenna (1994).",
        "First globally to commercialize TDD smart antenna.",
        "First globally to design integrated-filter 5G antenna.",
        "First globally to achieve AFU (Active Filter Unit) mass production.",
        "First in industry to introduce sheet-metal filter into 5G antenna (2022).",
        "706 granted patents (incl. 38 international).",
        "National Green Factory, National Enterprise Technology Center, Postdoctoral Research Station.",
    ]
    for t in techs:
        pdf.bullet(t)
    pdf.ln(2)

    # =========== SECTION 3: INDUSTRY POSITION ===========
    pdf.add_page()
    pdf.chapter_title("3", "Industry Position")

    pdf.sub_title("3.1 Market Size")
    pdf.confirmed("Global mobile communication antenna market ~$24.7B (2024), projected ~$49B (2034), CAGR 7.3%. China base station antenna market ~11.22B RMB (2024).")
    pdf.ln(1)
    pdf.confirmed("China Mobile 2025-2026 centralized procurement: 47,622 high-speed rail antennas, 195,500 TDD antennas, 272,400 green multi-band antennas, ~15.89M indoor antennas.")
    pdf.ln(2)

    pdf.sub_title("3.2 Market Share & Ranking")
    pdf.confirmed("Global base station antenna share: ~7% (2017 data). China ranking: 4th (after Huawei, Comba, CICT). Antennas in network: 7M+ units. Revenue rank in industry: 24/36 (2025 Q3).")
    pdf.ln(2)

    pdf.sub_title("3.3 Technology Position")
    pdf.confirmed("First global AFU commercial deployment. 706 patents. Coverage 2G to 6G. 5.5G/6G antenna tech in small-batch production. Guangdong Famous High-Tech Product award for 5G massive array antenna.")
    pdf.ln(2)

    # =========== SECTION 4: CUSTOMERS & APPLICATIONS ===========
    pdf.add_page()
    pdf.chapter_title("4", "Customers & Application Scenarios")

    pdf.sub_title("4.1 Customer Structure")
    pdf.confirmed("Equipment vendors (Huawei, ZTE, Nokia, Ericsson, Samsung, Datang) ~40% of revenue. Operators (China Mobile/Unicom/Telecom, Vodafone) ~40%. International distributors ~20%.")
    pdf.ln(2)

    pdf.sub_title("4.2 Application Scenarios")
    apps = [
        "4G/5G mobile communication base station construction",
        "Microwave backhaul network",
        "Satellite communication & IoT (low-earth orbit constellation)",
        "Outdoor long-range WiFi coverage (MacroWiFi)",
        "Fiber optic communication networks",
        "New energy battery swap stations",
        "Low-altitude economy (drone communication / air-ground integration)",
    ]
    for a in apps:
        pdf.bullet(a)
    pdf.ln(2)

    # =========== SECTION 5: COMPETITIVE LANDSCAPE ===========
    pdf.add_page()
    pdf.chapter_title("5", "Competitive Landscape")

    pdf.sub_title("5.1 Competitive Structure")
    pdf.body_text("China's base station antenna market is dominated by 'Big 4': Huawei (~32% global), Comba (13-15.8% in cumulative procurement), CICT Mobile/Wuhan Hongxin (10%+), and Tongyu (7-8%). The top 5 players control 73-80%+ of the market.")
    pdf.ln(1)

    pdf.sub_title("5.2 Key Competitors")
    competitors = [
        "Huawei (32% global share): Vertically integrated, self-developed antennas. Tongyu serves as a supplementary supplier. Huawei's self-sufficiency limits Tongyu's addressable market.",
        "Comba Telecom (02342.HK, ~13-15.8%): Independent antenna leader. Strong operator channel (~75% revenue from 3 major operators). Full wireless optimization solutions. More operator-direct oriented vs Tongyu's equipment-vendor orientation.",
        "CICT Mobile / Hongxin (10%+): State-owned enterprise background, 5G integrated solutions.",
        "Mobi Development (00947.HK, ~7-8%): Core ZTE supplier (~50% revenue from ZTE). Strong RF device capability.",
        "Shenglu Communication (002446, ~3%): Smaller scale, differentiated by military + civilian dual-track.",
    ]
    for c in competitors:
        pdf.bullet(c)
    pdf.ln(2)

    pdf.sub_title("5.3 Barriers to Entry")
    barriers = [
        "Technology: Massive MIMO, AFU require deep RF expertise. Full 2G-6G frequency coverage needed.",
        "Certification: Lengthy qualification process by Huawei, ZTE, Nokia, Ericsson, and major operators.",
        "Capital: Antenna manufacturing is capital intensive.",
        "Scale: Top 5 players hold 73-80%+ market share.",
        "IP: Tongyu holds 706 granted patents, hard for new entrants to bypass.",
        "Customer stickiness: Long-standing relationships with high switching costs.",
    ]
    for b in barriers:
        pdf.bullet(b)
    pdf.ln(2)

    # =========== SECTION 6: FINANCIAL & OPERATIONAL KEY SIGNALS ===========
    pdf.add_page()
    pdf.chapter_title("6", "Financial & Operational Key Signals (2024-2025)")

    pdf.sub_title("6.1 Revenue & Profit")
    pdf.confirmed("2025 revenue: 1.11B RMB (-7.01% YoY). 2025 net profit: 41.13M RMB (-0.62% YoY). 2024 revenue: 1.19B RMB (-7.71% YoY). 2024 net profit: 41.39M RMB (-49.00% YoY). Peak revenue was 1.64B RMB in 2019.")
    pdf.ln(1)

    pdf.sub_title("6.2 Profitability")
    pdf.confirmed("2025 gross margin: 20.17% (-2.04pcts YoY). 2025 net margin: 3.69% (-0.22pct). 2025 EPS: 0.0784 RMB. Q1 2026 turned loss: -0.13B RMB, -4.77% net margin, EPS -0.0247.")
    pdf.ln(1)

    pdf.sub_title("6.3 Segment Analysis")
    pdf.confirmed("Traditional (BS antennas, RF, MW): 93.77% of revenue. RF components: 170M RMB (+36.97% YoY). Satellite communication: 54M RMB (+26.29% YoY), 4.87% of revenue. MacroWiFi: ~60M RMB. Overseas: 40.03% of revenue, 31.65% GM (+6.13pcts).")
    pdf.ln(1)

    pdf.sub_title("6.4 Balance Sheet & Cash Flow")
    pdf.confirmed("Net assets per share: 5.3855 RMB (2025). Operating cash flow per share: 0.0041 RMB (2025, very thin). Book value per share was 5.3416 in Q1 2025. Dividend: 0.025 RMB per 10 shares (2025).")
    pdf.inference("Thin operating cash flow suggests working capital pressure or low cash conversion from receivables.")
    pdf.ln(1)

    pdf.sub_title("6.5 R&D & Strategic Investment")
    pdf.confirmed("R&D: continuous investment in 5.5G/6G, satellite communication products. 2025 share-based payment expense: 10.2M RMB. Strategic minority investments: 30M RMB in satellite components (Hangyu Technology), 50M RMB industry fund, 20M RMB in Shanghai Tongyu. 10M RMB special investment fund (May 2026).")
    pdf.ln(1)

    pdf.sub_title("6.6 Management & Shareholding")
    pdf.confirmed("Chairman Wu Zhonglin (59), GM Shi Guiqing (59, wife of Wu). Together hold ~46.64% of shares. Wu's pledge ratio: 13.64% (18.62M shares). Non-disposal commitment: valid until Oct 2026. Board Secretary Huang Hua appointed 2023. Independent directors from academia and legal profession.")
    pdf.ln(2)

    # =========== SECTION 7: BULLISH / BEARISH LOGIC ===========
    pdf.add_page()
    pdf.chapter_title("7", "Bullish / Bearish Logic")

    pdf.sub_title("7.1 Bullish Case")
    pdf.body_text("Satellite Communication First-Mover: Tongyu is one of the few Chinese listed companies with full 'Space-Ground-Terminal' product chain. It has participated in Qianfan Constellation (a Chinese LEO satellite internet project). Won a 25-type terminal bid in 2025. Has 1B+ RMB level satellite orders (single source, unverified).")
    pdf.body_text("Overseas Expansion: Overseas revenue grew to 40% with 31.65% GM, significantly higher than domestic. Belt & Road countries (Southeast Asia, Middle East, Africa) still in 4G-to-5G transition. EU production base in Latvia provides tariff-free access.")
    pdf.body_text("5G-A / 6G Upgrade Cycle: 5.5G requires more antennas and higher complexity. ELAA-MM (Extremely Large Aperture Array) drives per-station antenna value. China operators starting 5G-A deployment in 2024-2025.")
    pdf.body_text("Low-Altitude Economy: Air-ground integration (通感一体化) is a key infrastructure for drone/UAV operations. Tongyu has demonstrated 2.1G NR air-ground integrated green antennas. Won 'Low-Altitude Navigation Pioneer' recognition.")
    pdf.body_text("Valuation Re-rating: As satellite revenue scales, PE multiple could compress. Analyst EPS forecasts for 2026 range from 0.28 to 0.52 RMB, implying 60-110x forward PE at current ~5 RMB share price.")
    pdf.ln(2)

    pdf.sub_title("7.2 Bearish Case")
    pdf.body_text("Revenue Decline: Revenue has fallen from 1.64B (2019) to 1.11B (2025), a 32% decline. Chinese 5G buildout is past peak. Without satellite revenue inflection, traditional business will continue to shrink.")
    pdf.body_text("Weak Profitability: Net margin of 3.69% is razor-thin. Q1 2026 turned to net loss of 13M RMB. Pricing pressure from centralized procurement and Huawei self-sufficiency limits margin expansion.")
    pdf.body_text("Satellite Hype vs Reality: Satellite revenue is only 54M RMB (4.87% of total) after 3+ years of investment. Analyst forecasts have been wildly optimistic - Huaan forecasted 2025 revenue of 1.6B vs actual 1.11B, a 31% miss. This pattern of over-promising raises credibility concerns.")
    pdf.body_text("Valuation: At 0.0784 RMB EPS (2025), PE is ~66x. Even optimistic 2026 EPS of 0.36 RMB implies PE > 14x. The traditional antenna business at 3-5x PE is heavily loss-making in satellite growth. Any delay in satellite orders would lead to sharp de-rating.")
    pdf.body_text("Competition: Huawei's self-developed antennas limit market access. Comba and CICT have stronger operator relationships. The domestic market structure is oligopolistic with limited share gain potential.")
    pdf.body_text("Corporate Governance: High concentration of power in founder couple (46.64%). Pledged shares create refinancing risk. The company has pivoted to 3+ new business lines (satellite, new energy, FWA, MacroWiFi, optical), which may indicate lack of strategic focus.")
    pdf.ln(2)

    # =========== SECTION 8: 1-3 YEAR OPPORTUNITIES & RISKS ===========
    pdf.add_page()
    pdf.chapter_title("8", "1-3 Year Opportunities & Risks")

    pdf.sub_title("8.1 Opportunities")
    pdf.confirmed("China's LEO satellite constellation (Qianfan / GW) is expected to accelerate launches. ITU deadline requires 10% of planned satellites to be deployed. Tongyu is positioned as antenna/subsystem supplier.")
    pdf.confirmed("Overseas 4G/5G network buildout in Belt & Road, Southeast Asia, Middle East, Africa. Tongyu has existing distribution in 70+ countries.")
    pdf.confirmed("5G-A deployment starting in 2024-2025 requires antenna upgrades (more channels, higher complexity). ELAA-MM technology increases per-station antenna value.")
    pdf.confirmed("Low-altitude economy policy support. Tongyu's air-ground integration technology for drone communications.")
    pdf.inference("6G pre-commercial research (expected 2028-2030 standard) may drive early investments in next-gen antenna technology.")
    pdf.uncertainty("Satellite communication revenue inflection point (whether it reaches 200M-500M RMB scale within 1-3 years).")
    pdf.ln(2)

    pdf.sub_title("8.2 Risks")
    pdf.confirmed("Traditional business continues to shrink as China 5G capex declines. Base station antenna market is mature.")
    pdf.confirmed("Thin margins make the company vulnerable to raw material price fluctuations and procurement price cuts.")
    pdf.confirmed("Q1 2026 net loss raises concern about near-term earnings trajectory.")
    pdf.confirmed("Controlling shareholder pledge (13.64%) adds financial risk if share price declines significantly.")
    pdf.inference("Analyst model credibility: Large forecast errors suggest difficulty in predicting satellite revenue timing. If satellite orders are delayed, current valuation is unsupportable.")
    pdf.uncertainty("Trade war / decoupling risks affecting overseas business in sensitive markets (satellite communication may face export controls).")
    pdf.uncertainty("New energy / battery swap business is a completely unrelated diversification with unknown competitive position.")
    pdf.ln(2)

    # =========== SECTION 9: CONFIDENCE LEVEL SUMMARY ===========
    pdf.add_page()
    pdf.chapter_title("9", "Information Confidence Level Summary")

    pdf.sub_sub_title("Confirmed Facts (Cross-Validated, Multiple Sources)")
    confirmed_list = [
        "Company name, founding date, listing details, equity structure",
        "Core business: communication antennas & RF components",
        "Major product lines (as listed on official website and financial reports)",
        "Revenue and net profit for 2024 and 2025",
        "Gross margin, net margin, EPS for 2024-2025",
        "Market share ranking (~4th in China, ~7-8% share)",
        "Customer list (Huawei, ZTE, Nokia, Ericsson, Samsung, operators)",
        "Patent count (706 granted, 38 international)",
        "Overseas revenue ratio (~40%) and gross margin (31.65%)",
        "Satellite communication revenue (54M RMB in 2025, +26% YoY)",
        "Dividend history and share-based payment expense",
        "Management team and shareholding structure",
    ]
    for item in confirmed_list:
        pdf.bullet(item)
    pdf.ln(2)

    pdf.sub_sub_title("Likely Inferences (Reasonable but Not Directly Verified)")
    inference_list = [
        "Industry competitive dynamics and barrier structure",
        "Customer stickiness and switching cost analysis",
        "Satellite revenue growth trajectory (directionally correct, magnitude uncertain)",
        "Impact of 5G-A on antenna demand (positive correlation likely)",
        "Overseas business growth outlook based on stated strategy",
    ]
    for item in inference_list:
        pdf.bullet(item)
    pdf.ln(2)

    pdf.sub_sub_title("Open Uncertainties (Single Source or Unverifiable)")
    uncertainty_list = [
        "Goldman Sachs 2028 revenue forecast of 3.767B RMB (single source)",
        "Specific 1B+ RMB satellite order details (company claim, no public contract details)",
        "Market share % breakdown by year (data vintage issues)",
        "Exact timeline of satellite revenue inflection",
        "Low-altitude economy revenue contribution potential",
        "New energy business competitive position and revenue potential",
    ]
    for item in uncertainty_list:
        pdf.bullet(item)
    pdf.ln(2)

    # =========== SECTION 10: SOURCES ===========
    pdf.add_page()
    pdf.chapter_title("10", "Sources & References")

    sources = [
        "Company official website: www.tycc.cn",
        "Tonghuashun F10 page: basic.10jqka.com.cn/002792/",
        "Sina Finance stock page: finance.sina.com.cn/realstock/company/sz002792/",
        "CITIC Securities research report (2026-04-29): Annual report & 1Q26 review",
        "CITIC Securities research report (2025-11-27): Initiation coverage",
        "Huaan Securities research report (2025-11-20): Satellite communication thematic",
        "Huaan Securities research report (2025-04-28): 2024 annual report review",
        "Investor relations Q&A (2026-05-18): finance.sina.com.cn/stock/aigc/jgdy/",
        "Global Market Insights: Base station antenna market data",
        "Forward Industry Research Institute: Competitive landscape analysis",
        "Shenzhen Securities Times: Financial data cross-reference",
        "Securities Star / Huayan Zhixun: Industry status analysis",
        "Qianzhan Industry Research Institute: Market entry barriers",
        "Geelonghui: Competitor comparison analysis",
        "Sinodata / Snowball: Investment thesis references",
    ]
    for s in sources:
        pdf.bullet(s)
    pdf.ln(5)

    pdf.set_font("ping", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 4, "Disclaimer: This report is compiled from publicly available information for research purposes only. It does not constitute investment advice. Information accuracy depends on source reliability. The [CONFIRMED] tag indicates cross-validated data, but no guarantee of absolute accuracy is made.")

    return pdf


if __name__ == "__main__":
    pdf = build_report()
    os.makedirs("report", exist_ok=True)
    output_path = "report/tongyu_communication_deep_research.pdf"
    pdf.output(output_path)
    print(f"PDF report generated: {output_path}")
    print(f"Pages: {pdf.page_no()}")
