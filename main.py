import sys
import warnings
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from rich.console import Console
from rich.markdown import Markdown

from chain import build_chain

console = Console()


def header():
    console.print()
    console.print("  UNMASKED", style="bold white")
    console.print("  Know the character. Unmask their mind.", style="dim")
    console.print()
    console.rule(style="dim")
    console.print()


def main():
    header()

    console.print("  [dim]Enter a character name to begin.[/dim]")
    console.print("  [dim]Try: Batman  ·  Walter White  ·  Johan Liebert[/dim]")
    console.print()

    try:
        character = console.input("  [bold white]character[/bold white]  ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print()
        sys.exit(0)

    if not character:
        console.print()
        console.print("  [dim red]No character entered.[/dim red]")
        console.print()
        sys.exit(0)

    console.print()

    with console.status(
        f"  [dim]Loading knowledge for {character}...[/dim]",
        spinner="dots"
    ):
        try:
            chain, session_id, ingested = build_chain(character)
        except RuntimeError as e:
            console.print(f"  [red]{e}[/red]")
            console.print()
            sys.exit(1)

    label = "indexed" if ingested else "cache"
    console.print(f"  [dim green]✓[/dim green]  [dim]{character} · {label}[/dim]")
    console.print()
    console.print(
        "  [dim]Ask anything about the character.[/dim]  "
        "[bold white]q[/bold white] [dim]to quit.[/dim]"
    )
    console.print()
    console.rule(style="dim")

    while True:
        console.print()

        try:
            user_input = console.input("  [bold white]>[/bold white]  ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print()
            console.print("  [dim]Session ended.[/dim]")
            console.print()
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            console.print()
            console.print("  [dim]Session ended.[/dim]")
            console.print()
            break

        console.print()

        with console.status("  [dim]thinking...[/dim]", spinner="dots"):
            response = chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )

        console.print("  [dim]UNMASKED[/dim]")
        console.print()
        console.print(Markdown("  " + response["answer"]))
        console.print()
        console.rule(style="dim")


if __name__ == "__main__":
    main()
