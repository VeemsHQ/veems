# ffmpeg -i 2160p_24fps.mp4 -vf fps=1 out%d.png

plist=(15, 46, 77, 108, 139, 171, 202, 233, 264, 295, 326, 357, 388, 419, 450, 481, 513, 544, 575, 606, 637)
for i in ${plist[@]}; do
    start_time=${i//,/}
    echo $start_time
    ffmpeg -ss $start_time -i 360p_30fps_10min.mp4 -vf "select=gt(scene\,0.4)" -vf select="eq(pict_type\,I)" -vframes 1 thumbs/$start_time.jpg
done
