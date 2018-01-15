python $OBJDECPATH/object_detection/train.py \
    --logtostderr \
    --pipeline_config_path=../model/faster_rcnn_nas_coco.config \
    --train_dir=../data/faster_rcnn_nas_coco_tielu_train_logs \
    2>&1 | tee ../data/faster_rcnn_nas_coco_v1_tielu_train_logs.txt &
