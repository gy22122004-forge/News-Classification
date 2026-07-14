"""
Business Impact & Real-World Use Cases
AI News Classification
"""

def calculate_roi(articles_per_day: int = 10000, manual_cost_per_100: float = 5.0, ai_monthly_cost: float = 42.0) -> dict:
    articles_per_year = articles_per_day * 365
    manual_annual     = (articles_per_year / 100) * manual_cost_per_100
    ai_annual         = ai_monthly_cost * 12
    savings           = manual_annual - ai_annual
    roi_pct           = (savings / ai_annual) * 100

    return {
        "articles_per_year":  articles_per_year,
        "manual_annual_cost": manual_annual,
        "ai_annual_cost":     ai_annual,
        "annual_savings":     savings,
        "roi_percent":        roi_pct,
    }

if __name__ == "__main__":
    print("=" * 50)
    print("  NEWS CLASSIFICATION — BUSINESS IMPACT")
    print("=" * 50)
    
    for daily in [1000, 5000, 10000]:
        roi = calculate_roi(daily)
        print(f"  {daily:>6,} articles/day → saves ${roi['annual_savings']:>10,.0f}/year ({roi['roi_percent']:.0f}% ROI)")
