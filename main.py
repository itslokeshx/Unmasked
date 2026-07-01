import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

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

    character = Prompt.ask("  [dim]character[/dim]")

    if not character.strip():
        console.print()
        console.print("  [dim red]No character entered.[/dim red]")
        console.print()
        sys.exit(0)

    console.print()

    with console.status("  [dim]Loading...[/dim]", spinner="dots"):
        try:
            chain, session_id, ingested = build_chain(character)
        except RuntimeError as e:
            console.print(f"  [red]{e}[/red]")
            console.print()
            sys.exit(1)

    label = "indexed" if ingested else "cache"
    console.print(f"  [dim green]✓[/dim green]  [dim]{character} · {label}[/dim]")
    console.print(f"  [dim]Type q to exit.[/dim]")
    console.print()
    console.rule(style="dim")

    while True:
        console.print()

        try:
            user_input = Prompt.ask("  [bold white]>[/bold white]")
        except (KeyboardInterrupt, EOFError):
            console.print()
            console.print("  [dim]Session ended.[/dim]")
            console.print()
            break

        if not user_input.strip():
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            console.print()
            console.print("  [dim]Session ended.[/dim]")
            console.print()
            break

        console.print()

        with console.status("  [dim]UNMASKED is thinking...[/dim]", spinner="dots"):
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
