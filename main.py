import sys
import time
import random

from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.align import Align

from chain import build_chain

console = Console()

ACCENT = "#b967ff"       # violet — character mode
DIM = "grey50"
WHITE = "bold white"

BANNER = r"""
██╗   ██╗███╗   ██╗███╗   ███╗ █████╗ ███████╗██╗  ██╗███████╗██████╗
██║   ██║████╗  ██║████╗ ████║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║██╔████╔██║███████║███████╗█████╔╝ █████╗  ██║  ██║
██║   ██║██║╚██╗██║██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ ██╔══╝  ██║  ██║
╚██████╔╝██║ ╚████║██║ ╚═╝ ██║██║  ██║███████║██║  ██╗███████╗██████╔╝
 ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═════╝
"""

THINKING_LINES = [
    "peeling back the mask",
    "cross-referencing the source",
    "reading between the lines",
    "tracing the pattern",
    "digging past the surface",
]

HELP_TEXT = """
  [bold white]commands[/bold white]

    [dim]q, quit, exit[/dim]     end the session
    [dim]new[/dim]               unmask a different character
    [dim]help[/dim]              show this menu
"""


def header():
    console.print()
    console.print(Align.center(Text(BANNER.rstrip("\n"), style=ACCENT)))
    console.print(Align.center(Text("Know the character. Unmask their mind.", style=DIM)))
    console.print()
    console.rule(style="grey23")
    console.print()


def typewriter(text: str, style: str = "white", delay: float = 0.006):
    """Stream text out word by word for a live-typed feel."""
    words = text.split(" ")
    line = "  "
    for i, word in enumerate(words):
        line += word + " "
        sys.stdout.write("\r" + " " * console.width)
        sys.stdout.write("\r")
        console.print(line, style=style, end="\r")
        time.sleep(delay)
    console.print(line, style=style)


def load_character():
    console.print("  [dim]Enter a character name to begin.[/dim]")
    console.print("  [dim]Try: Batman  ·  Walter White  ·  Johan Liebert[/dim]")
    console.print()

    try:
        character = console.input(f"  [{WHITE}]character[/{WHITE}]  [{ACCENT}]›[/{ACCENT}]  ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print()
        sys.exit(0)

    if not character:
        console.print()
        console.print("  [dim red]No character entered.[/dim red]")
        console.print()
        sys.exit(0)

    console.print()

    with console.status(f"  [dim]unmasking {character}...[/dim]", spinner="dots", spinner_style=ACCENT):
        try:
            chain, session_id, ingested = build_chain(character)
        except RuntimeError as e:
            console.print(f"  [red]{e}[/red]")
            console.print()
            sys.exit(1)

    label = "freshly indexed" if ingested else "loaded from cache"
    console.print(f"  [{ACCENT}]●[/{ACCENT}]  [bold white]{character}[/bold white]  [dim]· {label}[/dim]")
    console.print()
    console.print(
        f"  [dim]Ask anything.[/dim]  [bold white]help[/bold white] [dim]for commands ·[/dim]  "
        f"[bold white]q[/bold white] [dim]to quit.[/dim]"
    )
    console.print()
    console.rule(style="grey23")

    return character, chain, session_id


def main():
    header()
    character, chain, session_id = load_character()

    while True:
        console.print()

        try:
            user_input = console.input(f"  [{WHITE}]›[/{WHITE}]  ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print()
            console.print("  [dim]Session ended.[/dim]")
            console.print()
            break

        if not user_input:
            continue

        lowered = user_input.lower()

        if lowered in ("quit", "exit", "q"):
            console.print()
            console.print("  [dim]Session ended.[/dim]")
            console.print()
            break

        if lowered == "help":
            console.print(HELP_TEXT)
            console.rule(style="grey23")
            continue

        if lowered == "new":
            console.print()
            console.rule(style="grey23")
            character, chain, session_id = load_character()
            continue

        console.print()

        try:
            phrase = random.choice(THINKING_LINES)
            with console.status(f"  [dim]{phrase}...[/dim]", spinner="dots", spinner_style=ACCENT):
                response = chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": session_id}}
                )
        except KeyboardInterrupt:
            console.print()
            console.print("  [dim]Interrupted.[/dim]")
            console.print()
            console.rule(style="grey23")
            continue
        except Exception as e:
            console.print(f"  [red]Something went wrong: {e}[/red]")
            console.print()
            console.rule(style="grey23")
            continue

        console.print(f"  [{ACCENT}]◆ UNMASKED[/{ACCENT}]")
        console.print()
        console.print(Markdown(response["answer"]))
        console.print()
        console.rule(style="grey23")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print()
        console.print("  [dim]Session ended.[/dim]")
        console.print()