"""Main application entry point for the document RAG system."""
import argparse
import sys
from pathlib import Path

from src.config import Config
from src.utils import get_logger
from src.rag import (
    build_index,
    query_documents,
    interactive_mode,
)

logger = get_logger(__name__)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Production-grade document RAG system using Docling and LangChain"
    )

    parser.add_argument(
        "command",
        choices=["build", "query", "interactive"],
        help="Command to execute: build (create index), query (ask question), interactive (chat mode)"
    )

    parser.add_argument(
        "-q", "--question",
        type=str,
        help="Question to ask (required for 'query' command)"
    )

    parser.add_argument(
        "-d", "--data-dir",
        type=Path,
        help="Directory containing documents (default: ./data)"
    )

    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild of the index"
    )

    parser.add_argument(
        "--no-sources",
        action="store_true",
        help="Don't show source documents in output"
    )

    args = parser.parse_args()

    try:
        # Validate configuration
        Config.validate()

        if args.command == "build":
            if not args.data_dir:
                parser.error("--data-dir is required for 'build' command")
                
            build_index(data_dir=args.data_dir, force_rebuild=args.rebuild)

        elif args.command == "query":
            if not args.question:
                parser.error("--question is required for 'query' command")

            result = query_documents(args.question, load_existing=not args.rebuild)

            print("\n" + "=" * 80)
            print(f"Question: {result['question']}")
            print("=" * 80)
            print(f"Answer: {result['answer']}")
            print("=" * 80)

            if not args.no_sources and "sources" in result:
                print(f"\nSources ({result['num_sources']} documents):")
                for source in result["sources"]:
                    print(f"\n[{source['number']}] {source['metadata'].get('source_file', 'Unknown')}")
                    print(f"    {source['content'][:200]}...")

        elif args.command == "interactive":
            interactive_mode()

    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
