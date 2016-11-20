GIT_BASE_DIR=`git rev-parse --show-toplevel`
NANOPB_DIR="$HOME/src/nanopb"
protoc  --proto_path=$GIT_BASE_DIR/proto \
        --plugin=protoc-gen-nanopb=$NANOPB_DIR/generator/protoc-gen-nanopb \
        --nanopb_out=$GIT_BASE_DIR/boards/basestation/src \
        --python_out=$GIT_BASE_DIR/pyflickerlight/flickerlights/proto \
	$GIT_BASE_DIR/proto/*.proto
