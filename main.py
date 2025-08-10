import click
from goal_manager import GoalManager

# Google Drive functionality (optional)
try:
    from pydrive2.drive import GoogleDrive
    from pydrive2.auth import GoogleAuth
    GOOGLE_DRIVE_AVAILABLE = True
    
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    
    # Check if credentials are not found or expired
    if gauth.credentials is None or gauth.access_token_expired:
        # Authenticate if credentials are not found or expired
        gauth.LocalWebserverAuth()
    else:
        # Initialize the saved credentials
        gauth.Authorize()
    
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    
    drive = GoogleDrive(gauth)
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    print("Note: Google Drive functionality not available (pydrive2 not installed)")
except Exception as e:
    GOOGLE_DRIVE_AVAILABLE = False
    print(f"Note: Google Drive functionality not available: {e}")


def list_files():
    if not GOOGLE_DRIVE_AVAILABLE:
        print("Error: Google Drive functionality not available. Please install pydrive2.")
        return
    try:
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print(f"title: {file1['title']}, id: {file1['id']}")
    except Exception as e:
        print("Error listing files:", str(e))


def print_tree(node, depth=0):
    indent = '  ' * depth
    print(f"{indent}- {node['title']} ({node['mimeType']})")

    for child in node['children']:
        print_tree(child, depth + 1)


def get_filesystem_tree(drive, folder_id='root', depth=0):
    try:
        files = drive.ListFile({'q': f"'{folder_id}' in parents"}).GetList()

        tree = []
        for file1 in files:
            node = {
                'title': file1['title'],
                'id': file1['id'],
                'mimeType': file1['mimeType'],
                'children': []
            }

            if file1['mimeType'] == 'application/vnd.google-apps.folder':
                node['children'] = get_filesystem_tree(drive, file1['id'], depth + 1)

            tree.append(node)

        return tree

    except Exception as e:
        print("Error getting filesystem tree:", str(e))
        return []


def file_upload():
    if not GOOGLE_DRIVE_AVAILABLE:
        print("Error: Google Drive functionality not available. Please install pydrive2.")
        return
    try:
        file1 = drive.CreateFile({'title': 'Hello.txt'})
        file1.Upload()
        print("File uploaded successfully. File ID:", file1['id'])
    except Exception as e:
        print("Error uploading file:", str(e))


# Goal management functions
def add_goal_func(description):
    """Add a new goal."""
    try:
        goal_manager = GoalManager()
        goal_id = goal_manager.add_goal(description)
        print(f"Goal added successfully with ID: {goal_id}")
        print(f"Description: {description}")
    except (ValueError, IOError) as e:
        print(f"Error adding goal: {e}")
    except Exception as e:
        print(f"Unexpected error adding goal: {e}")


def list_goals_func():
    """List all current goals."""
    try:
        goal_manager = GoalManager()
        goals = goal_manager.list_goals()
        
        if not goals:
            print("No goals found. Add your first goal with --add-goal 'Your goal description'")
            return
        
        print(f"Your Goals ({len(goals)} total):")
        print("-" * 50)
        for goal in goals:
            print(f"ID: {goal['id']}")
            print(f"Description: {goal['description']}")
            print("-" * 50)
    except Exception as e:
        print(f"Error listing goals: {e}")


def remove_goal_func(identifier):
    """Remove a goal by ID or description."""
    try:
        goal_manager = GoalManager()
        
        if goal_manager.remove_goal(identifier):
            print(f"Goal removed successfully: {identifier}")
        else:
            print(f"Goal not found: {identifier}")
            print("Use --list-goals to see available goals")
    except (ValueError, IOError) as e:
        print(f"Error removing goal: {e}")
    except Exception as e:
        print(f"Unexpected error removing goal: {e}")


@click.command()
@click.option('--list', is_flag=True, help='List files on Google Drive.')
@click.option('--tree', is_flag=True, help='Show filesystem tree on Google Drive.')
@click.option('--upload', is_flag=True, help='Upload a file to Google Drive.')
@click.option('--add-goal', type=str, help='Add a new personal goal.')
@click.option('--list-goals', is_flag=True, help='List all your personal goals.')
@click.option('--remove-goal', type=str, help='Remove a goal by ID or description.')
def main(list, tree, upload, add_goal, list_goals, remove_goal):
    try:
        # Goal management commands
        if add_goal:
            add_goal_func(add_goal)
        elif list_goals:
            list_goals_func()
        elif remove_goal:
            remove_goal_func(remove_goal)
        # Google Drive commands
        elif list:
            list_files()
        elif tree:
            if not GOOGLE_DRIVE_AVAILABLE:
                print("Error: Google Drive functionality not available. Please install pydrive2.")
            else:
                root_folder_tree = get_filesystem_tree(drive)
                for node in root_folder_tree:
                    print_tree(node)
        elif upload:
            file_upload()
        else:
            # Show help if no options provided
            ctx = click.get_current_context()
            click.echo(ctx.get_help())
    except Exception as e:
        print("Error in main function:", str(e))


if __name__ == '__main__':
    main()
