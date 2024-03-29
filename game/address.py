RwKbAddr = 0  # 人物基址
BuffKbAddr = 0  # buff地址
NcBhKbAddr = 0  # 内存汇编
PtGgKbAddr = 0  # 普通公告
JnKbAddr = 0  # 技能Call
GtKbAddr = 0  # 过图Call
CoolDownKbAddr = 0  # 冷却判断call

RwAddr = 0x14C1B61C0  # 新人物基址
RwAddr2 = 0x14B847CB8  # 人物基址B
BbJzAddr = 0x14B8D8458  # 背包基址
FbBhAddr = 0x14B8BD970  # 副本编号
RWCallAddr = 0x144C55B50  # 人物CALL
JSDjAddr = 0x14B8BD9E0  # 角色等级
JwCallAddr = 0x144A55D20  # 聚物CALL
JxWpAddr = 0x00F8A8  # 脚下物品
DmWpAddr = 0x002B00  # 地面物品
JwXyAddr = 0x00FD7C  # 聚物校验
PFAddr = 0x14B8D7190  # 评分基址
CEPfAddr = 0x000088  # 评分偏移
FpAddr = 0x14B8D5030  # 翻牌基址
HChengCallAddr = 0x14584C260  # 回城CALL
SNBBAddr = 0x14B8D84B0  # 司南背包
YrBbAddr = 0x14B8D84A8  # 玉荣背包
BxrBbAddr = 0x14B8D84A8  # 辟邪玉背包
SnAddCallAddr = 0x141D8E900  # 司南添加CALL
SnJtRcxAddr = 0x14B885FC8  # 司南进图_Rcx
SnJtCallAddr = 0x141D71C60  # 司南进图CALL
SnAddRcxAddr = 0x14540F110  # 取司南添加RCX
YrlPyAddr = 0x000600  # 玉荣力偏移
JsYrlAddr = 0x005398  # 角色玉荣力
DtPyAddr = 0x000168  # 地图偏移
DtKs2 = 0x0001B8  # 地图开始2
DtJs2 = 0x0001C0  # 地图结束2
DtMcAddr = 0x000418  # 地图名称
MxPyAddr = 0x000128  # 门型偏移
GouHuoAddr = 0x001E28  # 篝火判断
JzCtAddr = 0x00087C  # 建筑穿透
DtCtAddr = 0x000878  # 地图穿透
DzIDAddr = 0x0042FC  # 动作ID
FxIdAddr = 0x0000E8  # 方向ID
ZbStPyAddr = 0x003808  # 坐标顺图
DqFzAddr = 0x14C20B368  # 当前负重
ZdFzAddr = 0x002D78  # 最大负重
ZlCallAddr = 0x144898470  # 整理背包CALL
SJAddr = 0x20A050  # 时间基址
FJBHAddr = 0x14B8D8440  # 房间编号
GGCsAddr = 0x14C1B7508  # 公告参数
GGCallAddr = 0x144D21700  # 公告CALL
CreateCallAddr = 0x144722AD0  # 创建CALL
PutOnCallAddr = 0x144A68A90  # 穿上CALL
TmCallAddr = 0x145B410F0  # 透明CALL
DyBuffCall = 0x144C8CF10  # 调用BUFFCALL
JNCallAddr = 0x1447BD1A0  # 技能CALL
SqNcCallAddr = 0x143A0C930  # 申请内存
XrNcCallAddr = 0x144C90BC0  # 写入内存
PyCall1Addr = 0x143A37760  # 漂移CALL
PyCall2Addr = 0x145C006D0  # 漂移CALL2
YXZTAddr = 0x14B41FFD0  # 游戏状态
TaskAddr = 0x14B8D8540  # 任务基址
JsCallAddr = 0x1440AFA40  # 接受CALL
TgCallAddr = 0x143E4BC40  # 跳过CALL
WcCallAddr = 0x1440B0050  # 完成CALL
TjCallAddr = 0x1440AFB30  # 提交CALL
JSPtrAddr = 0x14B8D81C0  # 角色指针
DHAddr = 0x14B710C58  # 对话基址
DHAddrB = 0x14C209B78  # 对话基址B
EscDHAddr = 0x14B710C70  # Esc对话基址
MaxPlAddr = 0x14C1B6124  # 最大疲劳
CutPlAddr = 0x14C1B60DC  # 当前疲劳
AjAddr = 0x14C674440  # 按键基址
QyParamAddr = 0x14C20F060  # 区域参数
CzDqyAddr = 0x14B8956AC  # 城镇大区域
CzXqyAddr = 0x14B8956B0  # 城镇小区域
QyCallAddr = 0x145A665C0  # 区域CALL
QyPyAddr = 0x0A9FA8  # 区域偏移
CzSyRdxAddr = 0x14B8A9408  # 城镇瞬移_Rdx
CzSyCallAddr = 0x145AAD370  # 城镇瞬移CALL
HBCallAddr = 0x13FDC0000  # 汇编CALL
TranslateMessage = 0x14775DCC0  # TranslateMessage
GameTimeGetTime = 0x14775E0F8  # GameTimeGetTime
XzJsCallAddr = 0x1404F6F30  # 选择角色CALL
FhJsCallAddr = 0x1444C5140  # 返回角色CALL
BUffMemRcxAddr = 0x14B8D82F0  # BUFF内存_RCX
BUffMemCallAddr = 0x145B2F0D0  # BUFF内存CALL
GtCallAddr = 0x143BE58B0  # 过图CALL
XTuCallAddr = 0x145AA6150  # 选图CALL
JTuCallAddr = 0x145AE6D90  # 进图CALL
WpYdCallAddr = 0x14488EB10  # 物品移动CALL
BpCallAddr = 0x143FF12E0  # 奔跑CALL
FbAddr = 0x14C20FC70  # 发包基址
HcCallAddr = 0x145B123C0  # 缓冲CALL
FbCallAddr = 0x145B130B0  # 发包CALL
JmB1CallAddr = 0x145B13220  # 加密包CALL
JmB2CallAddr = 0x145B135A0  # 加密包CALL2
JmB3CallAddr = 0x145B13240  # 加密包CALL4
JmB4CallAddr = 0x145B13260  # 加密包CALL8
SyPyAddr = 0x001D8C  # 索引偏移
KgPyAddr = 0x000890  # 宽高偏移
SzPyAddr = 0x0008B0  # 数组偏移
StPyAddr = 0x000718  # 顺图偏移
CutRoomXAddr = 0x001C98  # 当前房间X
CutRoomYAddr = 0x001C9C  # 当前房间Y
BOSSRoomXAddr = 0x001D98  # BOSS房间X
BOSSRoomYAddr = 0x001D9C  # BOSS房间Y
FbSqAddr = 0x000134  # 发包拾取
RwMwAddr = 0x011DAC  # 人物名望
WpJyLxAddr = 0x0000A8  # 物品交易类型
LxPyAddr = 0x000134  # 类型偏移
FxPyAddr = 0x000148  # 方向偏移
ZyPyAddr = 0x000E88  # 阵营偏移
DmPyAddr = 0x000868  # 代码偏移
McPyAddr = 0x000870  # 名称偏移
GwXlAddr = 0x004F08  # 怪物血量
DqZbAddr = 0x000328  # 读取坐标
WplAddr = 0x00FCF0  # 物品栏
WplPyAddr = 0x0000A8  # 物品栏偏移
WpMcAddr = 0x000040  # 物品名称
ZbPjAddr = 0x0002B8  # 装备品级
SfKmAddr = 0x00027C  # 是否开门
YjRwStartAddr = 0x000010  # 已接任务首地址
YjRwEndAddr = 0x000018  # 已接任务尾地址
QbRwStartAddr = 0x0000A8  # 全部任务首地址
QbRwEndAddr = 0x0000B0  # 全部任务尾地址
RwDxAddr = 0x000028  # 任务大小
RwLxAddr = 0x000218  # 任务类型
RwTjAddr = 0x0004B0  # 任务条件
RwDjAddr = 0x000328  # 任务等级
RwFbAddr = 0x000468  # 任务副本
BpPyAddr1 = 0x001208  # 奔跑偏移_1
BpPyAddr2 = 0x0011F0  # 奔跑偏移_2
JnSwAddr = 0x144A11791  # 技能三无
LqCallJudgeAddr = 0x144C421B0  # 冷却判断CALL
CdResetCallAddr = 0x144AA56F0  # CD重置CALL
JnlAddr = 0x00FC68  # 技能栏
JnlPyAddr = 0x000090  # 技能栏偏移