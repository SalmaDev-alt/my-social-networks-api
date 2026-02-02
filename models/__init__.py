"""
Modèles de données pour My Social Networks API

Note: Ces modèles servent de documentation pour la structure des collections MongoDB.
La validation réelle est effectuée par les validators avec Marshmallow.
"""

from .user import UserModel
from .event import EventModel
from .group import GroupModel
from .discussion import DiscussionModel
from .message import MessageModel
from .album import AlbumModel
from .photo import PhotoModel
from .poll import PollModel
from .ticket import TicketModel, TicketTypeModel
from .shopping_item import ShoppingItemModel
from .carpooling import CarpoolingModel

__all__ = [
    'UserModel',
    'EventModel',
    'GroupModel',
    'DiscussionModel',
    'MessageModel',
    'AlbumModel',
    'PhotoModel',
    'PollModel',
    'TicketModel',
    'TicketTypeModel',
    'ShoppingItemModel',
    'CarpoolingModel'
]