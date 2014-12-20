from treebeard.ns_tree import NS_NodeManager
from eav.managers import BaseEntityManager
from django.db.models import Manager


class CottageManager(NS_NodeManager, BaseEntityManager):
    pass