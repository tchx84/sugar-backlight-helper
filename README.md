sugar-backlight-helper
======================

To install (promise proper install ASAP)
##########

```
$ git clone https://github.com/tchx84/sugar-backlight-helper.git
$ cd sugar-backlight-helper/
$ sudo cp sugar-backlight-helper /usr/libexec/
$ sudo chmod +x /usr/libexec/sugar-backlight-helper/
$ sudo cp org.sugar.brightness.policy /usr/share/polkit-1/actions/
```

To Use
#######

```
$ /usr/libexec/sugar-backlight-helper --get-brightness
$ /usr/libexec/sugar-backlight-helper --get-max-brightness
$ pkexec /usr/libexec/sugar-backlight-helper --set-brightness INT
```
