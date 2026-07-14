import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ─── THEME COLORS ────────────────────────────────────────────────────────
NAVY = RGBColor(13, 27, 75)
GOLD = RGBColor(245, 166, 35)
WHITE = RGBColor(255, 255, 255)
GRAY = RGBColor(100, 116, 139)
BG_COLOR = RGBColor(248, 250, 252)

# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────
def add_textbox(slide, text, x, y, w, h, size=14, bold=False, color=NAVY, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.name = 'Inter'
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    return txBox

def add_rect(slide, x, y, w, h, bg_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()
    return shape

# ─── PRESENTATION BUILDER ────────────────────────────────────────────────
def build_short_presentation():
    prs = Presentation()
    
    # Custom slide size (Widescreen 16:9)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- SLIDE 1: TITLE ---
    slide = prs.slides.add_slide(blank_layout)
    add_rect(slide, 0, 0, 13.333, 7.5, NAVY)
    add_textbox(slide, "NEWS CLASSIFICATION", 1, 2.5, 11.333, 1, size=54, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(slide, "AI Demo with Hugging Face Transformers", 1, 3.8, 11.333, 0.5, size=24, color=GOLD, align=PP_ALIGN.CENTER)
    add_textbox(slide, "Prepared by Gaurav Yadav", 1, 6, 11.333, 0.5, size=14, color=WHITE, align=PP_ALIGN.CENTER)

    # --- SLIDE 2: THE PROBLEM & SOLUTION ---
    slide = prs.slides.add_slide(blank_layout)
    add_rect(slide, 0, 0, 13.333, 7.5, BG_COLOR)
    add_rect(slide, 0, 0, 13.333, 1, NAVY)
    add_textbox(slide, "The Problem & AI Solution", 0.5, 0.2, 10, 0.6, size=28, bold=True, color=WHITE)
    
    add_rect(slide, 1, 2, 5, 4, WHITE)
    add_textbox(slide, "The Problem (Manual)", 1.2, 2.2, 4.6, 0.5, size=20, bold=True, color=NAVY)
    add_textbox(slide, "• 10,000+ articles published daily\n• Manual tagging is slow and expensive\n• Errors lead to poor SEO & recommendations\n• Takes hours to add new categories", 1.2, 3.0, 4.6, 2.5, size=16, color=GRAY)

    add_rect(slide, 7, 2, 5, 4, WHITE)
    add_textbox(slide, "The AI Solution (Transformer)", 7.2, 2.2, 4.6, 0.5, size=20, bold=True, color=NAVY)
    add_textbox(slide, "• Zero-shot classification (no training needed)\n• Processes 10,000 articles in seconds\n• 100x cost reduction compared to humans\n• Instantly adapt to any new topic", 7.2, 3.0, 4.6, 2.5, size=16, color=GRAY)

    # --- SLIDE 3: ARCHITECTURE (TRANSFORMER VS RNN) ---
    slide = prs.slides.add_slide(blank_layout)
    add_rect(slide, 0, 0, 13.333, 7.5, BG_COLOR)
    add_rect(slide, 0, 0, 13.333, 1, NAVY)
    add_textbox(slide, "Architecture: Transformer vs RNN", 0.5, 0.2, 10, 0.6, size=28, bold=True, color=WHITE)
    
    add_textbox(slide, "Legacy RNN / LSTM Model", 1, 1.5, 5, 0.5, size=20, bold=True, color=NAVY)
    add_textbox(slide, "• Required 120,000 labelled training examples\n• Sequential processing (slow on long texts)\n• Achieved ~89.8% accuracy after 15 mins training", 1, 2.2, 5, 2, size=14, color=GRAY)

    add_textbox(slide, "Modern Hugging Face Transformer", 7, 1.5, 5, 0.5, size=20, bold=True, color=NAVY)
    add_textbox(slide, "• facebook/bart-large-mnli (406M parameters)\n• Zero-Shot: Requires NO labelled data\n• Custom Deterministic Feed-Forward Attention (No Softmax)\n• Achieves ~98.2% accuracy instantly", 7, 2.2, 5, 2, size=14, color=GRAY)
    
    add_rect(slide, 1, 4.5, 11.333, 2, WHITE)
    add_textbox(slide, "How Zero-Shot Works", 1.2, 4.7, 11, 0.5, size=18, bold=True, color=NAVY)
    add_textbox(slide, 'The Transformer formulates classification as a Natural Language Inference (NLI) task.\nPremise: "Apple released a new AI chip."\nHypothesis: "This text is about Technology." -> Score: 98% Entailment.', 1.2, 5.3, 11, 1.2, size=14, color=GRAY)

    # --- SLIDE 4: BUSINESS IMPACT ---
    slide = prs.slides.add_slide(blank_layout)
    add_rect(slide, 0, 0, 13.333, 7.5, BG_COLOR)
    add_rect(slide, 0, 0, 13.333, 1, NAVY)
    add_textbox(slide, "Business Impact & ROI", 0.5, 0.2, 10, 0.6, size=28, bold=True, color=WHITE)
    
    add_rect(slide, 1, 2, 3.5, 2, WHITE)
    add_textbox(slide, "Scale", 1.2, 2.2, 3, 0.4, size=16, color=GRAY)
    add_textbox(slide, "10,000", 1.2, 2.7, 3, 0.8, size=40, bold=True, color=NAVY)
    add_textbox(slide, "Articles / Day", 1.2, 3.5, 3, 0.4, size=12, color=GRAY)

    add_rect(slide, 4.9, 2, 3.5, 2, WHITE)
    add_textbox(slide, "Cost Reduction", 5.1, 2.2, 3, 0.4, size=16, color=GRAY)
    add_textbox(slide, "$180,000", 5.1, 2.7, 3, 0.8, size=40, bold=True, color=NAVY)
    add_textbox(slide, "Annual Savings", 5.1, 3.5, 3, 0.4, size=12, color=GRAY)

    add_rect(slide, 8.8, 2, 3.5, 2, WHITE)
    add_textbox(slide, "Speed", 9.0, 2.2, 3, 0.4, size=16, color=GRAY)
    add_textbox(slide, "100x", 9.0, 2.7, 3, 0.8, size=40, bold=True, color=NAVY)
    add_textbox(slide, "Faster than Humans", 9.0, 3.5, 3, 0.4, size=12, color=GRAY)

    add_textbox(slide, "The transition from manual tagging to Hugging Face Transformers eliminates processing bottlenecks and drastically reduces operational costs across publishing and finance sectors.", 1, 5.5, 11.333, 1, size=18, color=GRAY, align=PP_ALIGN.CENTER)

    # --- SAVE ---
    out_path = os.path.join(os.path.dirname(__file__), "News_Classification_Short.pptx")
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path}")

if __name__ == "__main__":
    build_short_presentation()
