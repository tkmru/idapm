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

