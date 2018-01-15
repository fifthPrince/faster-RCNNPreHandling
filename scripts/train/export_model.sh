

python $OBJDECPATH/object_detection/export_inference_graph.py \
    --input_type image_tensor \
    --pipeline_config_path $WORKPATH/model/faster_rcnn_nas_coco.config \
    --trained_checkpoint_prefix ../data/ssd_mobilenet_train_logs/model.ckpt-2000 \
    --output_directory $WORKPATH/$IMAGEPATH/exportModel



