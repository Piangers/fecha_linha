# -*- coding: utf-8 -*-


import os
import math
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import *
from qgis.core import *
from qgis.PyQt.QtWidgets import *
from fecha_Linha import resources_rc

class fecha_Linha:
    

    def __init__(self, iface):
       
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'BGTImport_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        self.actions = []
        self.menu = self.tr(u'&Batch Vector Layer Saver')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'BatchVectorLayerSaver')
        self.toolbar.setObjectName(u'fecha_linha')

       
    def tr(self, message):
        
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('BatchVectorLayerSaver', message)
        
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
       
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/fecha_Linha/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'fecha_linha'),
            callback=self.fecha_Linha,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&fecha_Linha'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

            
    def fecha_Linha(self):
        if(self.testLayerAtivo()):
            if(self.testMetro() and self.testTipoGeometria() and self.testGeometriaSelecionada()):   
                layer = self.iface.activeLayer()

                for feat in layer.selectedFeatures():
                    geom = feat.geometry()
                    vertex_list = geom.asPolyline()
                    x1 = vertex_list[0][0]
                    y1 = vertex_list[0][1]
                    x2 = vertex_list[-1][0]
                    y2 = vertex_list[-1][1]
                    
                    distancia = (math.sqrt ((x1 - x2)**2 + (y1 - y2)**2))
                    
                    if(not distancia <= 50):
                        print ('Distância entre vertice final e inicial deve ser menor que a tolerância de 50 metros.') 
                    else:
                        indice_ultimo_vertice = len(vertex_list)-1
                        last_vertex = geom.vertexAt(indice_ultimo_vertice)
                        geom.moveVertex(x1,y1, indice_ultimo_vertice)
                        geom.insertVertex(last_vertex.x(),last_vertex.y(),indice_ultimo_vertice)
                        layer.changeGeometry(feat.id(),geom)
        
                      
    def testLayerAtivo(self):
        if(not self.iface.activeLayer()):
            print ('selecione a imagem')
            return False
        else:
            return True

    def testMetro(self): 
        if(not self.iface.activeLayer().crs().mapUnits()==6):
	        
                return False
        else:
            return True

    def testTipoGeometria(self):
        if(not self.iface.activeLayer().geometryType() == 1) :
            print ('A camada deve possuir geometrias do tipo linha.')
            return False
        elif(not self.iface.activeLayer().isEditable()):
            print ('A camada deve estar em modo de edição.')
            return False
        else:
            return True

    def testGeometriaSelecionada(self):
        if(not len(self.iface.activeLayer().selectedFeatures()) == 1):
            print ('Deve haver exatamente uma geometria linha selecionada.')
            return False
        else:
            return True    

    

