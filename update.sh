#!/usr/bin/env bash
mkdir -p data/input
mkdir -p data/output

echo "Downloading recent files from S3..."
recent_files=`aws s3 ls ${AWS_S3_BUCKET}/news/ | awk '{print $4}' | sort | tail -n 180`
while IFS= read -r line; do
  if [ ! -f data/input/${line} ]; then
    aws s3 cp --no-progress s3://${AWS_S3_BUCKET}/news/${line} data/input/ &
    sleep 0.5
  fi
done <<< "${recent_files}"
wait

echo "Unzipping files..."
gunzip -kf data/input/*.csv.gz

echo "Analyzing..."
python cli.py tag_and_stats

echo "Uploading results to S3..."
aws s3 sync --quiet data/output/ s3://${AWS_S3_BUCKET}/done-it-again-analysis/

