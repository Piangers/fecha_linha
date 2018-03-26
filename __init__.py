# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Suavizacao
                                 A QGIS plugin
 ferramenta
                             -------------------
        begin                : 2018-03-07
        copyright            : (C) 2018 by piangers
        email                : cesar_piangers@hotmail.com
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Suavizacao class from file Suavizacao.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .suavizacao import Suavizacao
    return Suavizacao(iface)
