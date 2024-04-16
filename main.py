from interface import *
import sys
import os
from PySide2 import *
from PySide2 import *
from qt_material import *
from PySide2 import QtCore, QtGui,QtWidgets
from PySide2.QtCore import *
import psutil
#from psutil import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PySide2extn
import datetime
import shutil
#import pyside2
platforms={
    "linux":"Linux",
    "linux1":"Linux",
    "darwin":"OS x",
    "win32":"Windows",
    "win64":"Windows"
    }
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        ### REMOVE WINDOW TITTLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        ### Set Main Background to transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ###Shadow effect style
        self.shadow=QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,92,157,550))
        ### Apply Shadow Effect to Central Widget
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        ### set window Icon
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/airplay.svg"))
        ### Set Window Tittle
        self.setWindowTitle("Process Manager")
        ### Window Size grip to Resize
        QSizeGrip(self.ui.size_grip)
        self.ui.close_window.clicked.connect(lambda:self.close())
        self.ui.minimize_window.clicked.connect(lambda:self.showMinimized())
        self.ui.restore_window.clicked.connect(lambda:self.restore_or_maximize_window())



        ### Navigate Between Page

        ## To cpu Page
        self.ui.cpu_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_memory) )
        ## To Battery Page
        self.ui.battery_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.battery) )
        ## To Battery Page
        self.ui.battery_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.battery) )
        ## To System Information
        self.ui.monitor_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.System_Information) )
        ## To Activity Page
        self.ui.activity_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.activities) )
        ## To Storage page
        self.ui.storage.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.storage_2) )
        ## To Sensors Page
        self.ui.sensors_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.sensors) )
        ## To Network Page
        self.ui.Network_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.networks) )

        def moveWindow(e):
            ### roundProgressBar(self.cpu_percent)
            ### spiralProgressBar(self.ram_percent)
            if self.isMaximized()==False:### Not Maximized
                if e.buttons()==Qt.LeftButton or e.buttons()==Qt.RightButton:
                    self.move(self.pos()+e.globalPos()-self.clickPosition)
                    print("Positions:\nPosition:{}\nGlobal Position:{}\nClicked Position:{}".format(self.pos(), e.globalPos(),self.clickPosition))
                    self.clickPosition=e.globalPos()
                    e.accept()
        ### Move Window
        self.ui.header.mouseMoveEvent=moveWindow
        ### Menu Animation
        self.ui.Menu_btn.clicked.connect(lambda: self.slideLeftMenu())
        
        apply_stylesheet(app,theme='dark_cyan.xml')

        for w in self.ui.menu_frame.findChildren(QPushButton):
            w.clicked.connect(self.applyButtonStyle)

        ### Battery
        self.battery()
        ### CPU And Memory
        self.cpu_ram()
        ### System Information
        self.system_info()
        ### Activities
        self.processes()
        ### Storage
        self.storage()
        ### Sensors
        self.sensors()
        ### Neworks
        self.net()
        self.show()
    
    def sec2hours(self,i):
        return str(int(i/3600))
    def net(self):
        ## Net Stats
        for x in psutil.net_if_stats():
            z=psutil.net_if_stats()
            # Create New Row
            rowPosition=self.ui.net_stats_table.rowCount()
            self.ui.net_stats_table.insertRow(rowPosition)
            self.create_table_widget(rowPosition,0,str(x),"net_stats_table")
            self.create_table_widget(rowPosition,1,str(z[x].isup),"net_stats_table")
            self.create_table_widget(rowPosition,2,str(z[x].duplex),"net_stats_table")
            self.create_table_widget(rowPosition,3,str(z[x].speed),"net_stats_table")
            self.create_table_widget(rowPosition,4,str(z[x].mtu),"net_stats_table")
        ## Net IO Counters
        for x in psutil.net_io_counters(pernic=True):
            z=psutil.net_io_counters(pernic=True)
            rowPosition=self.ui.net_io_table.rowCount()
            self.ui.net_io_table.insertRow(rowPosition)
            self.create_table_widget(rowPosition,0,str(x),"net_io_table")
            self.create_table_widget(rowPosition,1,str(z[x].bytes_sent),"net_io_table")
            self.create_table_widget(rowPosition,2,str(z[x].bytes_recv),"net_io_table")
            self.create_table_widget(rowPosition,3,str(z[x].packets_sent),"net_io_table")
            self.create_table_widget(rowPosition,4,str(z[x].packets_recv),"net_io_table")
            self.create_table_widget(rowPosition,5,str(z[x].errin),"net_io_table")
            self.create_table_widget(rowPosition,6,str(z[x].errout),"net_io_table")
            self.create_table_widget(rowPosition,7,str(z[x].dropin),"net_io_table")
            self.create_table_widget(rowPosition,8,str(z[x].dropout),"net_io_table")
        ### Net Addresses
        for x in psutil.net_if_addrs():
            z=psutil.net_if_addrs()
            for y in z[x]:
                rowPosition=self.ui.net_address_table.rowCount()
                self.ui.net_address_table.insertRow(rowPosition)
                self.create_table_widget(rowPosition,0,str(x),"net_address_table")
                self.create_table_widget(rowPosition,1,str(y.family),"net_address_table")
                self.create_table_widget(rowPosition,2,str(y.address),"net_address_table")
                self.create_table_widget(rowPosition,3,str(y.netmask),"net_address_table")
                self.create_table_widget(rowPosition,4,str(y.broadcast),"net_address_table")
                self.create_table_widget(rowPosition,5,str(y.ptp),"net_address_table")
                
        for x in psutil.net_connections():
            z=psutil.net_connections()
            rowPosition=self.ui.net_connections_table.rowCount()
            self.ui.net_connections_table.insertRow(rowPosition)
            
            self.create_table_widget(rowPosition,0,str(x.fd),"net_connections_table")
            self.create_table_widget(rowPosition,1,str(x.family),"net_connections_table")
            self.create_table_widget(rowPosition,2,str(x.type),"net_connections_table")
            self.create_table_widget(rowPosition,3,str(x.laddr),"net_connections_table")
            self.create_table_widget(rowPosition,4,str(x.raddr),"net_connections_table")
            self.create_table_widget(rowPosition,5,str(x.status),"net_connections_table")
            self.create_table_widget(rowPosition,6,str(x.pid),"net_connections_table")
    ######### create_table_widget
    def create_table_widget(self,rowPosition,columnPosition,text,tableName):
        qtable=QTableWidgetItem()
        #USE getattr() Method
        getattr(self.ui,tableName).setItem(rowPosition,columnPosition,qtable)
        qtablei=getattr(self.ui,tableName).item(rowPosition,columnPosition)
        qtablei.setText(text)
    #################### Get Running Activities
    def processes(self):
        for x in psutil.pids():
            rowPosition=self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowPosition)
            try:
                processus=psutil.Process(x)
                self.create_table_widget(rowPosition,0,str(processus.pid),"tableWidget")
                self.create_table_widget(rowPosition,1,str(processus.name()),"tableWidget")
                self.create_table_widget(rowPosition,2,str(processus.status()),"tableWidget")
                self.create_table_widget(rowPosition,3,str(datetime.datetime.utcfromtimestamp(processus.create_time()).strftime("%Y-%m-%d: %H:%M:%S")),"tableWidget")

                # Create cell widget =button for each row
                suspend_btn=QPushButton(self.ui.tableWidget)
                suspend_btn.setText("Suspend")
                suspend_btn.setStyleSheet("color: brown;")
                self.ui.tableWidget.setCellWidget(rowPosition,4,suspend_btn)

                resume_btn=QPushButton(self.ui.tableWidget)
                resume_btn.setText("Resume")
                resume_btn.setStyleSheet("color: green;")
                self.ui.tableWidget.setCellWidget(rowPosition,5,resume_btn)

                terminate_btn=QPushButton(self.ui.tableWidget)
                terminate_btn.setText("Terminate")
                terminate_btn.setStyleSheet("color: orange;")
                self.ui.tableWidget.setCellWidget(rowPosition,6,terminate_btn)

                kill_btn=QPushButton(self.ui.tableWidget)
                kill_btn.setText("Kill")
                kill_btn.setStyleSheet("color: red;")
                self.ui.tableWidget.setCellWidget(rowPosition,7,kill_btn)
            except Exception as e:
                print("An Error Occured in creating Table Widget Items ..........\n",e)
        self.ui.activity_search.textChanged.connect(self.findName)
    
    ####### Find Name
    def findName(self):
        name=self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            
            item=self.ui.tableWidget.item(row,1)
            #print("Item:",item)
            try:
                self.ui.tableWidget.setRowHidden(row,name not in item.text().lower())
            except Exception as e:
                print("Probably a Processus is killed so we pass to next line ....\n",e)
                pass
    #####################Sensors Informations
    def sensors(self):
        if sys.platform=="linux" or  sys.platform=="linux1" or sys.platform=="linux2":
            for x in psutil.sensors_temperatures():
                for y in psutil.sensors_temperatures()[x]:
                    rowPosition=self.ui.sensorTable.rowCount()
                    self.create_table_widget(rowPosition,0,x,"sensorTable")
                    self.create_table_widget(rowPosition,1,str(y.label),"sensorTable")
                    self.create_table_widget(rowPosition,2,str(y.current),"sensorTable")
                    self.create_table_widget(rowPosition,3,str(y.high),"sensorTable")
                    self.create_table_widget(rowPosition,4,str(y.critical),"sensorTable")
                    temp_per=(y.current/y.high)*100
                    progressBar=QProgressBar(self.ui.sensorTable)
                    progressBar.setObjectName(u"progressBar")
                    progressBar.setValue(temp_per)
                    self.ui.sensorTable.setCellWidget(rowPosition,5,progressBar)
        else:
            global platforms
            rowPosition=self.ui.sensorTable.rowCount()
            self.ui.sensorTable.insertRow(rowPosition)
            self.create_table_widget(rowPosition,0,"Function not supported on"+str(platforms[sys.platform]),"sensorTable")
            self.create_table_widget(rowPosition,1,"N/A","sensorTable")
            self.create_table_widget(rowPosition,2,"N/A","sensorTable")
            self.create_table_widget(rowPosition,3,"N/A","sensorTable")
            self.create_table_widget(rowPosition,4,"N/A","sensorTable")
    #####################Storage Partitions
    def storage(self):
        global platforms
        storage_device=psutil.disk_partitions(all=False)
        for x in storage_device:
            ### Create a NewRow
            rowPosition=self.ui.storageTable.rowCount()
            self.ui.storageTable.insertRow(rowPosition)
            self.create_table_widget(rowPosition,0,x.device,"storageTable")
            self.create_table_widget(rowPosition,1,x.mountpoint,"storageTable")
            self.create_table_widget(rowPosition,2,x.fstype,"storageTable")
            self.create_table_widget(rowPosition,3,x.opts,"storageTable")
            if sys.platform=="linux" or sys.platform=="linux1" or sys.platform=="linux2":
                self.create_table_widget(rowPosition,4,str(x.maxfile),"storageTable")
                self.create_table_widget(rowPosition,5,str(x.maxpath),"storageTable")
            else:
                self.create_table_widget(rowPosition,4,str("Function Not Available on "+platforms[sys.platform]),"storageTable")
                self.create_table_widget(rowPosition,5,str("Function Not Available on "+platforms[sys.platform]),"storageTable")
            disk_usage=shutil.disk_usage(x.mountpoint)
            self.create_table_widget(rowPosition,6,str(round(disk_usage.total/(1024*1024*1024),2))+"GB","storageTable")
            self.create_table_widget(rowPosition,7,str(round(disk_usage.free/(1024*1024*1024),2))+"GB","storageTable")
            print("Disk Usage:",disk_usage.used)
            self.create_table_widget(rowPosition,8,str(round(disk_usage.used/(1024*1024*1024),2))+"GB","storageTable")
            full_disk=(disk_usage.used/disk_usage.total)*100
            progressBar=QProgressBar(self.ui.storageTable)
            progressBar.setObjectName(u"progressBar")
            progressBar.setValue(full_disk)
            self.ui.storageTable.setCellWidget(rowPosition,9,progressBar)
    #####################System Information
    def system_info(self):
        time=datetime.datetime.now().strftime("%I:%M:%S %p")
        self.ui.system_date.setText(str(time))
        date=datetime.datetime.now().strftime("%Y-%m-%d")
        self.ui.system_time.setText(str(date))

        self.ui.system_machine.setText(platform.machine())
        self.ui.system_version.setText(platform.version())
        self.ui.system_platform.setText(platform.platform())
        self.ui.system_system.setText(platform.system())
        self.ui.system_processor.setText(platform.processor())
     ######## Ram Informations
    def cpu_ram(self):
        ## Total Ram
        #totalRam=1.0
        totalRam=psutil.virtual_memory()[0]
        print("=>",psutil.virtual_memory()[0])
        totalRam=totalRam/(1024*1024*1024)
        self.ui.total_ram.setText(str(str(round(totalRam,2))+"GB"))
        ## Available Ram
        availableRam=1.0
        availableRam=psutil.virtual_memory()[1]*availableRam
        availableRam=availableRam/(1024*1024*1024)
        self.ui.available_ram.setText(str("{:.2f}".format(availableRam)+"GB"))
        ## Used Ram
        ramUsed=1.0
        ramUsed=psutil.virtual_memory()[3]*ramUsed
        ramUsed=ramUsed/(1024*1024*1024)
        self.ui.ram_used.setText(str("{:.2f}".format(ramUsed)+"GB"))
        ## Free Ram
        freeRam=1.0
        freeRam=psutil.virtual_memory()[4]*freeRam
        freeRam=freeRam/(1024*1024*1024)
        self.ui.free_ram.setText(str("{:.2f}".format(freeRam)+"GB"))

        ## Usage Ram
        usageR=1.0
        usageR=psutil.virtual_memory()[2]*usageR
        
        #usageR=usageR/(1024*1024*1024)
        print("Usage Ram:",usageR)
        self.ui.ram_usage.setText(str("{:.4f}".format(usageR)+"%"))        
        ##############CPU USAGE
        core =psutil.cpu_count()
        self.ui.cpu_count.setText(str(core))
        cpup =psutil.cpu_percent()
        self.ui.cpu_per.setText(str(cpup)+"%")
        cpum=psutil.cpu_count(logical=False)
        self.ui.cpu_main_core.setText(str(cpum))
        ########### PROGRESS BAR Configuration FOR CPU
        #### Set The Max Value
        self.ui.cpu_percentage.rpb_setMaximum(100)
        ### Set Progress Value
        self.ui.cpu_percentage.rpb_setValue(cpup)        
        ## Set Bar Style
        self.ui.battery_usage.rpb_setBarStyle("Hybrid2")
        ### set Line Color
        self.ui.battery_usage.rpb_setLineColor((255,30,99))
        ### Set Pipe Color
        self.ui.battery_usage.rpb_setPieColor((45,74,83))
        ## Set Progress Bar Text Color
        self.ui.battery_usage.rpb_setTextColor((255,255,255))
        ## Set Progress Bar Starting Position
        # North , East,West,South
        self.ui.battery_usage.rpb_setInitialPos("West")
        ## Set Progress Bar Text Type: Value or Percentage
        
        self.ui.battery_usage.rpb_setTextFormat("Percentage")
        ## Set Progress Bar Line Widtth
        self.ui.battery_usage.rpb_setLineWidth(15)
        ## Set Progress Bar Font
        self.ui.battery_usage.rpb_setTextFont("Arial")
        ## Set Progress Bar Path Widtth
        self.ui.battery_usage.rpb_setPathWidth(15)
        ## Set Progress Bar Line Cap RoundCap, SquareCap
        self.ui.battery_usage.rpb_setLineCap("RoundCap")
        ########### PROGRESS BAR Configuration FOR RAM
        ## Set Minimum Value
        self.ui.ram_percent.spb_setMinimum((0,0,0))
        ## Set Max Value
        self.ui.ram_percent.spb_setMaximum((totalRam,totalRam,totalRam))
        ## Set Progress Value
        self.ui.ram_percent.spb_setValue((availableRam,ramUsed,freeRam))
        ## Set Progress
        self.ui.ram_percent.spb_lineColor(((6,233,38),(6,201,233),(233,6,201)))
        ## Set Progress Initial Position
        self.ui.ram_percent.spb_setInitialPos(("West","West","West"))
        ## Hide the Path !!!!!!!!!!!!!!!!!!!
        self.ui.ram_percent.spb_setPathHidden(True)
    ######## Batteru Informations
    def battery(self):
        batt = psutil.sensors_battery()
        if not hasattr(psutil, "sensors_battery"):
            self.ui.battery_status.setText("Platform Not Supported")
        if batt is None:
            self.ui.battery_status.setText("No Battery Installed")
        if batt.power_plugged:
            self.ui.battery_charge.setText(str(round(batt.percent, 2)) + "%")
            self.ui.battery_time_left.setText("N/A")
            if batt.percent < 100:
                self.ui.battery_status.setText("Charging")
            else:
                self.ui.battery_status.setText("Fully Charged")
            self.ui.battery_plugged.setText("Yes")
        else:
            self.ui.battery_charge.setText(str(round(batt.percent, 2)) + "%")
            self.ui.battery_time_left.setText(self.sec2hours(batt.secsleft))
            if batt.percent < 100:
                self.ui.battery_status.setText("Discharging")
            else:
                self.ui.battery_status.setText("Fully Charged")
            self.ui.battery_plugged.setText("No")
        ### Set Max Progress Value
        self.ui.battery_usage.rpb_setMaximum(100)
        ## Set Progress Value
        self.ui.battery_usage.rpb_setValue(batt.percent)
        ### Set Bar Style
        self.ui.battery_usage.rpb_setBarStyle("Hybrid2")
        ### set Line Color
        self.ui.battery_usage.rpb_setLineColor((255,30,99))
        ### Set Pipe Color
        self.ui.battery_usage.rpb_setPieColor((45,74,83))
        ## Set Progress Bar Text Color
        self.ui.battery_usage.rpb_setTextColor((255,255,255))
        ## Set Progress Bar Starting Position
        # North , East,West,South
        self.ui.battery_usage.rpb_setInitialPos("West")
        ## Set Progress Bar Text Type: Value or Percentage
        ## Set Progress Bar Font
        self.ui.battery_usage.rpb_setTextFormat("Percentage")
        ## Set Progress Bar Line Widtth
        self.ui.battery_usage.rpb_setLineWidth(15)
        ## Set Progress Bar Path Widtth
        self.ui.battery_usage.rpb_setPathWidth(15)
        ## Set Progress Bar Line Cap RoundCap, SquareCap
        self.ui.battery_usage.rpb_setLineCap("RoundCap")
    ######## Menu Button Styling Function
    
    def applyButtonStyle(self):
        ## Reset Style For other Buttons
        for w in self.ui.menu_frame.findChildren(QPushButton):
            # If Button name is not equal to clicked button name
            if w.objectName()!=self.sender().objectName():
                ## Default border style
                w.setStyleSheet("border-bottom:none none;")
        self.sender().setStyleSheet("border-bottom:2px solid")
        return
             
    def slideLeftMenu(self):
        width=self.ui.left_frame_count.width()
        if width==40:
            newWidth=200
        else:
            newWidth=40
        self.animation=QPropertyAnimation(self.ui.left_frame_count,b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
    def mousePressEvent(self,Event):
        self.clickPosition=Event.globalPos()
    
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
if __name__=="__main__":
    print("Sys.Argv:",sys.argv)
    app= QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec_())
