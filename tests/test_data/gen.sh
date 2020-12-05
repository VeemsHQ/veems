# ffmpeg -i 2160p_24fps.mp4 -vf fps=1 out%d.png

ffmpeg -i 1080p_30fps_vertical.webm -vf "select=gt(scene\,0.4)" -vsync vfr -vf fps=3/60 img%03d.jpg
