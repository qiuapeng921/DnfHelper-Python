class FullScreen:
    switch = False

    def __init__(self):
        pass

    def Run(self, switch: bool):
        while switch:
            print(convert.GetNowDate())
            time.sleep(1)

    def SkillSwitch(self):
        """
        技能全屏
        """
        self.switch = not self.switch
        if self.switch:
            self.Run(True)
            print("技能全屏开启")
        else:
            self.switch = False
            print("技能全屏关闭")

    def Stop(self):
        self.switch = False
