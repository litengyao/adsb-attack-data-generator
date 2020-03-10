# 针对ADS-B攻击数据的安全分析与建模

<kbd>作者：李腾耀</kbd>
<kbd>版本：ver-1.0</kbd>

> 本实验代码开发周期：2018/09/10-2018/09/14,2018/09/24-2018/09/30

## 主要功能

主要用于实现对ADS-B攻击数据的分析和建模，完成对ADS-B攻击数据的有效构造。按照《针对ADS-B攻击数据的安全分析与建模》的基本思路进行设计和实现，目前已包含针对13种不同的攻击样式进行了建模实现和数据验证。

## 运行基本要求

- 软件要求
  - Anaconda3 64bit 4.3.x
  - opensky_api(Internet support)
- 硬件需求
  - Core i5-4590
  - 内存4GB
- 其他
  - 互联网连接（可选）【如果需要在线下载数据，则必须要能够连接到http://www.opensky-network.org】

## 模块主要功能

- scripts
  - main.py  实验脚本的入口代码，描述了实验的主要分析流程
- attack 攻击样式设计的核心模块
  - attack 针对ADS-B数据进行攻击样式设计的基类
  - dos_attack DoS攻击
  - ghost_attack 虚假节点注入攻击
  - replay_attack 重放攻击
  - tampering_attack 篡改攻击
- attack_choice 遭受攻击飞行器的选择和攻击数据混合的控制策略
- basic_processor 数据清洗和初步可视化
- data_collector 数据在线采集
- data_io ADS-B数据的磁盘I/O操作

## 关于运行本实验的几点说明

攻击样式可以在继承基类attack的情况下进行灵活地扩充

## 联系我

如果在使用本实验代码过程中，遇到任何问题请联系我：totopcoder@gmail.com