#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cnoid.Base import *
from cnoid.BodyPlugin import *
from datetime import datetime as dt

#現在時刻文字列取得
tdatetime = dt.now()
tstr = tdatetime.strftime('%Y%m%d-%H%M%S')

# WorldItem取得(名前決め打ちなのがスマートではない)
world = RootItem.instance.findItem('World')

# WorldLogFile生成
worldlog = WorldLogFileItem()
worldlog.setChecked(True)
worldlog.setLogFile('/userdir/chidori_LOG/logs/cnoid-{}.log'.format(tstr))
worldlog.setRecordingFrameRate(0)

# Worldへ追加
world.addChildItem(worldlog)

