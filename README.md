# JunianFM

基于PlayerFM API的远程操控树莓派的Podcast控制方案
Podcast control solution for remote monitoring of Raspberry Pi based on PlayerFM API.

---

## 项目介绍：

一个基于 Flask 对树莓派 vlc 的播放状态进行控制，并通过 快捷指令（Workflow）进行可视化管理的控制方案。

## 项目实现：

- [x] 自定义 Podcast 订阅
- [x] 播放、暂停、停止等基本功能
- [X] 快进30s或后退15s
- [x] 音量调节、速率调节
- [ ] 节目选择时的翻页功能

## 如何部署：

#### 安装相关依赖并运行
```bash
pip install -r requirements.txt
gunicorn  --reload -c gunicorn.conf index:app;
```

#### 开机自启
```bash
sudo vim /etc/rc.local
```
在 exit 0 之前加入
```bash
su pi -c "exec 存放路径 + /flaskss.sh"
```
~我也不知道为啥，我的 root 用户没法启动 flask 服务，必须得改成 pi 用户才能正常运行~

#### 内网穿透（可选）
通过 frp 等服务将树莓派的 127.0.0.1:6654 端口映射到外网服务器

#### 安装捷径

[安装捷径链接](https://www.icloud.com/shortcuts/e466dc491ec341afa59641f73953614e)

如果实现了上一步就在向导步骤中填入指定的域名，否则就填入 树莓派ip : 6654

#### 最后，

enjoy it~

