# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GEEML
                                 A QGIS plugin
 This plugin allows to apply ML algorithms based on GEE data
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-09-22
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Kazi Jahidur Rahaman
        email                : Kazi.Rahaman@hnee.de
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, qVersion
from qgis.PyQt.QtGui import QIcon 
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject, Qgis
from .geeml_libs.wrapper import *


# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .GEE_ML_dialog import GEEMLDialog
import os.path


class GEEML:
    """QGIS Plugin Implementation."""

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
            'GEEML_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GEEML')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GEEML', message)


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
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

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

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GEE_ML/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GEEML'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&GEEML'),
                action)
            self.iface.removeToolBarIcon(action)

    def select_output_layer_path(self):
        filename, _filter = QFileDialog.getSaveFileName(
            self.dlg, "Save output file ","", '')
        self.dlg.output_layer_path.setText(filename)
    
    def select_gee_credentials_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.dlg, "Open File", "", "JSON Files (*.json);;All Files (*)", options=options)
        
        if file_name:
            print(f"Selected file: {file_name}")
            
            # Here, you can further process the selected JSON file as needed.
            # For example, you can read its contents, parse the JSON data, and use it in your plugin.
            
            # Example of reading and processing the JSON file:
            if file_name:
                print(f"Selected file: {file_name}")
                self.dlg.GEE_CREDS_PATH.setText(file_name)  # Set the file path in the textbox

            # try:
            #     with open(file_name, 'r') as json_file:
            #         json_data = json.load(json_file)
            #         # Now, 'json_data' contains the parsed JSON data that you can work with.
                    
            #         # You can access specific fields in the JSON data like this:
            #         field_value = json_data.get('field_name', 'default_value')
                    
            #         # Perform further processing of the JSON data here.
            #         # ...
            # except Exception as e:
            #     print(f"Error processing JSON file: {str(e)}")

    def select_aoi_layer_path(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.dlg, "Open File", "", "Shape Files (*.shp);;All Files (*)", options=options)
        
        if file_name:
            print(f"Selected file: {file_name}")
            
            # Here, you can further process the selected JSON file as needed.
            # For example, you can read its contents, parse the JSON data, and use it in your plugin.
            
            # Example of reading and processing the JSON file:
            if file_name:
                print(f"Selected file: {file_name}")
                self.dlg.aoi_layer_path.setText(file_name)  # Set the file path in the textbox

            # try:
            #     with open(file_name, 'r') as json_file:
            #         json_data = json.load(json_file)
            #         # Now, 'json_data' contains the parsed JSON data that you can work with.
                    
            #         # You can access specific fields in the JSON data like this:
            #         field_value = json_data.get('field_name', 'default_value')
                    
            #         # Perform further processing of the JSON data here.
            #         # ...
            # except Exception as e:
            #     print(f"Error processing JSON file: {str(e)}")


    def select_train_layer_path(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.dlg, "Open File", "", "Shape Files (*.shp);;All Files (*)", options=options)
        
        if file_name:
            print(f"Selected file: {file_name}")
            
            # Here, you can further process the selected JSON file as needed.
            # For example, you can read its contents, parse the JSON data, and use it in your plugin.
            
            # Example of reading and processing the JSON file:
            if file_name:
                print(f"Selected file: {file_name}")
                self.dlg.train_layer_path.setText(file_name)  # Set the file path in the textbox

            # try:
            #     with open(file_name, 'r') as json_file:
            #         json_data = json.load(json_file)
            #         # Now, 'json_data' contains the parsed JSON data that you can work with.
                    
            #         # You can access specific fields in the JSON data like this:
            #         field_value = json_data.get('field_name', 'default_value')
                    
            #         # Perform further processing of the JSON data here.
            #         # ...
            # except Exception as e:
            #     print(f"Error processing JSON file: {str(e)}")

    def select_test_layer_path(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.dlg, "Open File", "", "Shape Files (*.shp);;All Files (*)", options=options)
        
        if file_name:
            print(f"Selected file: {file_name}")
            
            # Here, you can further process the selected JSON file as needed.
            # For example, you can read its contents, parse the JSON data, and use it in your plugin.
            
            # Example of reading and processing the JSON file:
            if file_name:
                print(f"Selected file: {file_name}")
                self.dlg.test_layer_path.setText(file_name)  # Set the file path in the textbox

            # try:
            #     with open(file_name, 'r') as json_file:
            #         json_data = json.load(json_file)
            #         # Now, 'json_data' contains the parsed JSON data that you can work with.
                    
            #         # You can access specific fields in the JSON data like this:
            #         field_value = json_data.get('field_name', 'default_value')
                    
            #         # Perform further processing of the JSON data here.
            #         # ...
            # except Exception as e:
            #     print(f"Error processing JSON file: {str(e)}")





    def run(self):
        """Run method that performs all the real work"""
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = GEEMLDialog()
        
        # self.dlg.GEE_SERVICE_ACC.setText('Hello')
        # Fetch the currently loaded layers
        layers = QgsProject.instance().layerTreeRoot().children()
        # Clear the contents of the comboBox from previous runs
        # self.dlg.aoi_layer.clear()
        # # Populate the comboBox with names of all the loaded layers
        # self.dlg.aoi_layer.addItems([layer.name() for layer in layers])
        # self.dlg.train_data_layer.addItems([layer.name() for layer in layers])
        # self.dlg.test_data_layer.addItems([layer.name() for layer in layers])

        self.dlg.GEE_CREDS_PATH.clear()
        self.dlg.gee_credentials_pbtn.clicked.connect(self.select_gee_credentials_file)
        self.dlg.aoi_layer_path.clear()
        self.dlg.aoi_layer_path_pbtn.clicked.connect(self.select_aoi_layer_path)
        self.dlg.train_layer_path.clear()
        self.dlg.train_layer_path_pbtn.clicked.connect(self.select_train_layer_path)
        self.dlg.test_layer_path.clear()
        self.dlg.test_layer_path_pbtn.clicked.connect(self.select_test_layer_path)
        self.dlg.output_layer_path.clear()
        self.dlg.output_layer_path_pbtn.clicked.connect(self.select_output_layer_path)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # filename = self.dlg.GEE_SERVICE_ACC.text()
            # output_file = open(filename, 'w')
           
            # selectedLayerIndex = self.dlg.comboBox.currentIndex()
            # selectedLayer = layers[selectedLayerIndex]
            # fields = selectedLayer.pendingFields()
            # fieldnames = [field.name() for field in fields]
            
            # for f in selectedLayer.getFeatures():
            #     line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
            #     unicode_line = line.encode('utf-8')
            #     output_file.write(unicode_line)
            # output_file.close()


            GEE_SERVICE_ACC = 'kjr-eej-jahid@ee-kazijahid.iam.gserviceaccount.com' #self.dlg.GEE_SERVICE_ACC.text() #'kjr-eej-jahid@ee-kazijahid.iam.gserviceaccount.com'
            GEE_CREDS_PATH = self.dlg.GEE_CREDS_PATH.text() # "D:/3. Projects/dash/ds4rs_main_app/ee-kazijahid-f8bb3244119c.json"

            collection_name= self.dlg.collection_name.text() # 'COPERNICUS/S2_SR_HARMONIZED'

            from_year = int(self.dlg.f_year.text()) #2023
            from_month = int(self.dlg.f_month.text()) #1
            print(type(from_month))
            to_year = int(self.dlg.t_year.text()) #2023
            to_month = int(self.dlg.t_month.text()) #12
            maximum_cloud = int(self.dlg.max_cloud.text()) #2 #cloud cover to filter the images in percentage
            mgrs_tile_no = '48PVT' #self.dlg.collection_name.text() ## '48PVT'  For the area of our interest mgrs tile no is 48PVT. For different aoi please check sentinel 2 docs
            dark_feature_percenatge = int(self.dlg.dark_percentage.text())# 1
            aoi_path =  self.dlg.aoi_layer_path.text() #"D:/3. Projects/ClassificationTasks/Classification-No74Indices/Data/PH_Extent/extent.shp" # location of area of interest shape file in your storage


 

            training_choice = 1 # 1 or 2. 1 = Training Fresh, 2 = Use Pretrained
            train_samples_path = self.dlg.train_layer_path.text() #"D:/3. Projects/ClassificationTasks/Classification-No74Indices/Data/TrainingData/TrainingData_Reduced.shp"
            test_samples_path = self.dlg.test_layer_path.text() # "D:/3. Projects/ClassificationTasks/Classification-No74Indices/Data/TrainingData/TestData_Reduced.shp"

            file_saving_path =  self.dlg.output_layer_path.text() #'./temp'
            bands_to_include = ['B1', 'B2', 'B3', 'B4', 'B5']
            print(bands_to_include)
                                #, 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12','NDBI','NDWI', 'NDVI','BSI'] # EVI and NBR also available
#self.dlg.bands_to_include.text() 
            if training_choice == 1:
                trainFreshModel(
                    GEE_SERVICE_ACC,GEE_CREDS_PATH,
                    collection_name, from_year, from_month, to_year, to_month, maximum_cloud, mgrs_tile_no, dark_feature_percenatge, 
                    aoi_path, train_samples_path, test_samples_path, file_saving_path,
                    bands_to_include)
            elif training_choice ==2:
                print('Using pretrained')
            else:
                print(f'Please provide the correct choice!')
                