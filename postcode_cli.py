"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import get_postcode_completions, validate_postcode


def main():
    parser = ArgumentParser(description="Postcode utility tool.")
    parser.add_argument("--mode", "-m", required=True, choices=["validate", "complete"],
                        help="Select 'validate' or 'complete' mode.")
    parser.add_argument("postcode", type=str,
                        help="Postcode or partial postcode string.")
    args = parser.parse_args()
    postcode = args.postcode.strip().upper()
    if args.mode == "validate":
        try:
            results = validate_postcode(postcode)
            if results:
                print(f"{postcode} is a valid postcode.")
            else:
                print(f"{postcode} is not a valid postcode.")
        except Exception:
            print(1)
            print(f"{postcode} is not a valid postcode.")
    elif args.mode == "complete":
        try:
            completions = get_postcode_completions(postcode)
            if completions:
                for postcode in completions[:5]:
                    print(postcode)
            else:
                print(f"No matches for {postcode}.")
        except Exception:
            print(f"No matches for {postcode}.")


if __name__ == "__main__":
    main()
