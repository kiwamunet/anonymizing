#!/bin/bash

curl -L https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip > samples/KEN_ALL.zip

unzip -d samples samples/KEN_ALL.zip

rm samples/KEN_ALL.zip