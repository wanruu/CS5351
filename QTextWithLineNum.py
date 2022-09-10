# coding: utf-8
# @FileName: textPlainWithLineNum.py

from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtWidgets import QWidget, QTextEdit, QPlainTextEdit, QApplication
from PySide6.QtGui import QColor, QPainter, QTextFormat, QKeyEvent, QWheelEvent, QMouseEvent, QTextCursor

import sys


class QTextEditWithLineNum(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLineWrapMode(QTextEdit.NoWrap)  # 不自动换行
        self.lineNumberArea = LineNumPaint(self)
        self.document().blockCountChanged.connect(self.update_line_num_width)
        self.document().cursorPositionChanged.connect(self.highlightCurrentLine)  # 高亮当前行
        self.verticalScrollBar().sliderMoved.connect(self.scroll_event)  # 滚动条移动更新行号
        self.update_line_num_width()

    def wheelEvent(self, d: QWheelEvent) -> None:
        self.scroll_event(d)
        super().wheelEvent(d)

    def scroll_event(self, event: QWheelEvent = None):
        self.lineNumberArea.update()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        super().keyPressEvent(e)
        self.lineNumberArea.update()

    def mousePressEvent(self, e: 'QMouseEvent') -> None:
        super().mousePressEvent(e)
        self.update()
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        block_count = self.document().blockCount()
        max_value = max(1, block_count)
        d_count = len(str(max_value))
        _width = self.fontMetrics().maxWidth() * d_count
        return _width

    def update_line_num_width(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.blue).lighter(190)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        cursor = QTextCursor(self.document())
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)
        line_height = self.fontMetrics().lineSpacing()  # 包含行间距的行高

        block_number = self.cursorForPosition(QPoint(0, int(line_height / 2))).blockNumber()
        first_visible_block = self.document().findBlock(block_number)
        blockNumber = block_number
        cursor.setPosition(self.cursorForPosition(QPoint(0, int(line_height / 2))).position())
        rect = self.cursorRect()
        scroll_compensation = rect.y() - int(rect.y() / line_height) * line_height
        top = scroll_compensation
        last_block_number = self.cursorForPosition(QPoint(0, self.height() - 1)).blockNumber()

        height = self.fontMetrics().height()
        block = first_visible_block
        while block.isValid() and (top <= event.rect().bottom()) and blockNumber <= last_block_number:
            # cur_line_count = block.lineCount()
            if block.isVisible():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                # print((0, top, self.lineNumberArea.width(), height), number)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)
            block = block.next()
            top = top + line_height
            blockNumber += 1


class LineNumPaint(QWidget):
    def __init__(self, q_edit):
        super().__init__(q_edit)
        self.q_edit_line_num = q_edit

    def sizeHint(self):
        return QSize(self.q_edit.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.q_edit_line_num.lineNumberAreaPaintEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    codeEditor = QTextEditWithLineNum()
    codeEditor.setWindowTitle("带行号的编辑器")
    # codeEditor.setGeometry(100, 100, 800, 600)
    codeEditor.show()
    app.exec()
