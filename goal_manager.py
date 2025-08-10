import json
import os
from typing import List, Dict, Optional
import uuid


class GoalManager:
    """Manages personal goals with local JSON persistence."""
    
    def __init__(self, goals_file: str = "goals.json"):
        """Initialize the GoalManager with a specified goals file.
        
        Args:
            goals_file (str): Path to the JSON file for storing goals
        """
        self.goals_file = goals_file
        self.goals = self._load_goals()
    
    def _load_goals(self) -> List[Dict[str, str]]:
        """Load goals from the JSON file.
        
        Returns:
            List of goal dictionaries
        """
        try:
            if os.path.exists(self.goals_file):
                with open(self.goals_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load goals from {self.goals_file}: {e}")
            return []
    
    def _save_goals(self) -> bool:
        """Save goals to the JSON file.
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            with open(self.goals_file, 'w', encoding='utf-8') as f:
                json.dump(self.goals, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error: Could not save goals to {self.goals_file}: {e}")
            return False
    
    def add_goal(self, description: str) -> str:
        """Add a new goal.
        
        Args:
            description (str): The goal description
            
        Returns:
            str: The unique ID of the created goal
        """
        if not description or not description.strip():
            raise ValueError("Goal description cannot be empty")
        
        goal_id = str(uuid.uuid4())[:8]  # Short UUID for easier reference
        goal = {
            'id': goal_id,
            'description': description.strip()
        }
        
        self.goals.append(goal)
        if self._save_goals():
            return goal_id
        else:
            # Rollback if save failed
            self.goals.pop()
            raise IOError("Failed to save goal to file")
    
    def list_goals(self) -> List[Dict[str, str]]:
        """Get all current goals.
        
        Returns:
            List of goal dictionaries with 'id' and 'description' keys
        """
        return self.goals.copy()
    
    def remove_goal(self, identifier: str) -> bool:
        """Remove a goal by its ID or description.
        
        Args:
            identifier (str): Goal ID or description to remove
            
        Returns:
            bool: True if goal was found and removed, False otherwise
        """
        if not identifier or not identifier.strip():
            raise ValueError("Goal identifier cannot be empty")
        
        identifier = identifier.strip()
        
        # Try to find by ID first, then by description
        for i, goal in enumerate(self.goals):
            if goal['id'] == identifier or goal['description'] == identifier:
                removed_goal = self.goals.pop(i)
                if self._save_goals():
                    return True
                else:
                    # Rollback if save failed
                    self.goals.insert(i, removed_goal)
                    raise IOError("Failed to save changes to file")
        
        return False
    
    def get_goal_by_id(self, goal_id: str) -> Optional[Dict[str, str]]:
        """Get a specific goal by its ID.
        
        Args:
            goal_id (str): The goal ID to search for
            
        Returns:
            Dict with goal data or None if not found
        """
        for goal in self.goals:
            if goal['id'] == goal_id:
                return goal.copy()
        return None