"""Contains several models to inherit from"""

from abc import ABCMeta, abstractmethod, abstractproperty


class FormatterMeta(metaclass=ABCMeta):
    """A framework for each game pack's formatter class"""
    
    def make_header(self, header_text):
        """Bold the text for game pack title"""
        return f"**{header_text}**"
    
    def make_section_header(self, section_header_text):
        """Bracket the text for game pack section title"""
        return f"[{section_header_text}]"
    
    def format_role_name(self, role_name_text):
        """Mini code block around the names of roles"""
        return f"`{role_name_text}`"
    
    @abstractmethod
    def create_complete_roles_list(self):
        """Create the list of roles from the game pack when the !roles command is used without argument.
        To be implemented in child class.
        """
        pass


class GameMeta(metaclass=ABCMeta):
    """A framework for how game classes should be designed.
    All game packs for this bot must inherit from this class, and implement these methods.
    """

    @abstractmethod
    def register_players(self, id_list):
        """Register the players"""
        pass

    @abstractmethod
    def start_game(self):
        """Start the game"""
        pass

    @abstractmethod
    def end_game(self):
        """End the game, compute winners etc."""
        pass

    