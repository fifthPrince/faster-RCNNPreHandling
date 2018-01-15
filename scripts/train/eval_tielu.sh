
python $OBJDECPATH/object_detection/eval.py \
    --logtostderr \
    --pipeline_config_path=$WORKPATH/model/faster_rcnn_nas_coco.config \
    --checkpoint_dir=$WORKPATH/$IMAGEPATH/data/faster_rcnn_nas_coco_train_logs \
    --eval_dir=$WORKPATH/$IMAGEPATH/data/faster_rcnn_nas_coco_val_logs &
