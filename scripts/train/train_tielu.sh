python $OBJDECPATH/object_detection/train.py \
    --logtostderr \
    --pipeline_config_path=$WORKPATH/model/faster_rcnn_nas_coco.config \
    --train_dir=$WORKPATH/$IMAGEPATH/data/faster_rcnn_nas_coco_train_logs \
    2>&1 | tee $WORKPATH/$IMAGEPATH/data/faster_rcnn_nas_coco_train_logs.txt &
