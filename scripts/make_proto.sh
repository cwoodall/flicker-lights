BASE_DIR=`git rev-parse --show-toplevel`
FIRMWARE_OUT=$BASE_DIR/firmware/basestation/src
PYTHON_OUT=$BASE_DIR/software/pyflickerlight/flickerlights/proto
PROTOBUF_DIR=$BASE_DIR/shared/proto
NANOPB_LOCATION=$HOME/src/nanopb/generator/protoc-gen-nanopb
protoc  -I$PROTOBUF_DIR \
	--plugin=protoc-gen-nanopb=$NANOPB_LOCATION \
        --nanopb_out=$FIRMWARE_OUT \
        --python_out=$PYTHON_OUT \
        $PROTOBUF_DIR/*.proto
