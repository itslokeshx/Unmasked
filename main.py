import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

from chain import build_chain

console = Console()


def show_banner():
    title = Text("U N M A S K E D", style="bold white", justify="center")
    tagline = Text("Know the character. Unmask their mind.", style="dim white", justify="center")
    content = Text.assemble(title, "\n", tagline)
    console.print(Panel(content, border_style="white", padding=(1, 6)))
    console.print()


def main():
    show_banner()

    character = Prompt.ask("[bold white]Who do you want to unmask[/bold white]")

    if not character.strip():
        console.print("  No character entered.", style="red")
        sys.exit(0)

    console.print()

    with console.status(
        f"  Loading knowledge for [bold white]{character}[/bold white]...",
        spinner="dots"
    ):
        chain, session_id, ingested = build_chain(character)

    if ingested:
        console.print(
            f"  Scraped and indexed Wikipedia for [bold white]{character}[/bold white].",
            style="dim green"
        )
    else:
        console.print(
            f"  Loaded [bold white]{character}[/bold white] from cache.",
            style="dim green"
        )

    console.print("  Type [bold white]quit[/bold white] to end the session.\n", style="dim white")

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n  Session ended.\n", style="dim white")
            break

        if not user_input.strip():
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            console.print("\n  Session ended.\n", style="dim white")
            break

        with console.status("", spinner="dots"):
            response = chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )

        console.print(f"\n[dim]UNMASKED[/dim]  [white]{response['answer']}[/white]\n")


if __name__ == "__main__":
    main()
