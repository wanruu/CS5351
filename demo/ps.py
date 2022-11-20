import copy

import cv2 as cv
from PySide2 import QtGui
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog, QWidget
from qtconsole.qt import QtCore

import Seam_
import sift
import quanjingtu
import HOG
from dehaze import *
from dehaze import _getV1_


class Window:

    def __init__(self):
        self.path = "photo_box/haze.jpg"
        self.P_ori = cv.imread(self.path, cv.IMREAD_UNCHANGED)
        self.P_HLS = 0
        self.P_opt = 0
        self.P_tmp = 0
        self.P_HLS_tmp = 0
        self.P_shape = self.P_ori.shape
        self.P_dtype = self.P_ori.dtype
        self.H = 0
        self.S = 0
        self.V = 0
        self.temH = 0
        self.temS = 0
        self.temV = 0
        self._B_ = 0
        self._G_ = 0
        self._R_ = 0
        self.Alpha = 1
        self.Beta = 0
        self.P_TMP_STATE = 'null'
        # 加载UI定义

        qfile_stats = QFile("untitled.ui")
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        self.ui = QUiLoader().load(qfile_stats)
        self.init_show_photo()

        # 功能区
        self.ui.GAUSSIAN.clicked.connect(self.F_GAUSSIAN)
        self.ui.BLUR.clicked.connect(self.F_BLUR)
        self.ui.MEDIANBLUR.clicked.connect(self.F_MEDIANBLUR)
        self.ui.BILATERALFILTER.clicked.connect(self.F_BILATERALFILTER)
        self.ui.SEAM_CRAVING.clicked.connect(self.F_SEAM_CRAVING)
        self.ui.DEHAZE.clicked.connect(self.F_DEHAZE)
        self.ui.HOG.clicked.connect(self.F_HOG)
        self.ui.FILTER2D.clicked.connect(self.F_FILTER2D)
        self.ui.RGB2HLS.clicked.connect(self.F_BGR2HLS)
        self.ui.HLS2RGB.clicked.connect(self.F_HLS2BGR)
        self.ui.RGB_AND.clicked.connect(self.F_RGB_AND)
        self.ui.HSV_AND.clicked.connect(self.F_HSV_AND)
        self.ui.SAVE.clicked.connect(self.F_SAVE)
        self.ui.REFRESH.clicked.connect(self.F_REFRESH)
        self.ui.OPEN.clicked.connect(self.F_OPEN)
        self.ui.EXTEND_SHIF.clicked.connect(self.F_SIFT)
        self.ui.EXTEND_COM.clicked.connect(self.F_EXTEND_COM)

        self.ui.LIGHT.valueChanged.connect(self.F_LIGHT)
        self.ui.LIGHT_BOX.valueChanged.connect(self.F_LIGHT)
        self.ui.CONTRAST.valueChanged.connect(self.F_CONTRAST)
        self.ui.CONTRAST_BOX.valueChanged.connect(self.F_CONTRAST)
        self.ui.H__.valueChanged.connect(self.F_SATURATION_H)
        self.ui.L__.valueChanged.connect(self.F_SATURATION_L)
        self.ui.S__.valueChanged.connect(self.F_SATURATION_S)
        #

    def F_HOG(self):
        self.F_HLS2BGR()
        self.P_tmp = HOG.HOG_find_people(self.P_ori)
        self.update_photo()
        pass

    def F_RGB_AND(self):
        self.F_HLS2BGR()
        self.update_photo()

    def F_HSV_AND(self):
        # self.H, self.S, self.V = cv.split(self.P_ori)xw
        self.P_tmp = self.P_ori.astype(np.float32)
        self.P_tmp = self.P_tmp / 255.0
        self.F_BGR2HLS()
        self.temH = copy.deepcopy(self.H)
        self.temS = copy.deepcopy(self.S)
        self.temV = copy.deepcopy(self.V)
        # print(self.H, self.S, self.V)
        print(3)

    def F_BGR2HLS(self):
        if self.P_TMP_STATE == 'HLS':
            print("已经是HLS了")
            return
        # self.P_tmp = cv.cvtColor(self.P_tmp, cv.COLOR_BGR2HSV)
        self.P_TMP_STATE = 'HLS'
        self.update_photo()

    def F_HLS2BGR(self):
        if self.P_TMP_STATE == 'BGR':
            print("已经是BGR了")
            return
        # self.P_tmp = cv.cvtColor(self.P_tmp, cv.COLOR_HSV2BGR)
        self.P_TMP_STATE = 'BGR'
        self.update_photo()

    def F_GAUSSIAN(self):
        self.F_HLS2BGR()
        self.P_tmp = cv.GaussianBlur(self.P_tmp, (9, 9), 0)
        self.update_photo()

    def F_BLUR(self):
        self.F_HLS2BGR()
        self.P_tmp = cv.blur(self.P_tmp, (5, 5))
        self.update_photo()

    def F_MEDIANBLUR(self):
        self.F_HLS2BGR()
        self.P_tmp = cv.medianBlur(self.P_tmp, 5)
        self.update_photo()

    def F_BILATERALFILTER(self):
        self.F_HLS2BGR()
        self.P_tmp = cv.bilateralFilter(self.P_tmp, 13, 46, 8)
        self.update_photo()

    def F_FILTER2D(self):
        self.F_HLS2BGR()
        # kernel = np.ones((5, 5)) / 25
        kernel = np.array([[-1, -1, -1],
                           [-1, 2, -1],
                           [-1, -1, -1]])
        self.P_tmp = cv.filter2D(self.P_tmp, -1, kernel)
        self.update_photo()

    def F_LIGHT(self, beta):
        self.F_HLS2BGR()
        self.Beta = beta
        self.P_tmp = cv.convertScaleAbs(self.P_ori, alpha=self.Alpha, beta=self.Beta)
        self.update_photo()

    def F_CONTRAST(self, Alpha):
        self.F_HLS2BGR()
        print(self._B_, self._G_, self._R_)
        Alpha /= 100
        new_B_ = (self.P_ori[:, :, 0] - self._B_) * Alpha + self._B_
        new_G_ = (self.P_ori[:, :, 1] - self._G_) * Alpha + self._G_
        new_R_ = (self.P_ori[:, :, 2] - self._R_) * Alpha + self._R_

        new_B_[:][new_B_[:] > 255] = 255
        new_G_[:][new_G_[:] > 255] = 255
        new_R_[:][new_R_[:] > 255] = 255
        new_B_[:][new_B_[:] < 0] = 0
        new_G_[:][new_G_[:] < 0] = 0
        new_R_[:][new_R_[:] < 0] = 0

        print(new_B_, new_G_, new_R_)
        self.P_tmp = cv.merge([np.uint8(new_B_), np.uint8(new_G_), np.uint8(new_R_)])

        self.update_photo()

    def F_SATURATION_H(self, h_value):
        self.F_BGR2HLS()
        h_value /= 100.0
        self.P_HLS_tmp[:, :, 0] = h_value * self.P_HLS[:, :, 0]
        self.P_HLS_tmp[:, :, 0][self.P_HLS_tmp[:, :, 0] > 1] = 1
        self.update_photo()

    def F_SATURATION_L(self, l_value):
        self.F_BGR2HLS()
        l_value /= 100.0
        self.P_HLS_tmp[:, :, 1] = l_value * self.P_HLS[:, :, 1]
        self.P_HLS_tmp[:, :, 1][self.P_HLS_tmp[:, :, 1] > 1] = 1
        self.update_photo()

    def F_SATURATION_S(self, s_value):
        self.F_BGR2HLS()
        s_value /= 100.0
        print(s_value)
        self.P_HLS_tmp[:, :, 2] = s_value * self.P_HLS[:, :, 2]
        self.P_HLS_tmp[:, :, 2][self.P_HLS_tmp[:, :, 2] > 1] = 1
        self.update_photo()

    def F_DEHAZE(self, r=81, eps=0.001, w=0.95, maxV1=0.80, bGamma=False):
        self.F_HLS2BGR()
        self.P_tmp = self.P_tmp / 255.0
        Y = np.zeros(self.P_shape)
        V1, A = _getV1_(self.P_tmp, r, eps, w, maxV1)
        for k in range(3):
            Y[:, :, k] = (self.P_tmp[:, :, k] - V1) / (1 - V1 / A)
        Y = np.clip(Y, 0, 1)
        # if bGamma:
        #     Y = Y ** (np.log(0.5) / np.log(Y.mean())
        self.P_tmp = (Y * 255).astype(np.uint8)
        print(self.P_tmp)
        self.update_photo()

    def F_SEAM_CRAVING(self, A=True, len=20):
        self.F_HLS2BGR()
        img = np.array(self.P_tmp, dtype=np.float)
        print(A)
        if not A:
            for _ in range(len):
                img = Seam_.carve_row(img)
        elif A:
            for _ in range(len):
                img = Seam_.carve_col(img)

        self.P_tmp = img.astype(np.uint8)
        self.update_photo()

    def F_SIFT(self):
        shif_photo = self.open_and_show_in_P_tem_label()
        sift.sift_(self.P_ori,shif_photo)

    def F_EXTEND_COM(self):
        com_photo = self.open_and_show_in_P_tem_label()
        quanjingtu.combine(self.P_ori, com_photo)

    def init_show_photo(self):
        # self.H, self.S, self.V = cv.split(self.P_ori)
        self.P_HLS = cv.cvtColor(self.P_ori.astype(np.float32) / 255.0, cv.COLOR_BGR2HLS)
        self.P_HLS_tmp = copy.deepcopy(self.P_HLS)
        self._B_ = np.sum(self.P_ori[:, :, 0]) / (self.P_shape[0] * self.P_shape[1])
        self._G_ = np.sum(self.P_ori[:, :, 1]) / (self.P_shape[0] * self.P_shape[1])
        self._R_ = np.sum(self.P_ori[:, :, 2]) / (self.P_shape[0] * self.P_shape[1])
        self.P_opt = copy.deepcopy(self.P_ori)
        self.P_tmp = copy.deepcopy(self.P_ori)
        self.P_ori = cv.cvtColor(self.P_ori, cv.COLOR_BGR2RGB)
        show_P_ori = QtGui.QImage(self.P_ori.data,
                                  self.P_ori.shape[1],
                                  self.P_ori.shape[0],
                                  self.P_ori.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888
                                  )
        self.ui.ori_photo.setPixmap(QtGui.QPixmap(show_P_ori))
        self.ui.ori_photo.setWindowOpacity(0)

        self.P_TMP_STATE = 'BGR'

        show_P_opt = QtGui.QImage(self.P_ori.data,
                                  self.P_ori.shape[1],
                                  self.P_ori.shape[0],
                                  self.P_ori.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888
                                  )
        self.ui.opt_photo.setPixmap(QtGui.QPixmap(show_P_opt))
        self.ui.opt_photo.setWindowOpacity(0)

        self.P_ori = cv.cvtColor(self.P_ori, cv.COLOR_RGB2BGR)

    def update_photo(self):
        QApplication.processEvents()
        if self.P_TMP_STATE == 'BGR':
            self.P_opt = cv.cvtColor(self.P_tmp, cv.COLOR_BGR2RGB)
        elif self.P_TMP_STATE == 'HLS':
            self.P_opt = (cv.cvtColor(self.P_HLS_tmp, cv.COLOR_HLS2RGB) * 255).astype(np.uint8)
            # print(self.P_opt)
        show_P_opt = QtGui.QImage(self.P_opt.data,
                                  self.P_opt.shape[1],
                                  self.P_opt.shape[0],
                                  self.P_opt.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888
                                  )
        self.ui.opt_photo.setPixmap(QtGui.QPixmap(show_P_opt))

    def open_and_show_in_P_tem_label(self):
        open_img_name = QFileDialog.getOpenFileName(self.ui, 'open file',
                                                    '/Users/yunqizhao/PycharmProjects/Digital_media/photo_box')
        return cv.imread(open_img_name[0], cv.IMREAD_UNCHANGED)

    def F_OPEN(self):
        open_img_name = QFileDialog.getOpenFileName(self.ui, 'open file',
                                                    '/Users/yunqizhao/PycharmProjects/Digital_media/photo_box')
        self.P_ori = cv.imread(open_img_name[0], cv.IMREAD_UNCHANGED)
        self.init_show_photo()

    def F_SAVE(self):
        self.update_photo()
        if self.P_TMP_STATE == 'BGR':
            self.P_opt = cv.cvtColor(self.P_opt, cv.COLOR_BGR2RGB)
        elif self.P_TMP_STATE == 'HLS':
            self.P_opt = (cv.cvtColor(self.P_HLS_tmp, cv.COLOR_HLS2RGB) * 255).astype(np.uint8)
        cv.imwrite("output.jpg", self.P_opt)

    def F_REFRESH(self):
        self.P_HLS = cv.cvtColor(self.P_ori.astype(np.float32) / 255.0, cv.COLOR_BGR2HLS)
        self.P_HLS_tmp = copy.deepcopy(self.P_HLS)
        self.P_opt = copy.deepcopy(self.P_ori)
        self.P_tmp = copy.deepcopy(self.P_ori)

        self.P_TMP_STATE = 'BGR'

        show_P_opt = QtGui.QImage(self.P_ori.data,
                                  self.P_ori.shape[1],
                                  self.P_ori.shape[0],
                                  self.P_ori.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888
                                  )
        self.ui.opt_photo.setPixmap(QtGui.QPixmap(show_P_opt))
        self.ui.opt_photo.setWindowOpacity(0)

        self.update_photo()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication()
    window = Window()
    window.ui.show()
    app.exec_()



