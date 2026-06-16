from typing import Dict, Any
from backend.schema import ProgramSchema, SchemaField

# Helper to create a schema field dictionary
def f(value, confidence="high", source_url=None, access_date="2026-06-16", conflict=False, conflicting_value=None, conflicting_source_url=None):
    return {
        "value": value,
        "confidence": confidence,
        "source_url": source_url,
        "access_date": access_date,
        "conflict": conflict,
        "conflicting_value": conflicting_value,
        "conflicting_source_url": conflicting_source_url
    }

CACHED_PROFILES: Dict[str, Dict[str, Any]] = {
    "starbucks_rewards": {
        # Category 1: Program Basics
        "program_name": f("Starbucks Rewards", "high", "https://www.starbucks.com/rewards"),
        "brand_name": f("Starbucks Corporation", "high", "https://www.starbucks.com"),
        "industry": f("QSR", "high", "https://www.starbucks.com/rewards"),
        "program_type": f("Points (Stars)", "high", "https://www.starbucks.com/rewards"),
        "geography": f("Global (US, Canada, UK, China, etc.)", "high", "https://www.starbucks.com/rewards"),
        "membership_count": f("34.3 Million active members (US, Q2 2024)", "high", "https://stories.starbucks.com/press/2024/starbucks-reports-q2-fiscal-2024-results/"),
        "program_launch_year": f(2009, "high", "https://www.starbucks.com/rewards/history"),
        "membership_cost": f("Free", "high", "https://www.starbucks.com/rewards/terms"),

        # Category 2: Earn Mechanics
        "base_earn_rate": f("1 Star per $1 spent (regular pay) or 2 Stars per $1 spent (preloaded digital card)", "high", "https://www.starbucks.com/rewards", "2026-06-16", True, "2 Stars per $1 spent on all transactions", "https://www.businesswire.com/news/home/20200721005298/en/"),
        "bonus_earn_categories": f(["Double Star Days", "Star Dashes", "Product Challenges", "Partner Earn (Delta, Marriott)"], "high", "https://www.starbucks.com/rewards"),
        "bonus_earn_rates": f({
            "double_star_days": "2x Stars on all eligible purchases",
            "delta_partner": "1 Delta SkyMile per $1 spent at Starbucks (on linked accounts)",
            "marriott_partner": "Double Stars at Starbucks during Marriott stays (on linked accounts)"
        }, "high", "https://www.starbucks.com/rewards/partners"),
        "non_transactional_earn": f(["Birthday Reward (free drink/food)", "App Games/Streaks", "In-app surveys"], "high", "https://www.starbucks.com/rewards/terms"),
        "earn_cap": f("No cap on earned Stars", "high", "https://www.starbucks.com/rewards/faq"),
        "earn_expiry_activity": f("Stars expire 6 months after the month they were earned, unless earned using a Starbucks credit card", "high", "https://www.starbucks.com/rewards/faq"),

        # Category 3: Burn Mechanics
        "redemption_options": f(["Customizations (extra shot, syrup) - 25 Stars", "Brewed Coffee / Tea / Bakery item - 100 Stars", "Handcrafted Drink / Hot Breakfast - 200 Stars", "Lunch Sandwich / Salad - 300 Stars", "Merchandise / Packaged Coffee - 400 Stars"], "high", "https://www.starbucks.com/rewards"),
        "minimum_redemption_threshold": f("25 Stars", "high", "https://www.starbucks.com/rewards/faq"),
        "point_value_cpp": f(4.5, "medium", "https://thepointsguy.com/guide/starbucks-rewards-guide/"),
        "points_expiry_policy": f("6 months rolling from earning month", "high", "https://www.starbucks.com/rewards/faq"),
        "cashback_rate": f("N/A", "high", "https://www.starbucks.com/rewards/faq"),

        # Category 4: Tier System
        "tier_count": f(1, "high", "https://www.starbucks.com/rewards/terms"),  # Single tier with milestone redemptions
        "tier_names": f(["Green / Base Member"], "high", "https://www.starbucks.com/rewards/terms"),
        "tier_qualification_criteria": f(["0 Stars (Free sign up)"], "high", "https://www.starbucks.com/rewards/terms"),
        "tier_qualification_period": f("N/A", "high", "https://www.starbucks.com/rewards/faq"),
        "tier_benefits": f({
            "Green / Base Member": [
                "Free birthday drink or food item",
                "Free refills on brewed coffee and tea (in-store)",
                "Mobile Order & Pay access",
                "Exclusive member offers and games"
            ]
        }, "high", "https://www.starbucks.com/rewards/terms"),
        "tier_status_expiry": f("N/A", "high", "https://www.starbucks.com/rewards/faq"),

        # Category 5: Partnerships
        "partner_names": f(["Delta Air Lines", "Marriott Bonvoy", "Bank of America"], "high", "https://www.starbucks.com/rewards/partners"),
        "partnership_type_per_partner": f({
            "Delta Air Lines": "Both (Earn miles on Starbucks spend; double Stars on Delta travel days)",
            "Marriott Bonvoy": "Both (Earn Marriott points on streaks; double Stars on Starbucks during hotel stays)",
            "Bank of America": "Earn (Earn 2% cash back and 2x Stars when using linked BofA cards)"
        }, "high", "https://www.starbucks.com/rewards/partners"),
        "partnership_details": f([
            "Delta link: 1 SkyMile per $1 spent at Starbucks (excluding taxes & tips)",
            "Marriott link: 100 Marriott Bonvoy points per 3-visit streak in a week",
            "BofA link: 2% cash back and 2x Stars on all Starbucks purchases with linked cards"
        ], "high", "https://www.starbucks.com/rewards/partners"),
        "co_brand_card": f("No (discontinued Starbucks Rewards Visa Card by Chase in July 2023)", "high", "https://www.chase.com/personal/credit-cards/starbucks"),

        # Category 6: Digital Experience
        "mobile_app_available": f("Both (iOS & Android)", "high", "https://www.starbucks.com/rewards"),
        "app_rating_ios": f(4.8, "high", "https://apps.apple.com/us/app/starbucks/id331177714"),
        "app_rating_android": f(4.7, "high", "https://play.google.com/store/apps/details?id=com.starbucks.mobilecard"),
        "app_review_count": f("3.2 Million (App Store) + 1.1 Million (Google Play)", "medium", "https://apps.apple.com/us/app/starbucks/id331177714"),
        "personalization_features": f(["Deep Learning AI engine (Deep Brew) for personalized food/drink offers", "Localized recommendations based on weather and time of day", "Previous order quick-reorder"], "high", "https://stories.starbucks.com/stories/2019/how-starbucks-is-using-artificial-intelligence-to-connect-with-customers/"),
        "gamification_features": f(["Star Dashes (visit 3 days in a row for 50 Stars)", "Shake & Win games", "Progress bars", "Streaks"], "high", "https://www.starbucks.com/rewards"),
        "digital_only_benefits": f(["Mobile Order & Pay", "Order tracking", "Exclusive app-only games", "In-app digital card management"], "high", "https://www.starbucks.com/rewards/terms"),

        # Category 7: Member Sentiment
        "overall_sentiment": f("Mixed", "medium", "https://www.reddit.com/r/starbucks/"),
        "common_praise": f([
            "Highly convenient mobile ordering and checkout process",
            "Free refills on drip coffee and tea in-store make it great for working",
            "Gamified challenges and double star days make earning fast"
        ], "medium", "https://www.reddit.com/r/starbucks/"),
        "common_complaints": f([
            "Recent points devaluations (e.g., handcrafted drinks moving from 150 to 200 Stars in 2023)",
            "Stars expire too quickly (6 months) compared to other programs",
            "App glitches during peak hours causing ordering delays"
        ], "medium", "https://www.trustpilot.com/review/www.starbucks.com"),
        "sentiment_sources_checked": f([
            "https://www.reddit.com/r/starbucks/",
            "https://www.trustpilot.com/review/www.starbucks.com",
            "https://apps.apple.com/us/app/starbucks/id331177714"
        ], "high", "https://www.starbucks.com/rewards"),
        "nps_score": f(30, "low", "https://customer.guru/nps/starbucks"),

        # Category 8: Competitive Position
        "key_differentiators": f([
            "Pioneered mobile-order-and-pay integrations, creating an industry-standard daily habit loop",
            "Industry-leading partnership ecosystem allowing cross-loyalty earning (airline, hotel, banking)",
            "Massive scale of pre-loaded digital cash acting as an interest-free loan to the corporation (~$1.6B)"
        ], "high", "https://www.starbucks.com/rewards"),
        "known_weaknesses": f([
            "Perceived high frequency of points devaluations, harming long-term trust",
            "Discontinuance of co-brand credit card reduces direct financial acquisition channels",
            "Inability to transfer points to partner programs (only earn-crossways)"
        ], "high", "https://www.starbucks.com/rewards"),
        "closest_competitors": f(["Dunkin' Rewards", "McDonald's MyMcDonald's Rewards", "Dutch Bros Rewards", "Panera Unlimited Sip Club"], "high", "https://www.starbucks.com/rewards"),
        "recent_changes": f([
            "Introduced partnership with Marriott Bonvoy (June 2024)",
            "Introduced partnership with Bank of America (April 2024)",
            "Devalued several reward tiers (February 2023) - e.g., hot coffee from 50 to 100 Stars, cold drinks from 150 to 200 Stars"
        ], "high", "https://stories.starbucks.com/press/2024/starbucks-and-marriott-bonvoy-launch-new-loyalty-collaboration/")
    },

    "mcdonalds_rewards": {
        # Category 1: Program Basics
        "program_name": f("MyMcDonald's Rewards", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "brand_name": f("McDonald's Corporation", "high", "https://www.mcdonalds.com"),
        "industry": f("QSR", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "program_type": f("Points", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "geography": f("Global (US, UK, Canada, Australia, etc.)", "high", "https://www.mcdonalds.com"),
        "membership_count": f("150 Million active global members, 34 Million in US (2024)", "high", "https://www.reuters.com/business/retail-consumer/mcdonalds-targets-50000-restaurants-100-mln-new-loyalty-members-by-2027-2023-12-06/"),
        "program_launch_year": f(2021, "high", "https://corporate.mcdonalds.com/corpmcd/our-stories/article/mymcd-rewards-us.html"),
        "membership_cost": f("Free", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),

        # Category 2: Earn Mechanics
        "base_earn_rate": f("100 Points per $1 spent", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "bonus_earn_categories": f(["App-only Promos", "Double Points Days", "Welcome Bonus (free fries on first order)"], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "bonus_earn_rates": f({
            "welcome_bonus": "1,500 bonus points on first loyalty order",
            "specific_promos": "Varies (e.g. 2x points on Breakfast items)"
        }, "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "non_transactional_earn": f(["Birthday Rewards", "Promotional App Challenges"], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "earn_cap": f("No cap on points earned per day", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards/faq.html"),
        "earn_expiry_activity": f("Points expire on the first day of the month after the 6th month from the date they were earned", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards/faq.html"),

        # Category 3: Burn Mechanics
        "redemption_options": f(["Tier 1 (1500 Points): Hash Brown, Vanilla Cone, McChicken, Cheeseburger", "Tier 2 (3000 Points): Medium Fries, Sausage Burrito, 6pc McNuggets", "Tier 3 (4500 Points): Large Fries, Large Frappe, Filet-O-Fish", "Tier 4 (6000 Points): Big Mac, Quarter Pounder with Cheese, Happy Meal"], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "minimum_redemption_threshold": f("1,500 Points", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "point_value_cpp": f(0.08, "medium", "https://thepointsguy.com/guide/mymcdonalds-rewards-guide/"),  # 0.08 cents per point (80 cents per $10 spent value equivalent)
        "points_expiry_policy": f("6 months flat from earning date", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards/faq.html"),
        "cashback_rate": f("N/A", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),

        # Category 4: Tier System
        "tier_count": f(1, "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "tier_names": f(["Standard Member"], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "tier_qualification_criteria": f(["0 Points (Free signup)"], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "tier_qualification_period": f("N/A", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "tier_benefits": f({
            "Standard Member": [
                "100 points per $1 spent",
                "Access to exclusive daily deals and discounts",
                "Mobile ordering & curbside pickup",
                "Free food redemptions across four distinct reward tiers"
            ]
        }, "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "tier_status_expiry": f("N/A", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards/faq.html"),

        # Category 5: Partnerships
        "partner_names": f([], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "partnership_type_per_partner": f({}, "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "partnership_details": f([], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),
        "co_brand_card": f("No co-brand credit card available", "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards/faq.html"),

        # Category 6: Digital Experience
        "mobile_app_available": f("Both (iOS & Android)", "high", "https://www.mcdonalds.com"),
        "app_rating_ios": f(4.7, "high", "https://apps.apple.com/us/app/mcdonalds/id922103900"),
        "app_rating_android": f(4.5, "high", "https://play.google.com/store/apps/details?id=com.mcdonalds.mobileapp"),
        "app_review_count": f("4.1 Million (App Store) + 2.3 Million (Google Play)", "medium", "https://apps.apple.com/us/app/mcdonalds/id922103900"),
        "personalization_features": f(["Personalized daily coupons based on past purchase habits", "Geo-targeted breakfast and late-night deals", "Frictionless reordering of favorite combos"], "high", "https://corporate.mcdonalds.com/corpmcd/our-stories/article/mymcd-rewards-us.html"),
        "gamification_features": f(["Seasonal sweepstakes (e.g. Monopoly in-app integration)", "Occasional food order streak challenges"], "medium", "https://www.mcdonalds.com"),
        "digital_only_benefits": f(["Exclusive app coupon codes (e.g. Free Fries on Friday with $1 purchase)", "App-only free items promotions", "Mobile Order & Pay and Curbside Pickup"], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards.html"),

        # Category 7: Member Sentiment
        "overall_sentiment": f("Mixed", "medium", "https://www.reddit.com/r/mcdonalds/"),
        "common_praise": f([
            "Generous app-only discount coupons (such as 20% off $10+ orders or BOGO deals)",
            "Extremely fast points accumulation (100 points per $1 makes balances look massive)",
            "Simple, straightforward redemption categories"
        ], "medium", "https://www.reddit.com/r/mcdonalds/"),
        "common_complaints": f([
            "Short point expiration window (6 months flat with no activity-based extension)",
            "Only one coupon or reward can be used per order, preventing stacking",
            "App freezes, fails to load checkout codes, or crashes during payment"
        ], "medium", "https://www.trustpilot.com/review/www.mcdonalds.com"),
        "sentiment_sources_checked": f([
            "https://www.reddit.com/r/mcdonalds/",
            "https://www.trustpilot.com/review/www.mcdonalds.com",
            "https://apps.apple.com/us/app/mcdonalds/id922103900"
        ], "high", "https://www.mcdonalds.com"),
        "nps_score": f(12, "low", "https://customer.guru/nps/mcdonalds"),

        # Category 8: Competitive Position
        "key_differentiators": f([
            "Extremely high base earn rate multiplier (100x face value) creating strong user reward feedback loops",
            "Aggressive couponing integrated directly alongside points, driving high weekly app engagement",
            "Massive scale with over 150 million active global members driving digital sales to ~40% of system sales"
        ], "high", "https://corporate.mcdonalds.com/corpmcd/our-stories/article/mymcd-rewards-us.html"),
        "known_weaknesses": f([
            "Total lack of non-QSR partnerships (unlike Starbucks' Delta/Marriott integrations)",
            "Strict 1-deal-per-transaction limit limits utility for large family orders",
            "Relatively quick point expiration (6 months) with no way to halt via purchase activity"
        ], "high", "https://www.mcdonalds.com/us/en-us/mymcdonalds-rewards/faq.html"),
        "closest_competitors": f(["Burger King Royal Perks", "Wendy's Rewards", "Taco Bell Rewards", "Starbucks Rewards"], "high", "https://www.mcdonalds.com"),
        "recent_changes": f([
            "Announced plan to expand active membership from 150 million to 250 million by 2027 (Dec 2023)",
            "Restructured redemption thresholds in select international markets (2024)"
        ], "high", "https://www.reuters.com/business/retail-consumer/mcdonalds-targets-50000-restaurants-100-mln-new-loyalty-members-by-2027-2023-12-06/")
    },

    "sephora_beauty_insider": {
        # Category 1: Program Basics
        "program_name": f("Beauty Insider", "high", "https://www.sephora.com/about-beauty-insider"),
        "brand_name": f("Sephora (LVMH)", "high", "https://www.sephora.com"),
        "industry": f("Retail", "high", "https://www.sephora.com/about-beauty-insider"),
        "program_type": f("Tiered Points", "high", "https://www.sephora.com/about-beauty-insider"),
        "geography": f("North America (US & Canada), international variations run separately", "high", "https://www.sephora.com"),
        "membership_count": f("34 Million active members (US/Canada, 2023)", "medium", "https://www.insiderintelligence.com/content/sephora-loyalty-program-beauty-insider-success-insider-rewards"),
        "program_launch_year": f(2007, "high", "https://www.sephora.com/about-beauty-insider"),
        "membership_cost": f("Free", "high", "https://www.sephora.com/about-beauty-insider"),

        # Category 2: Earn Mechanics
        "base_earn_rate": f("1 Point per $1 spent", "high", "https://www.sephora.com/about-beauty-insider"),
        "bonus_earn_categories": f(["Multiplier Events (e.g., 4x points on fragrance)", "Credit Card purchases", "Co-branded Kohl's Sephora purchases"], "high", "https://www.sephora.com/about-beauty-insider"),
        "bonus_earn_rates": f({
            "insider_tier": "1 Point per $1 base",
            "vib_tier": "1 Point per $1 base (plus tier multiplier events)",
            "rouge_tier": "1 Point per $1 base (plus higher tier multiplier events)",
            "credit_card": "4% back in rewards / 4x points at Sephora"
        }, "high", "https://www.sephora.com/about-beauty-insider/terms"),
        "non_transactional_earn": f(["Birthday gift selection (no purchase necessary in-store)", "End-of-year bonus points challenges", "Beauty Insider Community review writing"], "high", "https://www.sephora.com/about-beauty-insider"),
        "earn_cap": f("No cap on points earned", "high", "https://www.sephora.com/about-beauty-insider/faq"),
        "earn_expiry_activity": f("Points expire if account is inactive (no purchase or redemption activity) for 12 consecutive months", "high", "https://www.sephora.com/about-beauty-insider/faq"),

        # Category 3: Burn Mechanics
        "redemption_options": f(["Beauty Insider Cash ($10 off) - 500 points", "Sample size products - 100-250 points", "Full-size products or custom merch - 500-2000 points", "Charity donations - 500 points", "Beauty Studio services - 1000+ points", "Rouge Reward ($100 reward) - 2500 points (Rouge only)"], "high", "https://www.sephora.com/about-beauty-insider"),
        "minimum_redemption_threshold": f("100 points (samples) or 500 points ($10 cash)", "high", "https://www.sephora.com/about-beauty-insider/faq"),
        "point_value_cpp": f(2.0, "medium", "https://thepointsguy.com/guide/sephora-beauty-insider-rewards-guide/"),  # 2.0 cpp on Beauty Insider Cash, higher on Rouge rewards (~4.0 cpp)
        "points_expiry_policy": f("12 months inactivity reset", "high", "https://www.sephora.com/about-beauty-insider/faq"),
        "cashback_rate": f("Effective 2% cashback via Beauty Insider Cash (500 pts = $10)", "high", "https://www.sephora.com/about-beauty-insider"),

        # Category 4: Tier System
        "tier_count": f(3, "high", "https://www.sephora.com/about-beauty-insider"),
        "tier_names": f(["Insider", "VIB (Very Important Beauty)", "Rouge"], "high", "https://www.sephora.com/about-beauty-insider"),
        "tier_qualification_criteria": f(["Insider: Free sign up", "VIB: Spend $350 in a calendar year", "Rouge: Spend $1,000 in a calendar year"], "high", "https://www.sephora.com/about-beauty-insider"),
        "tier_qualification_period": f("Calendar Year (January 1 - December 31)", "high", "https://www.sephora.com/about-beauty-insider/terms"),
        "tier_benefits": f({
            "Insider": [
                "Free birthday gift",
                "Standard seasonal savings events access (10% off)",
                "Free standard shipping (no minimum spend)",
                "1 point per $1 earned"
            ],
            "VIB": [
                "All Insider benefits",
                "Medium seasonal savings events access (15% off)",
                "Exclusive VIB gifts and products",
                "1 point per $1 earned + priority multiplier events"
            ],
            "Rouge": [
                "All VIB benefits",
                "Highest seasonal savings events access (20% off)",
                "Access to the $100 Rouge Reward (2,500 points)",
                "Early access to product launches",
                "Free custom beauty services and priority support"
            ]
        }, "high", "https://www.sephora.com/about-beauty-insider"),
        "tier_status_expiry": f("Status lasts for the remainder of the calendar year in which you qualify, plus the following calendar year", "high", "https://www.sephora.com/about-beauty-insider/terms"),

        # Category 5: Partnerships
        "partner_names": f(["Kohl's", "Instacart", "DoorDash"], "high", "https://www.sephora.com/about-beauty-insider"),
        "partnership_type_per_partner": f({
            "Kohl's": "Both (Earn and redeem Beauty Insider points at Sephora at Kohl's locations)",
            "Instacart": "Earn (Earn points on same-day delivery orders)",
            "DoorDash": "Earn (Earn points on same-day delivery orders)"
        }, "high", "https://www.sephora.com/about-beauty-insider"),
        "partnership_details": f([
            "Kohl's: Sephora at Kohl's purchases link seamlessly to beauty insider accounts. Kohl's rewards can sometimes be stacked.",
            "Same-Day Delivery: Members can link accounts on Instacart/DoorDash to earn 1 pt per $1."
        ], "high", "https://www.sephora.com/about-beauty-insider/faq"),
        "co_brand_card": f("Yes (Sephora Credit Card & Visa Card issued by Comenity Bank)", "high", "https://www.sephora.com/about-beauty-insider/credit-card"),

        # Category 6: Digital Experience
        "mobile_app_available": f("Both (iOS & Android)", "high", "https://www.sephora.com"),
        "app_rating_ios": f(4.9, "high", "https://apps.apple.com/us/app/sephora-buy-makeup-skincare/id393328038"),
        "app_rating_android": f(4.6, "high", "https://play.google.com/store/apps/details?id=com.sephora"),
        "app_review_count": f("2.5 Million (App Store) + 400K (Google Play)", "medium", "https://apps.apple.com/us/app/sephora-buy-makeup-skincare/id393328038"),
        "personalization_features": f(["Virtual Artist (AR makeup try-on in app)", "Color IQ matching (find foundations matching skin tone)", "Personalized product recommendations based on beauty quiz"], "high", "https://www.sephora.com/beauty/color-iq"),
        "gamification_features": f(["Beauty Insider Challenges (complete 4 tasks to earn 500 bonus points)", "App badges"], "high", "https://www.sephora.com/about-beauty-insider"),
        "digital_only_benefits": f(["Exclusive app-only product drops", "Virtual try-on services", "App-only sales events"], "high", "https://www.sephora.com/about-beauty-insider"),

        # Category 7: Member Sentiment
        "overall_sentiment": f("Mixed", "medium", "https://www.reddit.com/r/Sephora/"),
        "common_praise": f([
            "Excellent birthday gifts, which are often premium sample bundles",
            "Free shipping with no minimum spend threshold makes small purchases easy",
            "High-value seasonal discounts (20% off for Rouge members)"
        ], "medium", "https://www.reddit.com/r/Sephora/"),
        "common_complaints": f([
            "The Rewards Bazaar sample items are extremely hard to secure and sell out within minutes of posting",
            "Beauty Insider Cash ($10 for 500 points) is perceived as low value compared to Ulta's dollar-matching system",
            "VIB tier feels neglected, offering very few meaningful differentiators from the base Insider tier"
        ], "medium", "https://www.trustpilot.com/review/www.sephora.com"),
        "sentiment_sources_checked": f([
            "https://www.reddit.com/r/Sephora/",
            "https://www.trustpilot.com/review/www.sephora.com",
            "https://apps.apple.com/us/app/sephora-buy-makeup-skincare/id393328038"
        ], "high", "https://www.sephora.com"),
        "nps_score": f(58, "low", "https://customer.guru/nps/sephora"),

        # Category 8: Competitive Position
        "key_differentiators": f([
            "Extremely strong community-building through app-based forums and beauty reviews",
            "High-value experiential rewards (trips, brand founder meetups) inside the Rewards Bazaar",
            "The Rouge tier's 20% discount event creates a massive twice-yearly hoarding and purchase cycle"
        ], "high", "https://www.sephora.com/about-beauty-insider"),
        "known_weaknesses": f([
            "Lower point value compared to closest competitor (Ulta Beauty Rewards, which allows point values to scale up to 6.25cpp)",
            "High threshold ($1000/yr) for the only tier that gets early access and deep discounts",
            "Frequent stockouts of points redemption items"
        ], "high", "https://www.sephora.com/about-beauty-insider"),
        "closest_competitors": f(["Ulta Beauty Rewards", "Macy's Star Rewards", "Nordstromy Club", "Target Circle"], "high", "https://www.sephora.com"),
        "recent_changes": f([
            "Launched Beauty Insider Challenges (Sept 2023) giving members ways to earn points by doing tasks like in-store pickup",
            "Updated shipping policy to make free standard shipping available to all members (2022)"
        ], "high", "https://www.sephora.com/about-beauty-insider")
    },

    "marriott_bonvoy": {
        # Category 1: Program Basics
        "program_name": f("Marriott Bonvoy", "high", "https://www.marriott.com/loyalty.mi"),
        "brand_name": f("Marriott International, Inc.", "high", "https://www.marriott.com"),
        "industry": f("Hospitality", "high", "https://www.marriott.com/loyalty.mi"),
        "program_type": f("Tiered Points", "high", "https://www.marriott.com/loyalty.mi"),
        "geography": f("Global (10,000+ properties in 140+ countries)", "high", "https://www.marriott.com"),
        "membership_count": f("203 Million global members (Q1 2024)", "high", "https://marriott.gcs-web.com/news-releases/news-release-details/marriott-international-reports-first-quarter-2024-results"),
        "program_launch_year": f(2019, "high", "https://www.marriott.com/loyalty/history.mi"),  # Formed by merging Marriott Rewards, Ritz-Carlton Rewards, and Starwood Preferred Guest (SPG)
        "membership_cost": f("Free", "high", "https://www.marriott.com/loyalty.mi"),

        # Category 2: Earn Mechanics
        "base_earn_rate": f("10 Points per $1 spent at most brands (5 points per $1 at Element, Residence Inn, and TownePlace Suites)", "high", "https://www.marriott.com/loyalty/earn/hotels.mi"),
        "bonus_earn_categories": f(["Elite Status Bonuses (up to 75%)", "Co-brand Credit Cards", "Partner programs (Uber, Hertz, Starbucks)"], "high", "https://www.marriott.com/loyalty/earn/hotels.mi"),
        "bonus_earn_rates": f({
            "silver_bonus": "+10% bonus points on hotel spend",
            "gold_bonus": "+25% bonus points on hotel spend",
            "platinum_bonus": "+50% bonus points on hotel spend",
            "titanium_bonus": "+75% bonus points on hotel spend",
            "ambassador_bonus": "+75% bonus points on hotel spend",
            "uber_partner": "3x points on Uber Premium rides and 2x points on Uber Eats orders of $40+ (linked accounts)"
        }, "high", "https://www.marriott.com/loyalty/terms/default.mi"),
        "non_transactional_earn": f(["Co-brand Credit Card signup bonuses", "Marriott Bonvoy Events (meetings/groups)", "Point purchase promotions", "Partner car rentals (Hertz)"], "high", "https://www.marriott.com/loyalty/earn/hotels.mi"),
        "earn_cap": f("No cap on points earned", "high", "https://www.marriott.com/loyalty/faq.mi"),
        "earn_expiry_activity": f("Points expire after 24 months of inactivity (no hotel stays, card spend, or transfers)", "high", "https://www.marriott.com/loyalty/faq.mi"),

        # Category 3: Burn Mechanics
        "redemption_options": f(["Award Stays (hotels) - Free night awards starting at 5000 points", "Points + Cash awards", "Transfer to Airlines (40+ airlines, usually 3:1 ratio)", "Marriott Bonvoy Moments (experiences, concert suites)", "Merchandise & Gift Cards", "Car rentals"], "high", "https://www.marriott.com/loyalty/redeem.mi"),
        "minimum_redemption_threshold": f("5,000 points for hotel stay / 3,000 points to transfer to select airlines", "high", "https://www.marriott.com/loyalty/redeem.mi"),
        "point_value_cpp": f(0.8, "medium", "https://thepointsguy.com/guide/marriott-bonvoy-points-value/"),  # Average value is ~0.8 cents per point
        "points_expiry_policy": f("24 months rolling inactivity reset", "high", "https://www.marriott.com/loyalty/faq.mi"),
        "cashback_rate": f("N/A", "high", "https://www.marriott.com/loyalty.mi"),

        # Category 4: Tier System
        "tier_count": f(6, "high", "https://www.marriott.com/loyalty/member-benefits.mi"),
        "tier_names": f(["Member", "Silver Elite", "Gold Elite", "Platinum Elite", "Titanium Elite", "Ambassador Elite"], "high", "https://www.marriott.com/loyalty/member-benefits.mi"),
        "tier_qualification_criteria": f([
            "Member: 0-9 nights/year",
            "Silver Elite: 10 nights/year",
            "Gold Elite: 25 nights/year",
            "Platinum Elite: 50 nights/year",
            "Titanium Elite: 75 nights/year",
            "Ambassador Elite: 100 nights/year + $23,000 qualifying spend"
        ], "high", "https://www.marriott.com/loyalty/member-benefits.mi", "2026-06-16", True, "Ambassador requires 100 nights + $20,000 spend", "https://www.flyertalk.com/forum/marriott-marriott-bonvoy/"),
        "tier_qualification_period": f("Calendar Year (January 1 - December 31)", "high", "https://www.marriott.com/loyalty/terms/default.mi"),
        "tier_benefits": f({
            "Member": ["Free in-room Wi-Fi", "Member rates (up to 5% off)"],
            "Silver Elite": ["All Member benefits", "10% points bonus", "Priority late checkout", "Ultimate Reservation Guarantee"],
            "Gold Elite": ["All Silver benefits", "25% points bonus", "2:00 PM late checkout (subject to availability)", "Enhanced room upgrades", "Welcome gift (250/500 points)"],
            "Platinum Elite": ["All Gold benefits", "50% points bonus", "4:00 PM late checkout (guaranteed at non-resorts)", "Lounge Access / Free Breakfast", "Room upgrade to Select Suites", "Annual Choice Benefit (5 Suite Night Awards, etc.)"],
            "Titanium Elite": ["All Platinum benefits", "75% points bonus", "4:00 PM late checkout", "Room upgrade to standard suites", "Free United MileagePlus Premier Silver status", "Second Annual Choice Benefit"],
            "Ambassador Elite": ["All Titanium benefits", "Your24 (flexible 24-hour stay window check-in/out)", "Personal Ambassador service", "Access to exclusive retreats"]
        }, "high", "https://www.marriott.com/loyalty/member-benefits.mi"),
        "tier_status_expiry": f("Status is valid through February of the second year following qualification (e.g. qualify in Oct 2025, status expires Feb 2027)", "high", "https://www.marriott.com/loyalty/terms/default.mi"),

        # Category 5: Partnerships
        "partner_names": f(["United Airlines", "Delta Air Lines", "Starbucks", "Uber", "Hertz", "Chase", "American Express"], "high", "https://www.marriott.com/loyalty/earn/partners.mi"),
        "partnership_type_per_partner": f({
            "United Airlines": "Both (Points transfer; Titanium Elite gets Premier Silver status; Premier Gold+ gets Bonvoy Gold)",
            "Delta Air Lines": "Both (Linked members get reciprocal points and miles)",
            "Starbucks": "Both (Linked members earn 100 Bonvoy points on streaks; double Stars on travel stays)",
            "Uber": "Earn (Earn Bonvoy points on rides and deliveries)",
            "Hertz": "Earn (Earn points on rentals; Elite members get Hertz status)",
            "Chase": "Both (Co-brand cards, Chase Ultimate Rewards transfer partner)",
            "American Express": "Both (Co-brand cards, Amex Membership Rewards transfer partner)"
        }, "high", "https://www.marriott.com/loyalty/terms/default.mi"),
        "partnership_details": f([
            "United Preferred Partnership: 1:1 transfer bonus (plus 10,000 miles bonus per 60,000 points transferred). Reciprocal Elite status.",
            "Airline Transfer: 3:1 transfer ratio to 40+ airlines, with 5,000 mile bonus for every 60,000 Bonvoy points transferred.",
            "Credit Card transfers: Chase UR and Amex MR points transfer at 1:1 ratio to Marriott."
        ], "high", "https://www.marriott.com/loyalty/earn/partners.mi"),
        "co_brand_card": f("Yes (Chase Marriott Bonvoy Boundless/Bold and Amex Marriott Bonvoy Bevy/Brilliant)", "high", "https://www.marriott.com/loyalty/earn/credit-card-us.mi"),

        # Category 6: Digital Experience
        "mobile_app_available": f("Both (iOS & Android)", "high", "https://www.marriott.com/marriott/mobile-apps.mi"),
        "app_rating_ios": f(4.8, "high", "https://apps.apple.com/us/app/marriott-bonvoy/id351406560"),
        "app_rating_android": f(4.4, "high", "https://play.google.com/store/apps/details?id=com.marriott.intl"),
        "app_review_count": f("1.1 Million (App Store) + 250K (Google Play)", "medium", "https://apps.apple.com/us/app/marriott-bonvoy/id351406560"),
        "personalization_features": f(["Mobile Key (room unlock via app)", "In-app chat with front desk", "Personalized room service and dining offers during stays"], "high", "https://www.marriott.com/marriott/mobile-apps.mi"),
        "gamification_features": f(["Annual choice selection progress tracker", "Elite night credit progress bar", "Periodic in-app promotion dashboards"], "medium", "https://www.marriott.com/loyalty.mi"),
        "digital_only_benefits": f(["Mobile Check-in & Check-out", "Mobile Key access", "App-only room request selections"], "high", "https://www.marriott.com/marriott/mobile-apps.mi"),

        # Category 7: Member Sentiment
        "overall_sentiment": f("Mixed", "medium", "https://www.reddit.com/r/marriott/"),
        "common_praise": f([
            "Unrivaled hotel portfolio footprint means you can earn/redeem in almost any city on Earth",
            "Platinum Elite benefits (lounge access and free breakfast) provide substantial tangible savings",
            "Co-branded credit cards make earning points and reaching elite status nights very easy"
        ], "medium", "https://www.reddit.com/r/marriott/"),
        "common_complaints": f([
            "Dynamic award pricing introduced in 2022 has significantly inflated points costs for luxury resorts",
            "Suite Night Awards (now Nightly Upgrade Awards) are frequently denied due to tight availability",
            "'Bonvoyed' is a common community slang for service failures, points booking issues, or status downgrades"
        ], "medium", "https://www.flyertalk.com/forum/marriott-marriott-bonvoy/"),
        "sentiment_sources_checked": f([
            "https://www.reddit.com/r/marriott/",
            "https://www.flyertalk.com/forum/marriott-marriott-bonvoy/",
            "https://apps.apple.com/us/app/marriott-bonvoy/id351406560"
        ], "high", "https://www.marriott.com"),
        "nps_score": f(28, "low", "https://customer.guru/nps/marriott-hotels-and-resorts"),

        # Category 8: Competitive Position
        "key_differentiators": f([
            "Massive portfolio scale (30+ brands) covering everything from budget hotels to ultra-luxury (Ritz-Carlton, St. Regis)",
            "Robust airline transfer ecosystem supporting 40+ carriers, acting as a flexible currency for frequent flyers",
            "Strong corporate partnerships (United, Delta, Starbucks) that keep members engaged even when they aren't traveling"
        ], "high", "https://www.marriott.com/loyalty.mi"),
        "known_weaknesses": f([
            "Dynamic pricing structure makes point values highly variable and subject to inflation",
            "Weak elite benefits at mid-tiers (Gold gets no lounge access or breakfast compared to Hilton Gold)",
            "Complex Terms & Conditions with many brand-specific exclusions (e.g. no breakfast at Ritz-Carlton)"
        ], "high", "https://www.marriott.com/loyalty/terms/default.mi"),
        "closest_competitors": f(["Hilton Honors", "World of Hyatt", "IHG One Rewards", "Wyndham Rewards"], "high", "https://www.marriott.com"),
        "recent_changes": f([
            "Rebranded Suite Night Awards to 'Nightly Upgrade Awards' with expanded participating brands (Jan 2024)",
            "Launched partnership with Starbucks Rewards allowing points linkage (June 2024)",
            "Increased minimum spend qualification for Ambassador Elite status to $23,000 per year (Jan 2023)"
        ], "high", "https://marriott.gcs-web.com/news-releases/news-release-details/marriott-bonvoy-and-starbucks-launch-new-collaboration")
    },

    "delta_skymiles": {
        # Category 1: Program Basics
        "program_name": f("Delta SkyMiles", "high", "https://www.delta.com/skymiles"),
        "brand_name": f("Delta Air Lines, Inc.", "high", "https://www.delta.com"),
        "industry": f("Airline", "high", "https://www.delta.com/skymiles"),
        "program_type": f("Tiered Miles", "high", "https://www.delta.com/skymiles"),
        "geography": f("Global (with SkyTeam Alliance network)", "high", "https://www.delta.com"),
        "membership_count": f("Over 100 Million members globally (2023)", "medium", "https://stories.delta.com/delta-skymiles-program-evolution-focus-on-customers"),
        "program_launch_year": f(1981, "high", "https://www.delta.com/skymiles"),
        "membership_cost": f("Free", "high", "https://www.delta.com/skymiles/terms"),

        # Category 2: Earn Mechanics
        "base_earn_rate": f("5 Miles per $1 spent on ticket price (excluding government taxes & fees)", "high", "https://www.delta.com/us/en/skymiles/how-to-earn-miles/earn-on-flights"),
        "bonus_earn_categories": f(["Medallion Elite Bonuses (up to 120%)", "Co-branded credit card spend", "Partner spend (Lyft, Starbucks, Hertz)"], "high", "https://www.delta.com/us/en/skymiles/how-to-earn-miles/earn-on-flights"),
        "bonus_earn_rates": f({
            "silver_bonus": "+2 Miles per $1 (total 7x)",
            "gold_bonus": "+3 Miles per $1 (total 8x)",
            "platinum_bonus": "+4 Miles per $1 (total 9x)",
            "diamond_bonus": "+6 Miles per $1 (total 11x)",
            "lyft_partner": "2 miles per $1 on airport rides, 1 mile per $1 on others (linked accounts)"
        }, "high", "https://www.delta.com/us/en/skymiles/medallion-program/medallion-benefits"),
        "non_transactional_earn": f(["Amex Credit Card signup bonuses", "Delta SkyMiles Shopping Portal", "Delta SkyMiles Dining", "Car rentals & hotel booking partners"], "high", "https://www.delta.com/us/en/skymiles/how-to-earn-miles/earn-with-partners"),
        "earn_cap": f("No cap on miles earned", "high", "https://www.delta.com/skymiles/faq"),
        "earn_expiry_activity": f("SkyMiles NEVER expire (unconditional)", "high", "https://www.delta.com/skymiles/faq"),

        # Category 3: Burn Mechanics
        "redemption_options": f(["Award flights on Delta and 20+ partner airlines", "Pay with Miles (Amex cardholders only, 1 cent per mile)", "Seat Upgrades", "Delta Sky Club memberships", "Delta Vacations packages", "Merchandise & SkyMiles experiences"], "high", "https://www.delta.com/us/en/skymiles/use-miles/overview"),
        "minimum_redemption_threshold": f("Varies, domestic award flights start around 5,000 miles", "high", "https://www.delta.com/us/en/skymiles/use-miles/overview"),
        "point_value_cpp": f(1.2, "medium", "https://thepointsguy.com/guide/guide-to-delta-skymiles/"),  # Average value is ~1.2 cents per mile
        "points_expiry_policy": f("Miles do not expire", "high", "https://www.delta.com/skymiles/faq"),
        "cashback_rate": f("N/A", "high", "https://www.delta.com/skymiles"),

        # Category 4: Tier System
        "tier_count": f(5, "high", "https://www.delta.com/us/en/skymiles/medallion-program/overview"),
        "tier_names": f(["General Member", "Silver Medallion", "Gold Medallion", "Platinum Medallion", "Diamond Medallion"], "high", "https://www.delta.com/us/en/skymiles/medallion-program/overview"),
        "tier_qualification_criteria": f([
            "General Member: 0 Medallion Qualifying Dollars (MQD)",
            "Silver Medallion: 5,000 MQD",
            "Gold Medallion: 10,000 MQD",
            "Platinum Medallion: 15,000 MQD",
            "Diamond Medallion: 28,000 MQD"
        ], "high", "https://www.delta.com/us/en/skymiles/medallion-program/how-to-qualify", "2026-06-16", True, "Diamond requires $35,000 MQD", "https://www.reddit.com/r/delta/"),  # Massive rules changes in 2024
        "tier_qualification_period": f("Calendar Year (January 1 - December 31)", "high", "https://www.delta.com/us/en/skymiles/medallion-program/how-to-qualify"),
        "tier_benefits": f({
            "General Member": ["Earn 5x miles", "Free Wi-Fi on most domestic flights (linked accounts)"],
            "Silver Medallion": ["All General benefits", "7x earning", "Unlimited Complimentary Upgrades (1 day prior)", "Free checked bag", "Priority boarding"],
            "Gold Medallion": ["All Silver benefits", "8x earning", "Unlimited Complimentary Upgrades (3 days prior)", "SkyTeam Elite Plus status (lounge access on international flights)", "Waived baggage fees", "Priority security lines"],
            "Platinum Medallion": ["All Gold benefits", "9x earning", "Unlimited Complimentary Upgrades (5 days prior, cleared instantly to Comfort+)", "Annual Choice Benefit (Regional Upgrade Certs, bonus miles)", "Hertz President's Circle status"],
            "Diamond Medallion": ["All Platinum benefits", "11x earning", "Highest upgrade priority", "Three Annual Choice Benefits (Global Upgrade Certs, Sky Club membership, etc.)", "VIP customer support line"]
        }, "high", "https://www.delta.com/us/en/skymiles/medallion-program/medallion-benefits"),
        "tier_status_expiry": f("Medallion status lasts for the remainder of the calendar year in which it was earned, plus the entire next calendar year, expiring on Jan 31 of the following year", "high", "https://www.delta.com/us/en/skymiles/medallion-program/how-to-qualify"),

        # Category 5: Partnerships
        "partner_names": f(["American Express", "SkyTeam Alliance (Air France, KLM, etc.)", "Starbucks", "Lyft", "Hertz", "Instacart"], "high", "https://www.delta.com/us/en/skymiles/how-to-earn-miles/earn-with-partners"),
        "partnership_type_per_partner": f({
            "American Express": "Both (Co-brand cards, Amex Membership Rewards transfer partner)",
            "SkyTeam Alliance": "Both (Earn and redeem miles across 20 partner airlines)",
            "Starbucks": "Both (Earn 1 mile per $1 spent at Starbucks, double Stars on travel days)",
            "Lyft": "Earn (Earn 1-2 miles per $1 spent on rides)",
            "Hertz": "Earn (Earn miles on rental cars; Elite members get reciprocal Hertz status)",
            "Instacart": "Earn (Earn 1-1.5 miles per $1 spent on groceries)"
        }, "high", "https://www.delta.com/us/en/skymiles/how-to-earn-miles/earn-with-partners"),
        "partnership_details": f([
            "Amex: Co-brand cards offer MQD boosts and free checked bags. Amex MR transfers instantly 1:1.",
            "SkyTeam: Elite Plus members get access to partner airport lounges worldwide on international tickets.",
            "Discontinued partnerships: Airbnb partnership discontinued in 2023."
        ], "high", "https://www.delta.com/us/en/skymiles/how-to-earn-miles/earn-with-partners"),
        "co_brand_card": f("Yes (Delta SkyMiles Gold, Platinum, and Reserve Cards issued by American Express)", "high", "https://www.delta.com/us/en/skymiles/airline-credit-cards/american-express-card"),

        # Category 6: Digital Experience
        "mobile_app_available": f("Both (iOS & Android) via Fly Delta app", "high", "https://www.delta.com/us/en/mobile/fly-delta-app"),
        "app_rating_ios": f(4.9, "high", "https://apps.apple.com/us/app/fly-delta/id388491656"),
        "app_rating_android": f(4.6, "high", "https://play.google.com/store/apps/details?id=com.delta.mobile.android"),
        "app_review_count": f("2.8 Million (App Store) + 220K (Google Play)", "medium", "https://apps.apple.com/us/app/fly-delta/id388491656"),
        "personalization_features": f(["Live bag tracking using RFID tags in app", "Interactive airport terminal maps", "Automatic rebooking and flight disruption assistant"], "high", "https://stories.delta.com/interactive-airport-maps-bag-tracking-make-travel-easier"),
        "gamification_features": f(["Status progress rings", "Annual qualification trackers", "Medallion milestone counters"], "medium", "https://www.delta.com/skymiles"),
        "digital_only_benefits": f(["In-app digital boarding pass", "Real-time baggage status notifications", "In-app ticket change waiver processing"], "high", "https://www.delta.com/us/en/mobile/fly-delta-app"),

        # Category 7: Member Sentiment
        "overall_sentiment": f("Negative", "medium", "https://www.reddit.com/r/delta/"),  # Devalued/backlash on status requirements
        "common_praise": f([
            "Operational reliability and aircraft cleanliness exceed other US legacy carriers",
            "Free high-speed Wi-Fi on domestic flights (for SkyMiles members) is a massive quality-of-life improvement",
            "Excellent Fly Delta app makes tracking luggage and checking in stress-free"
        ], "medium", "https://www.reddit.com/r/delta/"),
        "common_complaints": f([
            "Severe devaluation of SkyMiles, frequently referred to in forums as 'SkyPesos' due to high redemption costs",
            "Massive backlash in late 2023 regarding the 2024 Medallion qualification updates, which restricted lounge access and made status spend-only",
            "Crowded Sky Clubs leading to long lines outside lounges at major hubs like Atlanta and JFK"
        ], "medium", "https://www.reddit.com/r/delta/"),
        "sentiment_sources_checked": f([
            "https://www.reddit.com/r/delta/",
            "https://www.flyertalk.com/forum/delta-air-lines-skymiles/",
            "https://apps.apple.com/us/app/fly-delta/id388491656"
        ], "high", "https://www.delta.com"),
        "nps_score": f(41, "low", "https://customer.guru/nps/delta-air-lines"),

        # Category 8: Competitive Position
        "key_differentiators": f([
            "Free domestic Wi-Fi creates immediate digital customer signups at 30,000 feet",
            "SkyMiles do not expire, reducing customer anxiety about unused points",
            "Industry-leading co-branded credit card spend volume ($60B+), contributing a major recurring revenue stream from Amex (~$6B/yr)"
        ], "high", "https://stories.delta.com/delta-skymiles-program-evolution-focus-on-customers"),
        "known_weaknesses": f([
            "High award pricing devalues points value to as low as 1.0cpp on international business class tickets",
            "Elite status requirements are heavily skewed toward high spending, ignoring loyal, budget-conscious travelers",
            "Tight lounge access policies have angered cardholders and elites alike"
        ], "high", "https://www.delta.com/us/en/skymiles/medallion-program/how-to-qualify"),
        "closest_competitors": f(["United MileagePlus", "American Airlines AAdvantage", "Southwest Rapid Rewards", "JetBlue TrueBlue"], "high", "https://www.delta.com"),
        "recent_changes": f([
            "Implemented massive Medallion qualification rules change (Jan 2024): removed Medallion Qualifying Miles/Segments, making MQDs the sole metric, and significantly raised qualification thresholds",
            "Restricted Sky Club access for Amex Platinum and Delta Reserve cardholders (effective Feb 2025)",
            "Launched free high-speed Wi-Fi network-wide for SkyMiles members (Feb 2023)"
        ], "high", "https://stories.delta.com/delta-announces-modifications-to-2024-skymiles-program-updates-increases-investment-in-customer-experience")
    }
}
