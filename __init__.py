# -*- coding: utf-8 -*-
"""
/***************************************************************************
showAttributeTable 
Abre o Formulário de Atributos da camada ativa
                             -------------------
        released             : 2025-01-10 
        author               : (C) 2025 by Andrés de M. Leite 
        email                : leite.m.andres@gmail.com 
        made in              : easyPlugin by Pavel Pereverzev
        credits to           : Gary Sherman and Alexandre Neto
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
from __future__ import absolute_import

def classFactory(iface):
    # load showAttributeTable class from file showAttributeTable -- load classname (plugin name)
    from .showAttributeTable import showAttributeTable # -- from filename import classname
    return showAttributeTable(iface) # -- import classname 
