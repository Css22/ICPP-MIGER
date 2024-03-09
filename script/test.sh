#!/bin/bash


offline_model_list=("GAN" "transformer" "bert" "resnet50" "resnet152" "mobilenet" "deeplabv3" "SqueezeNet" "unet" "vit")
online_model_list=("resnet50"  "resnet152" "vgg19" "vgg16" "inception_v3" "unet" "deeplabv3" "mobilenet_v2" "alexnet" "bert")

for model1 in ${offline_model_list[@]}; do
    cd /data/zbw/MIG/MIG/ATC-MIG/jobs/offline && proxychains python entry.py --task $model1  --epoch 1 
done


for model1 in ${online_model_list[@]}; do
    cd /data/zbw/MIG/MIG/ATC-MIG/jobs/online && python entry.py --task $model1 --batch 32
done

