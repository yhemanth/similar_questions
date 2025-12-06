import argparse
import os
import sys
from dotenv import load_dotenv
from typing import List

try:
    from openai import OpenAI
except ImportError:
    print(
        "Error: The 'openai' package is required. Install with: pip install openai",
        file=sys.stderr,
    )
    sys.exit(1)


def read_topics(path: str) -> List[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            # Keep original text per line, but drop empty/whitespace-only lines
            return [line.rstrip("\n") for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        sys.exit(2)


def build_messages(normalized_topics: List[str], input_topics: List[str]):
    n_inputs = len(input_topics)
    normalized_block = "\n".join(normalized_topics)
    inputs_block = "\n".join(input_topics)

    system_msg = (
        "You are a cautious topic normalizer. "
        "Your task is to map each input topic to the closest topic from the provided "
        "Normalized Topics list, or output 'Unknown' if no close match exists.\n\n"
        "Conservatism:\n"
        "- Only map when the match is clearly the same concept or a near-synonym.\n"
        "- If there is ambiguity or only a partial/broad relation, output 'Unknown'.\n\n"
        "Abbreviation/Acronym handling:\n"
        "- If the abbreviation is naturally mapping to a topic name, use that as the mapping.\n"
        "- Otherwise, output 'Unknown'.\n\n"
        "Multiple-topics in a single input line:\n"
        "- If an input line mentions multiple topics, choose the single best-matching normalized topic among them.\n"
        "- Do not output multiple topics. If no clear dominant match, output 'Unknown'.\n\n"
        "Output format requirements:\n"
        f"- Output exactly {n_inputs} lines.\n"
        "- Each line must be: <input topic>|<normalized topic or Unknown>\n"
        "- Use exactly one pipe '|' as the separator with no surrounding spaces.\n"
        "- No header, no bullets, no code fences, no explanations, no extra text.\n"
        "- Preserve the input order.\n"
        "- The normalized topic must be chosen exactly from the given list (copy text exactly; no new topics).\n"
        "- Do not add quotes."
    )

    user_msg = (
        "Normalized Topics:\n"
        f"{normalized_block}\n\n"
        "Input Topics:\n"
        f"{inputs_block}\n\n"
        "Now produce the mapping as specified."
    )

    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]


def call_openai(messages, model: str) -> str:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(3)

    client = OpenAI()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=messages
        )
        content = resp.choices[0].message.content
        if content is None:
            raise RuntimeError("Empty response content from model.")
        return content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        sys.exit(4)


def main():
    parser = argparse.ArgumentParser(
        description="Map input topics to closest normalized topics using OpenAI ChatGPT."
    )
    parser.add_argument("input_topics_file", help="Path to file with input topics (one per line).")
    parser.add_argument(
        "normalized_topics_file",
        help="Path to file with normalized topics (one per line).",
    )
    parser.add_argument(
        "--model",
        default="gpt-5.1",
        help="OpenAI model to use (default: gpt-4o).",
    )
    args = parser.parse_args()

    input_topics = read_topics(args.input_topics_file)
    normalized_topics = read_topics(args.normalized_topics_file)

    if not input_topics:
        print("Error: Input topics file is empty.", file=sys.stderr)
        sys.exit(5)
    if not normalized_topics:
        print("Error: Normalized topics file is empty.", file=sys.stderr)
        sys.exit(6)

    messages = build_messages(normalized_topics, input_topics)
    output_csv = call_openai(messages, args.model)

    print(output_csv)


if __name__ == "__main__":
    main()