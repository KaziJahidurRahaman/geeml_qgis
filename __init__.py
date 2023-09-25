# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GEEML
                                 A QGIS plugin
 This plugin allows to apply ML algorithms based on GEE data
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-09-22
        copyright            : (C) 2023 by Kazi Jahidur Rahaman
        email                : Kazi.Rahaman@hnee.de
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
    """Load GEEML class from file GEEML.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .GEE_ML import GEEML
    return GEEML(iface)
