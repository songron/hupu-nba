# hupu-nba
Live scoreboard of NBA games running in the console. NBA 文字/比分直播,命令行版本。

![HUPU-NBA](hupunba.gif)

## Features

* NBA终端直播
* NBA比赛日程
* 命令行控制，不依赖UI软件
* 支持系统：*NIX, OS X

## Dependencies

    pip install lxml

## Usage

    git clone https://github.com/ghostrong/hupu-nba.git
    cd hupu-nba
    python run.py

* MENU:

  Type the *[number]* to enter the corresponding game.

* LIVE:

  Type *m* to go back to the menu.

  Type *f* to refresh manually.

  The console will refresh automatically every 5 seconds by default.


## Acknowledgements

* 感谢[虎扑体育](http://www.hupu.com/)提供数据。
