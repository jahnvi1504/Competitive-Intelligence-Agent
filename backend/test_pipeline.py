import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pipeline import (
    get_company_fingerprint,
    validate_source_against_fingerprint,
    determine_source_tier,
    calculate_field_confidence
)

def test_fingerprint_validation():
    print("Testing Fingerprint Validation...")
    fingerprint = get_company_fingerprint("Starbucks Rewards")
    
    # 1. Official site should match 4/4 or 3/4
    is_ok, weight, reason = validate_source_against_fingerprint("https://www.starbucks.com/rewards/faq", fingerprint)
    assert is_ok == True
    assert weight == 3.0
    print(f"  Official page test passed: weight={weight}, reason='{reason}'")
    
    # 2. Third party news with brand in URL should match 3/4
    is_ok, weight, reason = validate_source_against_fingerprint("https://www.reuters.com/business/starbucks-points-devaluation-2023", fingerprint)
    assert is_ok == True
    assert weight == 3.0
    print(f"  Third-party news test passed: weight={weight}, reason='{reason}'")
    
    # 3. Low tier mismatch (different country or domain check)
    is_ok, weight, reason = validate_source_against_fingerprint("https://www.rewardplus.com/sg/starbucks-program", fingerprint)
    assert is_ok == True
    assert weight == 0.7
    print(f"  Low-tier match test passed: weight={weight}, reason='{reason}'")
    
    # 4. Total mismatch should fail
    is_ok, weight, reason = validate_source_against_fingerprint("https://www.example-hotel-rewards.com/rooms", fingerprint)
    assert is_ok == False
    assert weight == 0.0
    print(f"  Mismatch rejection test passed: is_ok={is_ok}, reason='{reason}'")

def test_source_tier_mapping():
    print("\nTesting Source Tier Mapping...")
    t1, w1 = determine_source_tier("https://www.starbucks.com/rewards/faq")
    assert t1 == "official"
    assert w1 == 3.0
    
    t2, w2 = determine_source_tier("https://www.businesswire.com/news/12345")
    assert t2 == "press_release"
    assert w2 == 2.0
    
    t3, w3 = determine_source_tier("https://www.reddit.com/r/starbucks")
    assert t3 == "forum"
    assert w3 == 0.5
    
    print("  Tier weights mapping test passed successfully!")

def test_confidence_scoring():
    print("\nTesting Confidence Scorer...")
    
    # High confidence test (official + press_release)
    extractions_high = [
        {"value": "1 Star per $1", "source_url": "https://www.starbucks.com/rewards"},
        {"value": "1 Star per $1", "source_url": "https://www.businesswire.com/news/123"}
    ]
    conf_high, score_high = calculate_field_confidence(extractions_high)
    assert conf_high == "high"
    print(f"  High confidence test passed: conf={conf_high}, score={score_high}")
    
    # Medium confidence test (press release + forum)
    extractions_med = [
        {"value": "2 Stars per $1", "source_url": "https://www.businesswire.com/news/123"},
        {"value": "2 Stars per $1", "source_url": "https://reddit.com/r/starbucks"}
    ]
    conf_med, score_med = calculate_field_confidence(extractions_med)
    assert conf_med == "medium"
    print(f"  Medium confidence test passed: conf={conf_med}, score={score_med}")
    
    # Low confidence test (forum only)
    extractions_low = [
        {"value": "3 Stars per $1", "source_url": "https://reddit.com/r/starbucks"}
    ]
    conf_low, score_low = calculate_field_confidence(extractions_low)
    assert conf_low == "low"
    print(f"  Low confidence test passed: conf={conf_low}, score={score_low}")

if __name__ == "__main__":
    print("--- PIPELINE LOGICAL VERIFICATION ---")
    test_fingerprint_validation()
    test_source_tier_mapping()
    test_confidence_scoring()
    print("--------------------------------------")
    print("ALL TESTS PASSED SUCCESSFULLY!")
