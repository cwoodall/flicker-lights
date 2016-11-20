# Flicker Lights

## dependencies

- protobuf (proto2)
- python-protobuf
- nanopb (a light-weight c version of protobuf)

## Sub Modules

## Making Google Protobuf Files

The following command will make the appropriate nanopb (C) and python 
files for using the protobuf:

```
$ ./scripts/make_proto.sh
```

This requires you call it from within the Flicker Lights git directory
and also have nanopb on your system somewhere so it can access the
nanopb generator plugin. This is specified by `NANOPB_DIR` which defaults
to `$HOME/src/nanopb`, but could be anywhere.


