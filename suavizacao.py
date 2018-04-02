# -*- coding: utf-8 -*-

import math
from qgis.core import QGis, QgsVectorLayer, QgsGeometry
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QIcon, QAction
from PyQt4.QtCore import *
import resources_rc
import os.path
from qgis.gui import QgsMessageBar


class Suavizacao:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
         
        # cria uma ação que iniciará a configuração do plugin 
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/Suavizacao/b.png'
        
        
        self.action = QAction (QIcon (icon_path),'Fechar linha', pai)
        self.action.setObjectName ('Fechar linha')
        self.action.setStatusTip('status_tip')
        self.action.setWhatsThis('whats_this')
        QObject.connect (self.action, SIGNAL ("triggered ()"), self.run)

        # Adicionar o botão da barra de ferramentas e item de menu 
        self.iface.addToolBarIcon (self.action) 
        self.iface.addPluginToMenu ("&Fecha_linha", self.action)



    def unload(self):
        
        self.iface.removePluginMenu(u'&Fecha_Linha', self.action)
        self.iface.removeToolBarIcon(self.action)
        # remove the toolbar
        


    def run(self):
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
                        self.iface.messageBar().pushMessage(u'Distãncia entre vertice final e inicial deve ser menor que a tolerãncia de 50 metros.', level=QgsMessageBar.WARNING, duration=5)   
                    else:
                        indice_ultimo_vertice = len(vertex_list)-1
                        last_vertex = geom.vertexAt(indice_ultimo_vertice)
                        geom.moveVertex(x1,y1, indice_ultimo_vertice)
                        geom.insertVertex(last_vertex.x(),last_vertex.y(),indice_ultimo_vertice)
                        layer.changeGeometry(feat.id(),geom)

                        
    def testLayerAtivo(self):
        if(not self.iface.activeLayer()):
            self.iface.messageBar().pushMessage(u'Selecione uma camada.', level=QgsMessageBar.INFO, duration=5)
            return False
        else:
            return True

    def testMetro(self):
        if(not self.iface.activeLayer().crs().mapUnits() == QGis.Meters):
            self.iface.messageBar().pushMessage(u'Sistema de coordenadas não suportado.', level=QgsMessageBar.INFO, duration=5)
            return False
        else:
            return True

    def testTipoGeometria(self):
        if(not self.iface.activeLayer().geometryType() == QGis.Line):
            self.iface.messageBar().pushMessage(u'A camada deve possuir geometrias do tipo linha.', level=QgsMessageBar.INFO, duration=5)
            return False
        elif(not self.iface.activeLayer().isEditable()):
            self.iface.messageBar().pushMessage(u'A camada deve estar em modo de edição.', level=QgsMessageBar.INFO, duration=5)
            return False
        else:
            return True

    def testGeometriaSelecionada(self):
        if(not len(self.iface.activeLayer().selectedFeatures()) == 1):
            self.iface.messageBar().pushMessage(u'Deve haver exatamente uma geometria linha selecionada.', level=QgsMessageBar.INFO, duration=5)
            return False
        else:
            return True        

    
