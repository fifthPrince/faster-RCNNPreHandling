
echo "$WORKPATH/$IMAGEPATH/img/tielu_label_map.pbtxt"
python create_pascal_tf_record.py \
    --label_map_path="$WORKPATH/$IMAGEPATH/img/tielu_label_map.pbtxt" \
    --data_dir="$WORKPATH/$IMAGEPATH/img/"  --year=VOC2012 --set=train \
    --output_path="$WORKPATH/$IMAGEPATH/TFRecord/tielu_train.record"

python create_pascal_tf_record.py \
    --label_map_path="$WORKPATH/$IMAGEPATH/img/tielu_label_map.pbtxt" \
    --data_dir="$WORKPATH/$IMAGEPATH/img/"  --year=VOC2012 --set=val \
    --output_path="$WORKPATH/$IMAGEPATH/TFRecord/tielu_val.record"


