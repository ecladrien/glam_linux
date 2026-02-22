# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainframeOuSobV.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)
from ..gui import ressources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1005, 978)
        MainWindow.setMaximumSize(QSize(1920, 1080))
        MainWindow.setStyleSheet(u"background-color: black;\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget {\n"
"    color: white;\n"
"}\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    border: 2px solid red;\n"
"    border-radius: 6px;\n"
"    color: red;\n"
"    font-size: 10px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 2px solid #ffffff;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border: 2px solid #999999;\n"
"	color: #999999;\n"
"}\n"
"\n"
"QFrame {\n"
"	background-color: transparent;\n"
"	border: 2px solid red;\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"QLabel {\n"
"	border: transparent\n"
"}\n"
"\n"
"#log {\n"
"	color:red;\n"
"}\n"
"\n"
"#time_label {\n"
"	color:red;\n"
"}\n"
"\n"
"")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_bar = QWidget(self.centralwidget)
        self.main_bar.setObjectName(u"main_bar")
        self.horizontalLayout_2 = QHBoxLayout(self.main_bar)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.side_frame = QFrame(self.main_bar)
        self.side_frame.setObjectName(u"side_frame")
        self.side_frame.setMinimumSize(QSize(150, 0))
        self.side_frame.setMaximumSize(QSize(150, 16777215))
        self.side_frame.setFrameShape(QFrame.Shape.Box)
        self.gridLayout = QGridLayout(self.side_frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plan_button = QPushButton(self.side_frame)
        self.plan_button.setObjectName(u"plan_button")
        self.plan_button.setMaximumSize(QSize(100, 100))
        self.plan_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.plan_button.setStyleSheet(u"")
        icon = QIcon()
        icon.addFile(u":/icons/ressources/icons/plan_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.plan_button.setIcon(icon)
        self.plan_button.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.plan_button, 1, 0, 1, 1)

        self.qlc_button = QPushButton(self.side_frame)
        self.qlc_button.setObjectName(u"qlc_button")
        self.qlc_button.setMaximumSize(QSize(100, 100))
        self.qlc_button.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/ressources/icons/sliders_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.qlc_button.setIcon(icon1)
        self.qlc_button.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.qlc_button, 4, 0, 1, 1)

        self.setup_button = QPushButton(self.side_frame)
        self.setup_button.setObjectName(u"setup_button")
        self.setup_button.setMaximumSize(QSize(100, 100))
        font = QFont()
        font.setBold(True)
        self.setup_button.setFont(font)
        self.setup_button.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/ressources/icons/settings_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.setup_button.setIcon(icon2)
        self.setup_button.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.setup_button, 5, 0, 1, 1)

        self.home_button = QPushButton(self.side_frame)
        self.home_button.setObjectName(u"home_button")
        self.home_button.setMinimumSize(QSize(0, 0))
        self.home_button.setMaximumSize(QSize(100, 100))
        self.home_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.home_button.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/ressources/icons/home_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.home_button.setIcon(icon3)
        self.home_button.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.home_button, 0, 0, 1, 1)

        self.cam_button = QPushButton(self.side_frame)
        self.cam_button.setObjectName(u"cam_button")
        self.cam_button.setMaximumSize(QSize(100, 100))
        self.cam_button.setStyleSheet(u"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/ressources/icons/video_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cam_button.setIcon(icon4)
        self.cam_button.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.cam_button, 3, 0, 1, 1)

        self.measurement_button = QPushButton(self.side_frame)
        self.measurement_button.setObjectName(u"measurement_button")
        self.measurement_button.setMaximumSize(QSize(100, 100))
        self.measurement_button.setStyleSheet(u"")
        icon5 = QIcon()
        icon5.addFile(u":/icons/ressources/icons/zap_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.measurement_button.setIcon(icon5)
        self.measurement_button.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.measurement_button, 2, 0, 1, 1)


        self.horizontalLayout_2.addWidget(self.side_frame)

        self.main_frame = QStackedWidget(self.main_bar)
        self.main_frame.setObjectName(u"main_frame")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.verticalLayout_4 = QVBoxLayout(self.home_page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.background_image = QLabel(self.home_page)
        self.background_image.setObjectName(u"background_image")
        self.background_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.background_image)

        self.button_home_page_widget = QWidget(self.home_page)
        self.button_home_page_widget.setObjectName(u"button_home_page_widget")
        self.button_home_page_widget.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout_3 = QHBoxLayout(self.button_home_page_widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 12)
        self.restart_button = QPushButton(self.button_home_page_widget)
        self.restart_button.setObjectName(u"restart_button")
        self.restart_button.setMinimumSize(QSize(0, 100))
        self.restart_button.setMaximumSize(QSize(100, 16777215))
        self.restart_button.setStyleSheet(u"")
        icon6 = QIcon()
        icon6.addFile(u":/icons/ressources/icons/refresh-cw_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.restart_button.setIcon(icon6)
        self.restart_button.setIconSize(QSize(30, 30))

        self.horizontalLayout_3.addWidget(self.restart_button)

        self.shutdown_button = QPushButton(self.button_home_page_widget)
        self.shutdown_button.setObjectName(u"shutdown_button")
        self.shutdown_button.setMinimumSize(QSize(0, 100))
        self.shutdown_button.setMaximumSize(QSize(100, 16777215))
        self.shutdown_button.setStyleSheet(u"")
        icon7 = QIcon()
        icon7.addFile(u":/icons/ressources/icons/power_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shutdown_button.setIcon(icon7)
        self.shutdown_button.setIconSize(QSize(30, 30))

        self.horizontalLayout_3.addWidget(self.shutdown_button)


        self.verticalLayout_4.addWidget(self.button_home_page_widget)

        self.main_frame.addWidget(self.home_page)
        self.plan_page = QWidget()
        self.plan_page.setObjectName(u"plan_page")
        self.horizontalLayout_4 = QHBoxLayout(self.plan_page)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.main_frame.addWidget(self.plan_page)
        self.measurement_page = QWidget()
        self.measurement_page.setObjectName(u"measurement_page")
        self.verticalLayout_3 = QVBoxLayout(self.measurement_page)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.phases_label_widget = QWidget(self.measurement_page)
        self.phases_label_widget.setObjectName(u"phases_label_widget")
        self.phases_label_widget.setMaximumSize(QSize(16777215, 100))
        self.phases_label_widget.setStyleSheet(u"color: red;")
        self.horizontalLayout_13 = QHBoxLayout(self.phases_label_widget)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.neutral_label = QLabel(self.phases_label_widget)
        self.neutral_label.setObjectName(u"neutral_label")
        font1 = QFont()
        font1.setPointSize(20)
        self.neutral_label.setFont(font1)
        self.neutral_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.neutral_label)

        self.phase_1_label = QLabel(self.phases_label_widget)
        self.phase_1_label.setObjectName(u"phase_1_label")
        self.phase_1_label.setFont(font1)
        self.phase_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.phase_1_label)

        self.phase_2_label = QLabel(self.phases_label_widget)
        self.phase_2_label.setObjectName(u"phase_2_label")
        self.phase_2_label.setFont(font1)
        self.phase_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.phase_2_label)

        self.phase_3_label = QLabel(self.phases_label_widget)
        self.phase_3_label.setObjectName(u"phase_3_label")
        self.phase_3_label.setFont(font1)
        self.phase_3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.phase_3_label)


        self.verticalLayout_3.addWidget(self.phases_label_widget)

        self.value_label_widget = QWidget(self.measurement_page)
        self.value_label_widget.setObjectName(u"value_label_widget")
        self.value_label_widget.setMaximumSize(QSize(16777215, 150))
        self.horizontalLayout_14 = QHBoxLayout(self.value_label_widget)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.neutral_value_frame = QFrame(self.value_label_widget)
        self.neutral_value_frame.setObjectName(u"neutral_value_frame")
        self.neutral_value_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.neutral_value_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.neutral_value_frame)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.neutral_value_label = QLabel(self.neutral_value_frame)
        self.neutral_value_label.setObjectName(u"neutral_value_label")
        font2 = QFont()
        font2.setPointSize(30)
        self.neutral_value_label.setFont(font2)
        self.neutral_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.neutral_value_label)


        self.horizontalLayout_14.addWidget(self.neutral_value_frame)

        self.phase_1_value_frame = QFrame(self.value_label_widget)
        self.phase_1_value_frame.setObjectName(u"phase_1_value_frame")
        self.phase_1_value_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.phase_1_value_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.phase_1_value_frame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.phase_1_value_label = QLabel(self.phase_1_value_frame)
        self.phase_1_value_label.setObjectName(u"phase_1_value_label")
        self.phase_1_value_label.setFont(font2)
        self.phase_1_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_7.addWidget(self.phase_1_value_label)


        self.horizontalLayout_14.addWidget(self.phase_1_value_frame)

        self.phase_2_value_frame = QFrame(self.value_label_widget)
        self.phase_2_value_frame.setObjectName(u"phase_2_value_frame")
        self.phase_2_value_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.phase_2_value_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.phase_2_value_frame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.phase_2_value_label = QLabel(self.phase_2_value_frame)
        self.phase_2_value_label.setObjectName(u"phase_2_value_label")
        self.phase_2_value_label.setFont(font2)
        self.phase_2_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.phase_2_value_label)


        self.horizontalLayout_14.addWidget(self.phase_2_value_frame)

        self.phase_3_value_frame = QFrame(self.value_label_widget)
        self.phase_3_value_frame.setObjectName(u"phase_3_value_frame")
        self.phase_3_value_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.phase_3_value_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.phase_3_value_frame)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.phase_3_value_label = QLabel(self.phase_3_value_frame)
        self.phase_3_value_label.setObjectName(u"phase_3_value_label")
        self.phase_3_value_label.setFont(font2)
        self.phase_3_value_label.setStyleSheet(u"border: red;")
        self.phase_3_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_9.addWidget(self.phase_3_value_label)


        self.horizontalLayout_14.addWidget(self.phase_3_value_frame)


        self.verticalLayout_3.addWidget(self.value_label_widget)

        self.measurement_line_1 = QFrame(self.measurement_page)
        self.measurement_line_1.setObjectName(u"measurement_line_1")
        self.measurement_line_1.setFrameShape(QFrame.Shape.HLine)
        self.measurement_line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.measurement_line_1)

        self.graph_frame = QFrame(self.measurement_page)
        self.graph_frame.setObjectName(u"graph_frame")
        self.graph_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.graph_frame)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.graph_label = QLabel(self.graph_frame)
        self.graph_label.setObjectName(u"graph_label")

        self.horizontalLayout_11.addWidget(self.graph_label)


        self.verticalLayout_3.addWidget(self.graph_frame)

        self.measurement_line_2 = QFrame(self.measurement_page)
        self.measurement_line_2.setObjectName(u"measurement_line_2")
        self.measurement_line_2.setFrameShape(QFrame.Shape.HLine)
        self.measurement_line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.measurement_line_2)

        self.measurement_button_widget = QWidget(self.measurement_page)
        self.measurement_button_widget.setObjectName(u"measurement_button_widget")
        self.measurement_button_widget.setMaximumSize(QSize(16777215, 150))
        self.horizontalLayout_12 = QHBoxLayout(self.measurement_button_widget)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.measurement_start_button = QPushButton(self.measurement_button_widget)
        self.measurement_start_button.setObjectName(u"measurement_start_button")
        self.measurement_start_button.setMaximumSize(QSize(200, 150))
        self.measurement_start_button.setStyleSheet(u"")
        icon8 = QIcon()
        icon8.addFile(u":/icons/ressources/icons/play_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.measurement_start_button.setIcon(icon8)
        self.measurement_start_button.setIconSize(QSize(50, 50))

        self.horizontalLayout_12.addWidget(self.measurement_start_button)

        self.measurement_stop_button = QPushButton(self.measurement_button_widget)
        self.measurement_stop_button.setObjectName(u"measurement_stop_button")
        self.measurement_stop_button.setMaximumSize(QSize(200, 150))
        self.measurement_stop_button.setStyleSheet(u"")
        icon9 = QIcon()
        icon9.addFile(u":/icons/ressources/icons/stop_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.measurement_stop_button.setIcon(icon9)
        self.measurement_stop_button.setIconSize(QSize(50, 50))

        self.horizontalLayout_12.addWidget(self.measurement_stop_button)

        self.measurement_reset_button = QPushButton(self.measurement_button_widget)
        self.measurement_reset_button.setObjectName(u"measurement_reset_button")
        self.measurement_reset_button.setMaximumSize(QSize(200, 150))
        self.measurement_reset_button.setStyleSheet(u"")
        self.measurement_reset_button.setIcon(icon6)
        self.measurement_reset_button.setIconSize(QSize(50, 50))

        self.horizontalLayout_12.addWidget(self.measurement_reset_button)

        self.measurement_savegraph_button = QPushButton(self.measurement_button_widget)
        self.measurement_savegraph_button.setObjectName(u"measurement_savegraph_button")
        self.measurement_savegraph_button.setMaximumSize(QSize(200, 150))
        self.measurement_savegraph_button.setStyleSheet(u"")
        icon10 = QIcon()
        icon10.addFile(u":/icons/ressources/icons/archive_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.measurement_savegraph_button.setIcon(icon10)
        self.measurement_savegraph_button.setIconSize(QSize(50, 50))

        self.horizontalLayout_12.addWidget(self.measurement_savegraph_button)


        self.verticalLayout_3.addWidget(self.measurement_button_widget)

        self.main_frame.addWidget(self.measurement_page)
        self.cam_page = QWidget()
        self.cam_page.setObjectName(u"cam_page")
        self.verticalLayout_5 = QVBoxLayout(self.cam_page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.flux_video_widget = QWidget(self.cam_page)
        self.flux_video_widget.setObjectName(u"flux_video_widget")
        self.horizontalLayout_15 = QHBoxLayout(self.flux_video_widget)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.flux_video_label = QLabel(self.flux_video_widget)
        self.flux_video_label.setObjectName(u"flux_video_label")

        self.horizontalLayout_15.addWidget(self.flux_video_label)


        self.verticalLayout_5.addWidget(self.flux_video_widget)

        self.button_search_cam_widget = QWidget(self.cam_page)
        self.button_search_cam_widget.setObjectName(u"button_search_cam_widget")
        self.button_search_cam_widget.setMaximumSize(QSize(16777215, 150))
        self.horizontalLayout_5 = QHBoxLayout(self.button_search_cam_widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.connect_cam_button = QPushButton(self.button_search_cam_widget)
        self.connect_cam_button.setObjectName(u"connect_cam_button")
        self.connect_cam_button.setMaximumSize(QSize(100, 100))
        icon11 = QIcon()
        icon11.addFile(u":/icons/ressources/icons/connect_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.connect_cam_button.setIcon(icon11)
        self.connect_cam_button.setIconSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.connect_cam_button)

        self.plus_zoom_cam_button = QPushButton(self.button_search_cam_widget)
        self.plus_zoom_cam_button.setObjectName(u"plus_zoom_cam_button")
        self.plus_zoom_cam_button.setMaximumSize(QSize(100, 100))
        icon12 = QIcon()
        icon12.addFile(u":/icons/ressources/icons/plus_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.plus_zoom_cam_button.setIcon(icon12)
        self.plus_zoom_cam_button.setIconSize(QSize(40, 40))

        self.horizontalLayout_5.addWidget(self.plus_zoom_cam_button)

        self.minus_zoom_cam_button = QPushButton(self.button_search_cam_widget)
        self.minus_zoom_cam_button.setObjectName(u"minus_zoom_cam_button")
        self.minus_zoom_cam_button.setMaximumSize(QSize(100, 100))
        icon13 = QIcon()
        icon13.addFile(u":/icons/ressources/icons/minus_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minus_zoom_cam_button.setIcon(icon13)
        self.minus_zoom_cam_button.setIconSize(QSize(40, 40))

        self.horizontalLayout_5.addWidget(self.minus_zoom_cam_button)

        self.full_screen_cam_button = QPushButton(self.button_search_cam_widget)
        self.full_screen_cam_button.setObjectName(u"full_screen_cam_button")
        self.full_screen_cam_button.setMaximumSize(QSize(100, 100))
        icon14 = QIcon()
        icon14.addFile(u":/icons/ressources/icons/maximize_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.full_screen_cam_button.setIcon(icon14)
        self.full_screen_cam_button.setIconSize(QSize(40, 40))

        self.horizontalLayout_5.addWidget(self.full_screen_cam_button)

        self.disconnect_cam_button = QPushButton(self.button_search_cam_widget)
        self.disconnect_cam_button.setObjectName(u"disconnect_cam_button")
        self.disconnect_cam_button.setMaximumSize(QSize(100, 100))
        icon15 = QIcon()
        icon15.addFile(u":/icons/ressources/icons/disconnect_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.disconnect_cam_button.setIcon(icon15)
        self.disconnect_cam_button.setIconSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.disconnect_cam_button)


        self.verticalLayout_5.addWidget(self.button_search_cam_widget)

        self.main_frame.addWidget(self.cam_page)
        self.qlc_page = QWidget()
        self.qlc_page.setObjectName(u"qlc_page")
        self.verticalLayout_6 = QVBoxLayout(self.qlc_page)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.qlc_form_layout = QFormLayout()
        self.qlc_form_layout.setObjectName(u"qlc_form_layout")
        self.qlc_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.qlc_form_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.path_qlc_file_label = QLabel(self.qlc_page)
        self.path_qlc_file_label.setObjectName(u"path_qlc_file_label")

        self.qlc_form_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.path_qlc_file_label)

        self.path_choose_qlc_file_label = QLabel(self.qlc_page)
        self.path_choose_qlc_file_label.setObjectName(u"path_choose_qlc_file_label")

        self.qlc_form_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.path_choose_qlc_file_label)

        self.choose_qlc_file_label = QLabel(self.qlc_page)
        self.choose_qlc_file_label.setObjectName(u"choose_qlc_file_label")

        self.qlc_form_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.choose_qlc_file_label)

        self.choose_qlc_file_button = QPushButton(self.qlc_page)
        self.choose_qlc_file_button.setObjectName(u"choose_qlc_file_button")
        self.choose_qlc_file_button.setMinimumSize(QSize(100, 100))
        self.choose_qlc_file_button.setMaximumSize(QSize(100, 16777215))
        icon16 = QIcon()
        icon16.addFile(u":/icons/ressources/icons/file-plus_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.choose_qlc_file_button.setIcon(icon16)
        self.choose_qlc_file_button.setIconSize(QSize(40, 40))

        self.qlc_form_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.choose_qlc_file_button)


        self.verticalLayout_6.addLayout(self.qlc_form_layout)

        self.run_qlc_button_widget = QWidget(self.qlc_page)
        self.run_qlc_button_widget.setObjectName(u"run_qlc_button_widget")
        self.horizontalLayout_17 = QHBoxLayout(self.run_qlc_button_widget)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.run_qlc_button = QPushButton(self.run_qlc_button_widget)
        self.run_qlc_button.setObjectName(u"run_qlc_button")
        self.run_qlc_button.setMinimumSize(QSize(200, 200))
        self.run_qlc_button.setMaximumSize(QSize(200, 16777215))
        self.run_qlc_button.setIcon(icon8)
        self.run_qlc_button.setIconSize(QSize(100, 100))

        self.horizontalLayout_17.addWidget(self.run_qlc_button)


        self.verticalLayout_6.addWidget(self.run_qlc_button_widget)

        self.main_frame.addWidget(self.qlc_page)
        self.setup_page = QWidget()
        self.setup_page.setObjectName(u"setup_page")
        self.setup_page.setStyleSheet(u"QLabel{\n"
"	font-size: 20px;\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QLineEdit{\n"
"	font-size: 20px;\n"
"	font-weight: bold;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.setup_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.screen_size_layout = QFormLayout()
        self.screen_size_layout.setObjectName(u"screen_size_layout")
        self.screen_size_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.screen_size_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.width_screen_label = QLabel(self.setup_page)
        self.width_screen_label.setObjectName(u"width_screen_label")
        self.width_screen_label.setEnabled(True)
        self.width_screen_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.screen_size_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.width_screen_label)

        self.width_screen_line_edit = QLineEdit(self.setup_page)
        self.width_screen_line_edit.setObjectName(u"width_screen_line_edit")

        self.screen_size_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.width_screen_line_edit)

        self.height_screen_label = QLabel(self.setup_page)
        self.height_screen_label.setObjectName(u"height_screen_label")
        self.height_screen_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.screen_size_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.height_screen_label)

        self.height_screen_line_edit = QLineEdit(self.setup_page)
        self.height_screen_line_edit.setObjectName(u"height_screen_line_edit")

        self.screen_size_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.height_screen_line_edit)


        self.verticalLayout.addLayout(self.screen_size_layout)

        self.setup_line_1 = QFrame(self.setup_page)
        self.setup_line_1.setObjectName(u"setup_line_1")
        self.setup_line_1.setFrameShape(QFrame.Shape.HLine)
        self.setup_line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.setup_line_1)

        self.adress_ip_layout = QFormLayout()
        self.adress_ip_layout.setObjectName(u"adress_ip_layout")
        self.adress_ip_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.adress_ip_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.adress_ip_label = QLabel(self.setup_page)
        self.adress_ip_label.setObjectName(u"adress_ip_label")
        self.adress_ip_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.adress_ip_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.adress_ip_label)

        self.adress_ip_line_edit = QLineEdit(self.setup_page)
        self.adress_ip_line_edit.setObjectName(u"adress_ip_line_edit")

        self.adress_ip_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.adress_ip_line_edit)

        self.adress_ip_artnet = QLabel(self.setup_page)
        self.adress_ip_artnet.setObjectName(u"adress_ip_artnet")
        self.adress_ip_artnet.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.adress_ip_artnet.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.adress_ip_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.adress_ip_artnet)

        self.adress_ip_artnet_line_edit = QLineEdit(self.setup_page)
        self.adress_ip_artnet_line_edit.setObjectName(u"adress_ip_artnet_line_edit")

        self.adress_ip_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.adress_ip_artnet_line_edit)


        self.verticalLayout.addLayout(self.adress_ip_layout)

        self.setup_line_2 = QFrame(self.setup_page)
        self.setup_line_2.setObjectName(u"setup_line_2")
        self.setup_line_2.setFrameShape(QFrame.Shape.HLine)
        self.setup_line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.setup_line_2)

        self.setings_cam_layout = QFormLayout()
        self.setings_cam_layout.setObjectName(u"setings_cam_layout")
        self.setings_cam_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.setings_cam_layout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.adress_ip_cam_line_edit = QLineEdit(self.setup_page)
        self.adress_ip_cam_line_edit.setObjectName(u"adress_ip_cam_line_edit")

        self.setings_cam_layout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.adress_ip_cam_line_edit)

        self.adress_ip_cam_label = QLabel(self.setup_page)
        self.adress_ip_cam_label.setObjectName(u"adress_ip_cam_label")

        self.setings_cam_layout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.adress_ip_cam_label)

        self.port_cam_label = QLabel(self.setup_page)
        self.port_cam_label.setObjectName(u"port_cam_label")

        self.setings_cam_layout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.port_cam_label)

        self.user_cam_label = QLabel(self.setup_page)
        self.user_cam_label.setObjectName(u"user_cam_label")

        self.setings_cam_layout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.user_cam_label)

        self.port_cam_line_edit = QLineEdit(self.setup_page)
        self.port_cam_line_edit.setObjectName(u"port_cam_line_edit")

        self.setings_cam_layout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.port_cam_line_edit)

        self.user_cam_line_edit = QLineEdit(self.setup_page)
        self.user_cam_line_edit.setObjectName(u"user_cam_line_edit")

        self.setings_cam_layout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.user_cam_line_edit)

        self.password_cam_label = QLabel(self.setup_page)
        self.password_cam_label.setObjectName(u"password_cam_label")

        self.setings_cam_layout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.password_cam_label)

        self.password_cam_line_edit = QLineEdit(self.setup_page)
        self.password_cam_line_edit.setObjectName(u"password_cam_line_edit")

        self.setings_cam_layout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.password_cam_line_edit)


        self.verticalLayout.addLayout(self.setings_cam_layout)

        self.setup_line_4 = QFrame(self.setup_page)
        self.setup_line_4.setObjectName(u"setup_line_4")
        self.setup_line_4.setFrameShape(QFrame.Shape.HLine)
        self.setup_line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.setup_line_4)

        self.plan_layout = QGridLayout()
        self.plan_layout.setObjectName(u"plan_layout")
        self.plan_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.plan_layout.setContentsMargins(0, -1, 0, -1)
        self.plan_label = QLabel(self.setup_page)
        self.plan_label.setObjectName(u"plan_label")
        self.plan_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.plan_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.plan_layout.addWidget(self.plan_label, 0, 0, 1, 1)

        self.plan_charge_button = QPushButton(self.setup_page)
        self.plan_charge_button.setObjectName(u"plan_charge_button")
        self.plan_charge_button.setMinimumSize(QSize(100, 100))
        self.plan_charge_button.setMaximumSize(QSize(100, 16777215))
        self.plan_charge_button.setStyleSheet(u"")
        icon17 = QIcon()
        icon17.addFile(u":/icons/ressources/icons/folder-plus_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.plan_charge_button.setIcon(icon17)
        self.plan_charge_button.setIconSize(QSize(30, 30))

        self.plan_layout.addWidget(self.plan_charge_button, 0, 1, 1, 1)

        self.plan_delete_button = QPushButton(self.setup_page)
        self.plan_delete_button.setObjectName(u"plan_delete_button")
        self.plan_delete_button.setMinimumSize(QSize(100, 100))
        self.plan_delete_button.setMaximumSize(QSize(100, 16777215))
        self.plan_delete_button.setStyleSheet(u"")
        icon18 = QIcon()
        icon18.addFile(u":/icons/ressources/icons/folder-minus_red.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.plan_delete_button.setIcon(icon18)
        self.plan_delete_button.setIconSize(QSize(30, 30))

        self.plan_layout.addWidget(self.plan_delete_button, 0, 2, 1, 1)

        self.background_img_label = QLabel(self.setup_page)
        self.background_img_label.setObjectName(u"background_img_label")
        self.background_img_label.setMaximumSize(QSize(200, 16777215))
        self.background_img_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.plan_layout.addWidget(self.background_img_label, 1, 0, 1, 1)

        self.background_img_choose_button = QPushButton(self.setup_page)
        self.background_img_choose_button.setObjectName(u"background_img_choose_button")
        self.background_img_choose_button.setMinimumSize(QSize(100, 100))
        self.background_img_choose_button.setMaximumSize(QSize(100, 16777215))
        self.background_img_choose_button.setStyleSheet(u"")
        self.background_img_choose_button.setIcon(icon16)
        self.background_img_choose_button.setIconSize(QSize(30, 30))

        self.plan_layout.addWidget(self.background_img_choose_button, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.plan_layout)

        self.setup_line_3 = QFrame(self.setup_page)
        self.setup_line_3.setObjectName(u"setup_line_3")
        self.setup_line_3.setFrameShape(QFrame.Shape.HLine)
        self.setup_line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.setup_line_3)

        self.button_box_setup = QWidget(self.setup_page)
        self.button_box_setup.setObjectName(u"button_box_setup")
        self.horizontalLayout_6 = QHBoxLayout(self.button_box_setup)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.reset_setup_button = QPushButton(self.button_box_setup)
        self.reset_setup_button.setObjectName(u"reset_setup_button")
        self.reset_setup_button.setMinimumSize(QSize(0, 100))
        self.reset_setup_button.setMaximumSize(QSize(100, 16777215))
        self.reset_setup_button.setStyleSheet(u"")
        self.reset_setup_button.setIcon(icon6)
        self.reset_setup_button.setIconSize(QSize(30, 30))

        self.horizontalLayout_6.addWidget(self.reset_setup_button)

        self.save_setup_button = QPushButton(self.button_box_setup)
        self.save_setup_button.setObjectName(u"save_setup_button")
        self.save_setup_button.setMinimumSize(QSize(0, 100))
        self.save_setup_button.setMaximumSize(QSize(100, 16777215))
        self.save_setup_button.setStyleSheet(u"")
        self.save_setup_button.setIcon(icon10)
        self.save_setup_button.setIconSize(QSize(30, 30))

        self.horizontalLayout_6.addWidget(self.save_setup_button)


        self.verticalLayout.addWidget(self.button_box_setup)

        self.main_frame.addWidget(self.setup_page)

        self.horizontalLayout_2.addWidget(self.main_frame)


        self.verticalLayout_2.addWidget(self.main_bar)

        self.status_bar = QWidget(self.centralwidget)
        self.status_bar.setObjectName(u"status_bar")
        self.status_bar.setMaximumSize(QSize(16777215, 20))
        self.horizontalLayout = QHBoxLayout(self.status_bar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.log = QLabel(self.status_bar)
        self.log.setObjectName(u"log")

        self.horizontalLayout.addWidget(self.log)

        self.time_label = QLabel(self.status_bar)
        self.time_label.setObjectName(u"time_label")
        self.time_label.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout.addWidget(self.time_label)


        self.verticalLayout_2.addWidget(self.status_bar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.main_frame.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.plan_button.setText(QCoreApplication.translate("MainWindow", u"Plans", None))
        self.qlc_button.setText(QCoreApplication.translate("MainWindow", u"QLC", None))
        self.setup_button.setText(QCoreApplication.translate("MainWindow", u"Parametres", None))
        self.home_button.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.cam_button.setText(QCoreApplication.translate("MainWindow", u"Cam", None))
        self.measurement_button.setText(QCoreApplication.translate("MainWindow", u"Mesures", None))
        self.background_image.setText("")
        self.restart_button.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.shutdown_button.setText(QCoreApplication.translate("MainWindow", u"Shutdown", None))
        self.neutral_label.setText(QCoreApplication.translate("MainWindow", u"Neutre", None))
        self.phase_1_label.setText(QCoreApplication.translate("MainWindow", u"Phase 1", None))
        self.phase_2_label.setText(QCoreApplication.translate("MainWindow", u"Phase 2", None))
        self.phase_3_label.setText(QCoreApplication.translate("MainWindow", u"Phase 3", None))
        self.neutral_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.phase_1_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.phase_2_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.phase_3_value_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.graph_label.setText(QCoreApplication.translate("MainWindow", u"Graphique", None))
        self.measurement_start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.measurement_stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.measurement_reset_button.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.measurement_savegraph_button.setText(QCoreApplication.translate("MainWindow", u"Save CSV", None))
        self.flux_video_label.setText("")
        self.connect_cam_button.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.plus_zoom_cam_button.setText("")
        self.minus_zoom_cam_button.setText("")
        self.full_screen_cam_button.setText("")
        self.disconnect_cam_button.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.path_qlc_file_label.setText(QCoreApplication.translate("MainWindow", u"Chemin fichier :", None))
        self.path_choose_qlc_file_label.setText("")
        self.choose_qlc_file_label.setText(QCoreApplication.translate("MainWindow", u"Choisir fichier :", None))
        self.choose_qlc_file_button.setText("")
        self.run_qlc_button.setText("")
        self.width_screen_label.setText(QCoreApplication.translate("MainWindow", u"Largeure \u00e9cran :", None))
        self.height_screen_label.setText(QCoreApplication.translate("MainWindow", u"Hauteur \u00e9cran :", None))
        self.adress_ip_label.setText(QCoreApplication.translate("MainWindow", u"Adresse ip :", None))
        self.adress_ip_artnet.setText(QCoreApplication.translate("MainWindow", u"Adresse Artnet :", None))
        self.adress_ip_cam_label.setText(QCoreApplication.translate("MainWindow", u"Adresse ip Cam :", None))
        self.port_cam_label.setText(QCoreApplication.translate("MainWindow", u"Port Cam :", None))
        self.user_cam_label.setText(QCoreApplication.translate("MainWindow", u"User :", None))
        self.password_cam_label.setText(QCoreApplication.translate("MainWindow", u"Password :", None))
        self.plan_label.setText(QCoreApplication.translate("MainWindow", u"Plans :", None))
        self.plan_charge_button.setText(QCoreApplication.translate("MainWindow", u"Charger", None))
        self.plan_delete_button.setText(QCoreApplication.translate("MainWindow", u"Supprimer", None))
        self.background_img_label.setText(QCoreApplication.translate("MainWindow", u"Image background :", None))
        self.background_img_choose_button.setText(QCoreApplication.translate("MainWindow", u"Choisir", None))
        self.reset_setup_button.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.save_setup_button.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.log.setText(QCoreApplication.translate("MainWindow", u"Log", None))
        self.time_label.setText(QCoreApplication.translate("MainWindow", u"Time", None))
    # retranslateUi

