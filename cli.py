import argparse
from core.scraper import scrape_reddit, scrape_indiehackers, scrape_x
from core.pitch_gen import generate_pitches
from core.db import init_db, save_prospects

def main():
    parser = argparse.ArgumentParser(description="SudohumanX Outreach Engine")
    parser.add_argument("--platform", choices=["reddit", "indiehackers", "X"], required=True)
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords")
    parser.add_argument("--batch", type=int, default=10, help="Number of prospects to fetch")
    parser.add_argument("--style", choices=["empire", "friendly", "technical"], default="empire")

    args = parser.parse_args()
    keywords = [k.strip() for k in args.keywords.split(",")]

    print(f"⚔️ Scanning {args.platform} for prospects...")

    if args.platform == "reddit":
        prospects = scrape_reddit(keywords, args.batch)
    elif args.platform == "indiehackers":
        prospects = scrape_indiehackers(keywords, args.batch)
    elif args.platform == "X":
        prospects = scrape_x(keywords, args.batch)

    print("✅ Found prospects. Generating pitches...")
    pitched_prospects = generate_pitches(prospects, style=args.style)

    save_prospects(pitched_prospects)
    print(f"🗡 Saved {len(pitched_prospects)} prospects to database.")

if __name__ == "__main__":
    init_db()
    main()
