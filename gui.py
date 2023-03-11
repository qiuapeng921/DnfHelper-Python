import _thread
import time

import xcgui._xcgui as gui
from xcgui import XApp
from xcgui import XWindow, XButton, XEdit, XShapeText

from common import globle, logger
from common import helper
from driver import init_driver
from game import mem, init

svgIcon = '<svg t="1674984352573" class="icon" viewBox="0 0 1024 1024" version="1.1" ' \
          'xmlns="http://www.w3.org/2000/svg" p-id="10315" width="16" height="16"><path d="M901.957085 ' \
          '349.126786c-60.072164-87.975001-153.76426-100.09183-187.170868-101.49977-79.698013-8.106329-155.59885 ' \
          '46.931378-196.0025 46.931377-40.40365 0-102.779718-45.822091-168.86763-44.627473-86.908379 ' \
          '1.279947-166.990375 50.515229-211.788509 128.421315-90.32157 156.665472-23.12437 388.762468 64.850631 ' \
          '515.818508 43.048873 62.248073 94.332069 132.133161 161.6146 129.615933 64.850631-2.559893 ' \
          '89.425607-41.982251 167.673013-41.982251 78.418066 0 100.433149 41.982251 169.03829 40.702304 ' \
          '69.799758-1.279947 114.000583-63.400025 156.665473-125.818758 49.405941-72.188992 69.714429-141.98875 ' \
          '70.909045-145.572601-1.578601-0.725303-135.973001-52.221824-137.380942-207.095371-1.279947-129.573268 ' \
          '105.68093-191.778676 110.502062-194.893213zM715.852839 0.042665c-51.496521 2.133244-113.829924 ' \
          '34.302571-150.820382 77.479438-33.107954 38.3984-58.706887 99.622516-50.899213 158.414733 57.51227 ' \
          '4.479813 112.720637-29.182784 148.473814-72.530311 35.710512-43.176868 59.816174-103.377026 ' \
          '53.245781-163.36386z" fill="#1afa29" opacity=".65" p-id="10316"></path></svg>'

version = '1.0.0'


class AppWindow(XWindow):
    def __init__(self):
        super(AppWindow, self).__init__(0, 0, 300, 400, "情歌 √ 当前时间 {}".format(helper.get_now_date()), 0,
                                        gui.window_style_modal)
        _thread.start_new_thread(self.title_time, ())

        # 设置窗口图标
        self.setIcon(gui.XImage.loadSvgString(svgIcon))
        # 禁止改变大小
        self.enableDragBorder(False)
        # 设置边框
        self.setBorderSize(0, 30, 0, 0)

        XShapeText(0, 35, 60, 30, "卡号:", self)
        self.card_edit = XEdit(35, 35, 200, 30, self)
        self.card_edit.setText("19930921")
        self.card_edit.enablePassword(True)
        self.card_edit.setTextAlign(gui.edit_textAlign_flag_center)

        self.activation_but = XButton(244, 35, 50, 30, "激活", self)
        self.activation_but.regEvent(gui.XE_BNCLICK, self.activation)

        self.edit_content = XEdit(1, 70, 300, 310, self)
        self.edit_content.enableMultiLine(True)
        self.edit_content.enableReadOnly(True)
        self.edit_content.autoScroll()
        self.edit_content.showSBarV(True)
        self.edit_content.showSBarH(True)
        self.edit_content.scrollBottom()

        self.run_time_label = XShapeText(1, 375, 60, 30, "运行时间:", self)
        self.run_time_value = XShapeText(56, 375, 60, 30, "00:00:00", self)
        _thread.start_new_thread(self.app_run_time, ())

        self.version_label = XShapeText(220, 375, 60, 30, "版本号:", self)
        self.version_value = XShapeText(260, 375, 60, 30, version, self)

    def activation(self, event, userdata) -> bool:
        process_id = helper.get_process_id_by_name("DNF.exe")
        if process_id == 0:
            helper.message_box("请打开dnf后运行")
            return False
        card_edit_val = self.card_edit.getText()
        if card_edit_val != "19930921":
            helper.message_box("卡密错误")
        self.activation_but.enable(False)
        mem.set_process_id(process_id)
        init.init_empty_addr()
        init.hotkey()
        self.add_content("加载成功-欢迎使用")
        self.add_content("当前时间：".format(helper.get_now_date()))

        return True

    def app_run_time(self):
        while 1:
            time.sleep(1)
            self.run_time_value.setText(helper.get_app_run_time())
            self.run_time_value.redraw()

    def title_time(self):
        while 1:
            time.sleep(1)
            self.setTitle("情歌 √ 当前时间 {}".format(helper.get_now_date()))
            self.redraw()

    def add_content(self, msg):
        self.edit_content.addTextUser("{}\n".format(msg))
        self.redraw()


if __name__ == '__main__':
    try:
        init_driver()
        globle.cmd = "gui"
        app = XApp()
        win = AppWindow()
        globle.win_app = win
        logger.info("驱动加载成功")
        win.showWindow()
        app.run()
        app.exit()
    except Exception as err:
        import sys
        import traceback

        except_type, _, except_traceback = sys.exc_info()
        print(except_type)
        print(err.args)
        print(except_traceback)
        print('-----------')
        for i in traceback.extract_tb(except_traceback):
            print(i)
