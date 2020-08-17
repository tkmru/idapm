# idapm

`idapm` is IDA Plugin Manager. It still only works on macOS.

## Motivation

Managing the IDA Plugin is inconvenient. There is no official package manager and you have to copy files to the plugin directory manually. 
So I developed a plugin manager inspired by `go get` that allows you to install plugins from GitHub repositories without API server, and also allows you to import plugins from different directories on your PC with a single command.

## Installation

```
$ pip install git+ssh://git@github.com/tkmru/idapm.git
```

## Usage

### init

```
$ idapm init
~/idapm.json was created successfully!
```

### install

```
$ idapm install L4ys/LazyIDA
----------------------
Cloning into '/Applications/IDA Pro 7.5/ida.app/Contents/MacOS/plugins/idapm/L4ys/LazyIDA'...
Symbolic link(/Applications/IDA Pro 7.5/ida.app/Contents/MacOS/plugins/LazyIDA.py) has been created
Installed successfully!
```

```
$ cat /Users/tkmru/idapm.json
{
  "plugins": [
    "L4ys/LazyIDA"
  ]
}
```

```
$ idapm install --local ./
Copy to /Applications/IDA Pro 7.5/ida.app/Contents/MacOS/plugins/test.py from ./test.py
Installed successfully!
```

### list

```
$ idapm list
List of scripts in IDA plugin directory
LazyIDA.py

List of plugins in config
L4ys/LazyIDA
```

### check

```
$ idapm check
IDA plugin dir:    /Applications/IDA Pro 7.5/ida.app/Contents/MacOS/plugins
idapm config path: /Users/tkmru/idapm.json
```

## License

GPLv3 - GNU General Public License, version 3

Copyright (C) 2020 tkmru
