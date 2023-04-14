from enum import Enum


class DocDbClustersEnum(str, Enum):
    """Enum for DocDb Clusters"""
    # DocDb Clusters
    prodonpier = 'prodonpier'
    devonpier = 'devonpier'
    stageonpier = 'stageonpier'
    all = 'all'
    prodlvm = 'prodlvm'
    devlvm = 'devlvm'
    prodhdi = 'prodhdi'
    devhdi = 'devhdi'
    prodhuk = 'prodhuk'
    devhuk = 'devhuk'
    prodowd = 'prodowd'
    devowd = 'devowd'
    prodwgv = 'prodwgv'
    devwgv = 'devwgv'


class DocDbClusterActionsEnum(str, Enum):
    """Enum for DocDb Cluster Actions"""
    # DocDb Cluster Actions
    status = 'status'
    create = 'create'
    delete = 'delete'
    update = 'update'
