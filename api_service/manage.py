# encoding: utf-8

import click
from flask.cli import with_appcontext


@click.group()
def cli():
    """Main entry point"""
    pass


@cli.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from api_service.extensions import db
    from api_service.models import User, StockEntry, RequestHistory, StockStat
    
    db.create_all()
    click.echo("Created database tables")

    if not User.query.filter_by(username="admin").first():
        user = User(username="admin", email="admin@mail.com", password="admin", active=True, role='ADMIN')
        db.session.add(user)
        click.echo("created admin user")

    if not User.query.filter_by(username="johndoe").first():
        user = User(username="johndoe", email="johndoe@mail.com", password="john", active=True, role='USER')
        db.session.add(user)
        click.echo("created normal user")
    
    db.session.commit()
    click.echo("Finished initialization.")


if __name__ == "__main__":
    cli()
