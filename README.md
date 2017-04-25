# Check_webp_advantages_for_system

Description:
============
找出android的升级包update.zip或target_files.zip的所有apk中超过指定大小的图片转换为webp后的体积瘦身．

Usage:
=========

	python StartUpdateWebp.py dir [Specifiedsize] 

	dir： 指定的目录,此目录为update.zip或target_files.zip解压后目录绝对路径．升级包中app priv-app的apk都将被转换．
	Specifiedsize： 图片大小超过Specifiedsize才转换webp，默认Specifiedsize=50，Specifiedsize单位是KB,即超过50KB图片将转换为webp。

	eg：python StartUpdateWebp.py  ~/update
	
	
	
	python updateWebp.py dir [Specifiedsize] 
	dir： 指定的目录,只转换指定目录
	Specifiedsize： 图片大小超过Specifiedsize才转换webp，默认Specifiedsize=50，Specifiedsize单位是KB,即超过50KB图片将转换为webp。

	eg：python updateWebp.py  ~/update/app/demo



FAQ:
========

1."/bin/sh: 1: cwebp: not found"

first method(cp):
```java
sudo cp cwebp /usr/local/bin/
```
second method(download the command line tools cwebp):
```java
1)download libwebp-0.6.0-linux-x86-32.tar.gz 
	https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-0.6.0-linux-x86-32.tar.gz
2).tar xvzf  libwebp-0.6.0-linux-x86-32.tar.gz
3).sudo cp libwebp-0.6.0-linux-x86-32/bin/cwebp  /usr/local/bin/
```
third method(build the cwebp yourself for linux):
```java
1).sudo apt-get install libjpeg-dev libpng-dev libtiff-dev libgif-dev
2).download source,libwebp-0.6.0.tar.gz 
	https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-0.6.0.tar.gz
3).Compiling the source. 
	tar xvzf libwebp-0.6.0.tar.gz
	cd libwebp-0.6.0
	./configure --enable-everything
	make
	sudo make install
```

Discuss:
========
tanhaiqing89@126.com
