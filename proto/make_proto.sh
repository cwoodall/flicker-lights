protoc --plugin=protoc-gen-nanopb=/home/cwoodall/src/nanopb/generator/protoc-gen-nanopb \
        --nanopb_out=../boards/basestation/src \
        --python_out=../pyflickerlight/flickerlights/proto \
        *.proto
