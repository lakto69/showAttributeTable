# -*- coding: utf-8 -*-
"""
/***************************************************************************
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
"""
# import system, PyQt and QGIS libraries
from __future__ import absolute_import
import os.path

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * # only used widgets can be listed here

from qgis.core import *
from qgis._gui import * 
from qgis.utils import iface

from .template_tools import *

class showAttributeTable(object): 
    # main plugin class
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'showAttributeTable_{}.qm'.format(locale)) 

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u"showAttributeTable")

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    
    def initGui(self):
        # Create the menu entries and toolbar icons inside the QGIS GUI 
        icon_path = QIcon(os.path.join(self.plugin_dir, "icon.png"))
        self.icon_action = self.add_action(
            icon_path,
            text=self.tr(u"showAttributeTable"),
            callback=self.run,
            checkable=False,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def warning_message(self, err_text):
        msg = QMessageBox()
        msg.warning(self, "Warning", err_text)
    
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        checkable=False,
        add_to_menu=False,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        action.setCheckable(checkable)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action
    

    def unload(self):
        # Removes the plugin menu item and icon from QGIS GUI
        for action in self.actions:
            self.iface.removeToolBarIcon(action)


    def tr(self, text):
        return QCoreApplication.translate("showAttributeTable", text)
    
    # custom actions, feel free to edit them
    def simple_action(self, msg):
        # # run a simple action like in python console of QGIS
        # self.iface.messageBar().pushMessage("Simple", "Action", level=Qgis.Info)

        # run a simple action like in python console of QGIS
        self.iface.messageBar().pushMessage("Error", msg, level=Qgis.Warning)

    def simple_gui(self):
        # run a widget with some actions
        self.app = SimpleGui()


    def simple_map_tool(self):
        # run a map tool, also making an action button checkable
        if self.icon_action.isChecked():
            self.rband_tool_anchor = PointTool(self.icon_action)        
            iface.mapCanvas().setMapTool(self.rband_tool_anchor)
        else:
            self.rband_tool_anchor.deactivate()
            iface.mapCanvas().unsetMapTool(self.rband_tool_anchor)
    

    def custom_tool(self):
        try:
            pass
        except Exception as e:
            print(e)
            self.warning_message("Error in script\nSee Python console for details")

    # MAIN ACTION FUNCTION IS HERE
    def run(self):
        # Obtém a camada ativa
        layer = iface.activeLayer()
                
        # Verifica se a camada é válida
        if layer is not None and layer.type() == QgsMapLayer.VectorLayer:
            if layer.featureCount() >0:
                # Abre o formulário de atributos
                iface.showAttributeTable(layer)
            else:
                msg = "Selected vector layer contains no features."
                print(msg)
                # run method that performs all the real work
                self.simple_action(msg)            
        else:
            msg = "No vector layer selected."
            print(msg)
            # run method that performs all the real work
            self.simple_action(msg)
    


    