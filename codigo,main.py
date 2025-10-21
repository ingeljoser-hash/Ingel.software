import typer
import uuid
from rich.console import Console
from rich.table import Table
from typing import Literal
from rich import print
from connection.connect_database import connect_database
from helpers.status_colors import status_colored


conn = connect_database("./src/database/todo.db")

app = typer.Typer()
table = Table("UUID", "Name", "Description", "Status", show_lines=True)
console = Console()

STATUS = Literal["COMPLETED", "PENDING", "IN_PROGRESS"]

@app.command(short_help="Create on task")
def create(name: str, description: str, status: STATUS):
  if conn:
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO TASKS(uuid, name, description, status) VALUES(?, ?, ?, ?)",
        (str(uuid.uuid4()), name, description, status, )
    )
    conn.commit()
    conn.close()
    print("One task have been [bold green]created[/bold green]")

@app.command(short_help="List all tasks")
def list():
  if conn:
    cursor = conn.cursor()
    results = cursor.execute(
        "SELECT uuid, name, description, status FROM tasks"
    )
    for uuid, name, description, status in results.fetchall():
      status_with_color = status_colored(status)
      table.add_row(uuid, name, description, status_with_color)
    conn.close()

  table.caption = "List all tasks"
  console.print(table)

@app.command(short_help="Update one task")
def update(
    uuid: str = typer.Argument(..., help="The UUID of the task to update."),
    name: str = typer.Option(None, help="New name for the task."),
    description: str = typer.Option(None, help="New description for the task."),
    status: STATUS = typer.Option(None, help="New status for the task (COMPLETED, PENDING, IN_PROGRESS).")
):
   
    if not (name or description or status):
        print("[bold yellow]Warning:[/bold yellow] You must provide at least one option to update (--name, --description, or --status).")
        return

    
    local_conn = connect_database("./src/database/todo.db") 
    if local_conn:
        cursor = local_conn.cursor()
        
    
        fields = []
        values = []

        if name:
            fields.append("name = ?")
            values.append(name)
        if description:
            fields.append("description = ?")
            values.append(description)
        if status:
            fields.append("status = ?")
            values.append(status)
        
       
        values.append(uuid) 

        sql = f"UPDATE TASKS SET {', '.join(fields)} WHERE uuid = ?"
        
       
        cursor.execute(sql, tuple(values))
        
        if cursor.rowcount > 0:
            local_conn.commit()
            print(f"Task with UUID [bold yellow]{uuid}[/bold yellow] has been [bold green]updated[/bold green].")
        else:
            
             print(f"Error: No task found with UUID [bold red]{uuid}[/bold red] or no changes were made.")
        
        local_conn.close()
           
@app.command(short_help="Delete one task")
def delete(uuid: str = typer.Argument(..., help="The UUID of the task to delete.")):
    local_conn = connect_database("./src/database/todo.db") 
    if local_conn:
        cursor = local_conn.cursor()
        cursor.execute(
            "DELETE FROM TASKS WHERE uuid = ?",
            (uuid,)
        )
        
        if cursor.rowcount > 0:
            local_conn.commit()
            print(f"Task with UUID [bold yellow]{uuid}[/bold yellow] has been [bold green]deleted[/bold green].")
        else:
            print(f"Error: No task found with UUID [bold red]{uuid}[/bold red].")
            
        local_conn.close()



if __name__ == "__main__":
  app()
