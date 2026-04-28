"""CLI tool for Atlas Sanctum OS."""

import asyncio
import sys
import httpx
from typing import Optional
import click


class ASOS_CLI:
    """Command-line interface for Atlas Sanctum OS."""

    def __init__(self, api_url: str = "http://localhost:8000"):
        """Initialize CLI."""
        self.api_url = api_url
        self.client = httpx.AsyncClient(timeout=10.0)

    async def submit_intent(self, intent: str, metadata: dict = None) -> dict:
        """
        Submit an intent to the system.
        
        Args:
            intent: The user's natural language intent
            metadata: Optional metadata
            
        Returns:
            Response from API
        """
        try:
            response = await self.client.post(
                f"{self.api_url}/intent",
                json={
                    "intent": intent,
                    "metadata": metadata or {}
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return {
                "error": "Could not connect to API",
                "hint": "Make sure the gateway is running: docker-compose up"
            }
        except Exception as e:
            return {"error": str(e)}

    async def get_action(self, action_id: int) -> dict:
        """Get the status of an action."""
        try:
            response = await self.client.get(f"{self.api_url}/actions/{action_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    async def list_actions(self, limit: int = 10) -> dict:
        """List recent actions."""
        try:
            response = await self.client.get(
                f"{self.api_url}/actions",
                params={"limit": limit}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_agents(self) -> dict:
        """List available agents."""
        try:
            response = await self.client.get(f"{self.api_url}/agents")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


# Global CLI instance
_cli: Optional[ASos_CLI] = None


def get_cli(api_url: Optional[str] = None) -> ASOS_CLI:
    """Get or create CLI instance."""
    global _cli
    if _cli is None:
        _cli = ASOS_CLI(api_url or "http://localhost:8000")
    return _cli


@click.group()
@click.option("--api-url", default="http://localhost:8000", help="API gateway URL")
@click.pass_context
def cli(ctx, api_url):
    """Atlas Sanctum OS - AI Agent Orchestration System."""
    ctx.ensure_object(dict)
    ctx.obj["api_url"] = api_url


@cli.command()
@click.argument("intent")
@click.pass_context
def intent(ctx, intent):
    """Submit an intent to the system."""
    api_url = ctx.obj.get("api_url", "http://localhost:8000")
    cli_instance = ASOS_CLI(api_url)
    
    result = asyncio.run(cli_instance.submit_intent(intent))
    
    if "error" in result:
        click.secho(f"✗ Error: {result['error']}", fg="red")
        if "hint" in result:
            click.secho(f"  {result['hint']}", fg="yellow")
    else:
        click.secho(f"✓ Intent accepted", fg="green")
        click.echo(f"  Action ID: {result['action_id']}")
        click.echo(f"  Status: {result['status']}")
        click.echo(f"  Agent: {result['agent_type']}")
        click.echo(f"\nUse: asos status {result['action_id']} to check progress")


@cli.command()
@click.argument("action_id", type=int)
@click.pass_context
def status(ctx, action_id):
    """Check the status of an action."""
    api_url = ctx.obj.get("api_url", "http://localhost:8000")
    cli_instance = ASOS_CLI(api_url)
    
    result = asyncio.run(cli_instance.get_action(action_id))
    
    if "error" in result:
        click.secho(f"✗ Error: {result['error']}", fg="red")
    else:
        click.echo(f"Action ID: {result['id']}")
        click.echo(f"Intent: {result['intent']}")
        click.echo(f"Agent: {result['agent_type']}")
        click.secho(f"Status: {result['status']}", fg="blue")
        click.echo(f"Created: {result['created_at']}")
        if result['executed_at']:
            click.echo(f"Executed: {result['executed_at']}")
        if result['result']:
            click.echo(f"Result: {result['result']}")
        if result['blockchain_tx_hash']:
            click.secho(f"Blockchain TX: {result['blockchain_tx_hash']}", fg="cyan")


@cli.command()
@click.option("--limit", default=10, help="Number of actions to list")
@click.pass_context
def history(ctx, limit):
    """List recent actions."""
    api_url = ctx.obj.get("api_url", "http://localhost:8000")
    cli_instance = ASOS_CLI(api_url)
    
    result = asyncio.run(cli_instance.list_actions(limit))
    
    if "error" in result:
        click.secho(f"✗ Error: {result['error']}", fg="red")
    else:
        click.echo(f"\n{'ID':<6} {'Status':<12} {'Agent':<10} {'Intent':<40}")
        click.echo("-" * 70)
        for action in result['actions']:
            click.echo(
                f"{action['id']:<6} {action['status']:<12} {action['agent_type']:<10} {action['intent']:<40}"
            )


@cli.command()
@click.pass_context
def agents(ctx):
    """List available agents."""
    api_url = ctx.obj.get("api_url", "http://localhost:8000")
    cli_instance = ASOS_CLI(api_url)
    
    result = asyncio.run(cli_instance.get_agents())
    
    if "error" in result:
        click.secho(f"✗ Error: {result['error']}", fg="red")
    else:
        click.echo("\nAvailable Agents:")
        for agent_id, agent_type in result['agents'].items():
            click.echo(f"  • {agent_id.capitalize()} ({agent_type})")


if __name__ == "__main__":
    cli(obj={})
