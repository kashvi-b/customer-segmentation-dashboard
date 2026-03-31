def get_segment_insight(segment_name: str, avg_spend: float,
                        avg_frequency: float, count: int,
                        avg_recency: float) -> str:
    """Generate marketing insights using rules — no API needed."""

    # Build profile sentence
    if avg_spend > 600:
        spend_desc = "high-value spenders who contribute significantly to revenue"
    elif avg_spend > 300:
        spend_desc = "moderate spenders with solid purchasing power"
    else:
        spend_desc = "low-spend customers who may need stronger incentives"

    if avg_frequency >= 7:
        freq_desc = "They purchase very frequently, showing strong brand loyalty."
    elif avg_frequency >= 4:
        freq_desc = "They buy regularly throughout the year."
    else:
        freq_desc = "They purchase infrequently and may need re-engagement."

    if avg_recency < 60:
        recency_desc = "recently active"
    elif avg_recency < 180:
        recency_desc = "moderately recent"
    else:
        recency_desc = "at risk of churning due to inactivity"

    profile = (
        f"PROFILE: The '{segment_name}' segment consists of {spend_desc}. "
        f"{freq_desc} They are {recency_desc} "
        f"(avg {avg_recency:.0f} days since last purchase)."
    )

    # Build action recommendation
    if avg_recency > 180:
        action = "ACTION: Launch a win-back campaign with a time-limited discount (e.g. '20% off — we miss you!') to re-engage dormant customers."
    elif avg_spend > 600 and avg_frequency >= 6:
        action = "ACTION: Introduce a VIP loyalty programme with exclusive early access to new products and free shipping to retain these top customers."
    elif avg_spend > 300:
        action = "ACTION: Send personalised upsell emails recommending premium products based on past purchases to grow their average order value."
    elif avg_frequency < 3:
        action = "ACTION: Offer a 'buy 2 get 1 free' promotion or bundle deal to increase purchase frequency among occasional buyers."
    else:
        action = "ACTION: Run a referral programme offering discounts to customers who bring in new buyers — this segment has solid loyalty to leverage."

    # Build email subject line
    if avg_recency > 180:
        subject = "EMAIL SUBJECT: \"We miss you, {first_name} — here's 20% off just for you\""
    elif avg_spend > 600:
        subject = "EMAIL SUBJECT: \"{first_name}, you're one of our VIPs — here's something special\""
    elif avg_frequency >= 6:
        subject = "EMAIL SUBJECT: \"Thank you for being a loyal customer — exclusive offer inside\""
    elif avg_spend < 200:
        subject = "EMAIL SUBJECT: \"A deal we picked just for you, {first_name}\""
    else:
        subject = "EMAIL SUBJECT: \"New arrivals we think you'll love, {first_name}\""

    return f"{profile}\n\n{action}\n\n{subject}"


def generate_campaign_email(segment_name: str, avg_spend: float,
                             avg_frequency: float) -> str:
    """Generate a marketing email body using rules — no API needed."""

    if avg_frequency < 3:
        opener = f"We noticed it's been a while since your last visit, and we wanted to reach out personally."
        offer = "As a thank-you for being a customer, we'd like to offer you an exclusive discount on your next order. Whether you're looking to try something new or restock a favourite, now is a great time."
        cta = "Use code COMEBACK20 at checkout for 20% off. This offer is valid for the next 7 days."
    elif avg_spend > 600:
        opener = f"As one of our most valued customers, you deserve to be the first to know about what's coming next."
        offer = "We're launching an exclusive members-only collection next week, and we're giving you early access before anyone else. Your loyalty means everything to us, and we want to make sure you get first pick."
        cta = "Click below to browse the early access collection. No code needed — your VIP status is already applied."
    elif avg_spend > 300:
        opener = "We've been thinking about what our best customers love most, and we put together something just for you."
        offer = "Based on your purchase history, we've handpicked a selection of products we think you'll enjoy. Plus, for a limited time, we're offering free shipping on all orders over $50."
        cta = "Shop your personalised picks today and use code FORYOU at checkout for an extra 10% off."
    else:
        opener = "Everyone loves a good deal — and we've got one with your name on it."
        offer = "For a limited time, we're running a buy-more-save-more promotion across our most popular categories. The more you explore, the more you save."
        cta = "Visit our store today and use code SAVE15 for 15% off your next purchase. Offer ends Sunday."

    closing = "Thank you for being part of our community. We truly appreciate your support and look forward to serving you again soon."

    return f"{opener}\n\n{offer}\n\n{cta}\n\n{closing}"
